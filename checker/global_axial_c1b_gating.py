#!/usr/bin/env python3
"""Lineage gating and numerical orchestration for the C1b producer."""
from __future__ import annotations

import argparse
import contextlib
import io
import re
import signal
import sys
from decimal import Decimal, ROUND_CEILING, localcontext
from fractions import Fraction
from pathlib import Path

from analysis import c1b_resumable_driver as persistence

_stop_requested = False

def decimal_add_up(a, b):
    with localcontext() as dc:
        dc.prec = max(120, len(a) + len(b) + 20)
        dc.rounding = ROUND_CEILING
        return str(Decimal(a) + Decimal(b))


_ARB_RE = re.compile(r"^\[?\s*([^\s\]]+)\s*\+/-\s*([^\s\]]+)\s*\]?$")


def arb_decimal_record(text):
    """Normalize an Arb decimal rendering without binary float conversion."""
    s = text.strip()
    if s == "None":
        return None
    if s.startswith("[+/-"):
        rad = s[len("[+/-"):].strip().rstrip("]").strip()
        mid = "0"
        return {"mid": mid, "rad": rad, "upper": decimal_add_up(mid, rad)}
    m = _ARB_RE.match(s)
    if m:
        mid, rad = m.group(1), m.group(2)
        return {"mid": mid, "rad": rad, "upper": decimal_add_up(mid, rad)}
    # Exact decimal Arb rendering.
    return {"mid": s, "rad": "0", "upper": s}



class Tee(io.TextIOBase):
    def __init__(self, target):
        self.target = target
        self.lines = []
        self.partial = ""

    def write(self, text):
        self.target.write(text)
        self.target.flush()
        self.partial += text
        while "\n" in self.partial:
            line, self.partial = self.partial.split("\n", 1)
            self.lines.append(line)
        return len(text)

    def flush(self):
        self.target.flush()


def parse_trace(lines):
    result = {
        "predictor": [],
        "tube_stages": [],
        "root_steps": [],
        "root_enclosure": [],
        "acceptance": [],
        "exterior_stages": [],
        "middle_partition": [],
    }
    tube = re.compile(
        r"^C1B_TUBE_STAGE\s+\d+\s+\d+\s+\S+\s+\S+\s+(T[0-2]).*?"
        r"gt_bad\s+(\d+)\s+left_bad\s+(\d+)\s+right_bad\s+(\d+).*?"
        r"gt_worst_upper\s+(.*?)\s+left_worst_lower\s+(.*?)\s+right_worst_upper\s+(.*)$"
    )
    exterior = re.compile(
        r"^C1B_EXTERIOR_STAGE\s+\d+\s+\d+\s+(E[0-2]).*?"
        r"unresolved\s+(\d+).*?worst_left_lower\s+(.*?)\s+worst_right_upper\s+(.*)$"
    )
    for line in lines:
        if line.startswith("C1B_PREDICTOR "):
            result["predictor"].append(line)
        elif line.startswith("C1B_ROOT_STEP "):
            result["root_steps"].append(line)
        elif line.startswith("C1B_ROOT_ENCLOSURE "):
            result["root_enclosure"].append(line)
        elif line.startswith("C1B_PREDICTOR_ACCEPT "):
            result["acceptance"].append(line)
        elif line.startswith("C1B_MIDDLE_T_PARTITION "):
            result["middle_partition"].append(line)
        else:
            m = tube.match(line)
            if m:
                result["tube_stages"].append({
                    "stage": m.group(1),
                    "gt_unresolved": int(m.group(2)),
                    "left_unresolved": int(m.group(3)),
                    "right_unresolved": int(m.group(4)),
                    "gt_worst_upper": arb_decimal_record(m.group(5)),
                    "left_worst_lower": arb_decimal_record(m.group(6)),
                    "right_worst_upper": arb_decimal_record(m.group(7)),
                })
                continue
            m = exterior.match(line)
            if m:
                result["exterior_stages"].append({
                    "stage": m.group(1),
                    "unresolved": int(m.group(2)),
                    "worst_left_lower": arb_decimal_record(m.group(3)),
                    "worst_right_upper": arb_decimal_record(m.group(4)),
                })
    return result


def serialize_root(root):
    if root is None:
        return None
    return [persistence.rational_text(root[0]), persistence.rational_text(root[1])]


def serialize_record(rec, tc, mode, work, reason, trace):
    if rec is None:
        return {
            "predictor_mode": mode,
            "t_c": None if tc is None else persistence.rational_text(tc),
            "T_star": None,
            "left_clamp": None,
            "right_clamp": None,
            "corner_hull": None,
            "tube_stage": None,
            "sup_error": None,
            "middle_partition": None,
            "work": {k: int(v) for k, v in work.items()},
            "work_total": int(sum(work.values())),
            "reason": reason,
            "trace": trace,
        }
    return {
        "predictor_mode": rec["mode"],
        "t_c": persistence.rational_text(rec["tc"]),
        "T_star": serialize_root(rec["root"]),
        "left_clamp": bool(rec["left_clamp"]),
        "right_clamp": bool(rec["right_clamp"]),
        "corner_hull": int(rec["corner_hull"]),
        "tube_stage": rec["tube_stage"],
        "sup_error": persistence.rational_text(rec["sup_error"]),
        "middle_partition": [
            [kind, persistence.rational_text(lo), persistence.rational_text(hi)]
            for kind, lo, hi in rec["pieces"]
        ],
        "work": {k: int(v) for k, v in work.items()},
        "work_total": int(sum(work.values())),
        "reason": reason,
        "trace": trace,
    }


def replay(kernel, records):
    queue, ok = kernel.coarse_ledger()
    if not ok:
        raise SystemExit("COARSE_LEDGER_FAIL")
    persisted = persistence.resume_state(records)
    previous_root = None
    for payload in persisted["terminal"]:
        if not queue:
            raise SystemExit("LEDGER_EXTRA_SLAB")
        slab = queue.pop(0)
        expected = slab_payload(slab)
        if any(payload[key] != expected[key] for key in expected):
            raise SystemExit("LEDGER_SLAB_ORDER_FAIL")
        decision = payload["decision"]
        if decision == "ACCEPT":
            root = payload["result"]["T_star"]
            previous_root = tuple(Fraction(value) for value in root)
        elif decision == "REFINE":
            left, right = slab.children()
            queue = [left, right] + queue
        elif decision == "ABORT":
            raise SystemExit("LEDGER_TERMINAL_ABORT")
    return {
        "queue": queue,
        "previous_root": previous_root,
        **persisted,
    }


def estimates(kernel):
    predictor = 513 * 2 * kernel.PRED_SCAN_PANELS
    t0 = 8 * 4 * 4096 + 2 * 4 * 4096
    root = kernel.ROOT_STEPS * kernel.ROOT_LBOXES * kernel.ROOT_PANELS
    e0 = kernel.E0_TBOXES * kernel.E0_LBOXES * kernel.E_STAGES[0][1]
    early = kernel.N_COARSE * (predictor + t0 + root + e0)
    no_refine_late = kernel.N_COARSE * (
        predictor + kernel.ATTEMPT_WORK_CEILING
    )
    return {
        "coarse_slabs": kernel.N_COARSE,
        "predictor_per_attempt": predictor,
        "T0_E0_early_pass_one_lineage": early,
        "T2_E2_no_refinement_one_lineage": no_refine_late,
        "accepted_gating_ceiling": kernel.ACCEPTED_WORK_CEILING,
        "global_attempted_gating_ceiling": kernel.GLOBAL_ATTEMPT_WORK_CEILING,
    }


def header_payload(kernel, lineage, pins, identity):
    return {
        "chain_version": CHAIN_VERSION,
        "lineage": lineage,
        "created_utc": persistence.utc_now(),
        "identity": identity,
        "precision_bits": kernel.BITS,
        "degree": kernel.DEG,
        "u_star": persistence.rational_text(kernel.USTAR),
        "lambda_domain": [persistence.rational_text(kernel.L_LO), persistence.rational_text(kernel.L_HI)],
        "stages": {
            "T": [list(x) for x in kernel.T_STAGES],
            "ROOT": [kernel.ROOT_STEPS, kernel.ROOT_LBOXES, kernel.ROOT_PANELS],
            "E": [list(x) for x in kernel.E_STAGES],
        },
        "caps": {
            "coarse": kernel.N_COARSE,
            "accepted": kernel.MAX_ACCEPTED,
            "attempted": kernel.MAX_ATTEMPTED,
            "depth": kernel.MAX_DEPTH,
        },
        "budgets": {
            "attempt": kernel.ATTEMPT_WORK_CEILING,
            "accepted": kernel.ACCEPTED_WORK_CEILING,
            "global": kernel.GLOBAL_ATTEMPT_WORK_CEILING,
            "predictor": 513 * 2 * kernel.PRED_SCAN_PANELS,
        },
        "estimates": estimates(kernel),
        "pin_manifest": pins,
    }


def request_stop(signum, frame):
    global _stop_requested
    _stop_requested = True


def run_full(kernel, lineage, run_dir):
    pins = persistence.load_pins()
    if pins is None:
        raise SystemExit("RESUMABLE_PIN_MANIFEST_MISSING")
    identity = persistence.environment_snapshot(pins[lineage])
    persistence.verify_identity(identity, pins[lineage])
    run_dir = Path(run_dir)
    ledger = persistence.Ledger(run_dir / "ledger.jsonl")
    if not ledger.records:
        ledger.append("header", header_payload(kernel, lineage, pins[lineage], identity))
    else:
        header = ledger.records[0]
        if header["record_type"] != "header":
            raise SystemExit("LEDGER_HEADER_MISSING")
        if header["payload"]["identity"] != identity:
            raise SystemExit("RESUME_HEADER_IDENTITY_MISMATCH")
    state = replay(kernel, ledger.records)
    full_charge = kernel.ATTEMPT_WORK_CEILING + 513 * 2 * kernel.PRED_SCAN_PANELS
    for seq in state["unmatched"]:
        ledger.append("interrupted_attempt_charge", {
            "attempt_sequence": seq,
            "charged_work": full_charge,
            "charged_attempt_unit": 1,
            "utc": persistence.utc_now(),
        })
    if state["unmatched"]:
        state = replay(kernel, ledger.records)
    persistence.check_ceiling(
        state["attempted"], kernel.MAX_ATTEMPTED, "MAX_ATTEMPTED_SLABS_EXCEEDED"
    )
    segment_index = persistence.next_segment_index(ledger.records)
    ledger.append("segment_begin", {
        "segment_index": segment_index,
        "utc": persistence.utc_now(),
        "pin_check": "PASS",
        "identity": identity,
        "cumulative_work": state["global_work"],
        "attempted": state["attempted"],
        "next_slab": None if not state["queue"] else slab_payload(state["queue"][0]),
    })
    def append_segment_end(reason, cumulative_work, attempted, **extra):
        post_identity = persistence.environment_snapshot(pins[lineage])
        persistence.verify_identity(post_identity, pins[lineage])
        payload = {
            "segment_index": segment_index,
            "utc": persistence.utc_now(),
            "reason": reason,
            "cumulative_work": cumulative_work,
            "attempted": attempted,
            "post_pin_check": "PASS",
            "post_identity": post_identity,
        }
        payload.update(extra)
        ledger.append("segment_end", payload)

    signal.signal(signal.SIGTERM, request_stop)
    signal.signal(signal.SIGINT, request_stop)
    kernel.ctx.prec = kernel.BITS
    kernel.base.ctx.prec = kernel.BITS
    kernel.preflight()
    queue = state["queue"]
    previous_root = state["previous_root"]
    accepted_work = state["accepted_work"]
    global_work = state["global_work"]
    attempted = state["attempted"]
    accepted_count = len(state["accepted"])
    while queue:
        if _stop_requested:
            append_segment_end(
                "requested_stop", global_work, attempted,
                next_slab=slab_payload(queue[0]),
            )
            return
        if attempted >= kernel.MAX_ATTEMPTED:
            raise SystemExit("MAX_ATTEMPTED_SLABS_EXCEEDED")
        slab = queue.pop(0)
        attempted += 1
        attempt_sequence = attempted
        ledger.append("attempt_begin", {
            "attempt_sequence": attempt_sequence,
            **slab_payload(slab),
            "previous_root": serialize_root(previous_root),
            "cumulative_work_before": global_work,
            "utc": persistence.utc_now(),
        })
        tee = Tee(sys.stdout)
        with contextlib.redirect_stdout(tee):
            ok, rec, root, tc, work, reason = kernel.attempt(slab, previous_root)
        trace = parse_trace(tee.lines)
        result = serialize_record(rec, tc, None if rec is None else rec["mode"], work, reason, trace)
        attempt_work = result["work_total"]
        global_work += attempt_work
        if not persistence.within_ceiling(
            global_work, kernel.GLOBAL_ATTEMPT_WORK_CEILING
        ):
            decision = "ABORT"
        elif ok:
            decision = "ACCEPT"
            accepted_count += 1
            accepted_work += attempt_work
            previous_root = root
            if (
                not persistence.within_ceiling(accepted_count, kernel.MAX_ACCEPTED)
                or not persistence.within_ceiling(
                    accepted_work, kernel.ACCEPTED_WORK_CEILING
                )
            ):
                decision = "ABORT"
        elif slab.depth < kernel.MAX_DEPTH:
            decision = "REFINE"
        else:
            decision = "ABORT"
        payload = {
            "attempt_sequence": attempt_sequence,
            **slab_payload(slab),
            "decision": decision,
            "result": result,
            "accepted_count": accepted_count,
            "accepted_work": accepted_work,
            "cumulative_work_after": global_work,
            "attempted_count": attempted,
            "utc": persistence.utc_now(),
        }
        ledger.append("slab_record", payload)
        if decision == "ACCEPT":
            pass
        elif decision == "REFINE":
            left, right = slab.children()
            queue = [left, right] + queue
        else:
            append_segment_end(
                "failure", global_work, attempted,
                next_slab=slab_payload(slab),
            )
            raise SystemExit(f"C1B_UNRESOLVED {slab}")
    slabs = [r["payload"] for r in ledger.records if r["record_type"] == "slab_record"
             and r["payload"]["decision"] == "ACCEPT"]
    union_ok = bool(slabs)
    if union_ok:
        union_ok = slabs[0]["lambda_lo"] == persistence.rational_text(kernel.L_LO)
        union_ok = union_ok and slabs[-1]["lambda_hi"] == persistence.rational_text(kernel.L_HI)
        union_ok = union_ok and all(
            a["lambda_hi"] == b["lambda_lo"] for a, b in zip(slabs, slabs[1:])
        )
    append_segment_end(
        "completed" if union_ok else "failure",
        global_work,
        attempted,
        accepted=accepted_count,
        exact_union=union_ok,
        final_record_hash_before_end=ledger.last_hash,
    )
    print("C1B_RESUMABLE_FINAL", "PASS" if union_ok else "UNRESOLVED",
          "accepted", accepted_count, "attempted", attempted,
          "work", global_work, "ledger_hash", ledger.last_hash)
    if not union_ok:
        raise SystemExit("C1B_EXACT_UNION_FAIL")


def main(kernel, lineage):
    parser = argparse.ArgumentParser()
    parser.add_argument("--ledger-only", action="store_true")
    parser.add_argument("--run-dir")
    args = parser.parse_args()
    kernel.ctx.prec = kernel.BITS
    kernel.base.ctx.prec = kernel.BITS
    if args.ledger_only:
        kernel.preflight()
        print("C1B_PREFLIGHT_ESTIMATES", persistence.canonical_bytes(estimates(kernel)).decode("ascii"))
        print("C1B_LEDGER_ONLY_WRITES_REPOSITORY", False)
        return
    if not args.run_dir:
        raise SystemExit("--run-dir required")
    run_full(kernel, lineage, args.run_dir)
