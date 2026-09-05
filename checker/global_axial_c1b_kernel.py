#!/usr/bin/env python3
"""Full-source 192-bit C1b checker.

CHECKER_KERNEL=TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION
INDEPENDENCE_SCOPE=PRECISION/PARTITION/GATING
Status: IMPLEMENTED_PROTOTYPE / MACHINE_NOT_RUN / NOT_BINDING.
"""
from __future__ import annotations
import argparse
import hashlib
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

from flint import arb, ctx

from checker import global_axial_c0_checker as base
from checker import c0a_four_group_v2 as grouped
from checker.monotone_tube_refinement_checker import _ordinary_refinement as _gt_ordinary
from checker.monotone_tube_interval_checker import _corner as _gt_corner

BITS, DEG = 192, 50
USTAR = Fraction(3, 5)
L_LO, L_HI = Fraction(9, 20), Fraction(5, 8)
DLAM, N_COARSE = Fraction(1, 800), 140
MAX_DEPTH, MAX_ACCEPTED, MAX_ATTEMPTED = 3, 1120, 2100
T_LO, T_MID_HI, T_HI = Fraction(1, 2), Fraction(31, 32), Fraction(1)
W0, PRED_ACCEPT, ROOT_TARGET = Fraction(1, 16), Fraction(1, 64), Fraction(1, 128)
T_STAGES = (("T0", 8, 4, 4096), ("T1", 16, 8, 4096), ("T2", 32, 16, 8192))
ROOT_STEPS, ROOT_LBOXES, ROOT_PANELS = 12, 16, 8192
E0_TBOXES, E0_LBOXES = 24, 8
E_STAGES = (("E0", 1024), ("E1", 2048), ("E2", 4096))
E_BOX_CAP = 4096
PRED_GRID_DEN, PRED_SCAN_PANELS = 1024, 256
ATTEMPT_WORK_CEILING = 23_560_192
GLOBAL_ATTEMPT_WORK_CEILING = 49_476_403_200
ACCEPTED_WORK_CEILING = 26_387_415_040
BOB_RECEIPT = Path("analysis/GLOBAL_AXIAL_C1B_BOB_MACHINE_RECEIPT.md")
BOB_EVIDENCE_HEAD = "25efb59b851eb9d7a3d5ce30309eb8903d976930"
BOB_CONTRACT_BLOB = "215193e2fc2a1abcf2aee2527c4c2e6f3176ea6c"
BOB_AMENDMENT_BLOB = "8e04e2efaf816bab9d9d1f3fd0a9d753538b31ad"
BOB_RECEIPT_BLOB = "0f19e3877b9675506ac8f35a5702147a84723c43"

@dataclass(frozen=True)
class Slab:
    coarse: int
    depth: int
    ll: Fraction
    lr: Fraction
    def children(self):
        m = (self.ll + self.lr) / 2
        return (Slab(self.coarse, self.depth + 1, self.ll, m),
                Slab(self.coarse, self.depth + 1, m, self.lr))

@dataclass(frozen=True)
class EBox:
    side: str
    tl: Fraction
    tr: Fraction
    ll: Fraction
    lr: Fraction

def split(a, b, n):
    h = (b - a) / n
    return [(a + i*h, a + (i+1)*h) for i in range(n)]

def coarse_ledger():
    q = [Slab(i, 0, L_LO + i*DLAM, L_LO + (i+1)*DLAM) for i in range(N_COARSE)]
    ok = (len(q) == N_COARSE and q[0].ll == L_LO and q[-1].lr == L_HI
          and all(a.lr == b.ll for a, b in zip(q, q[1:]))
          and all(s.lr - s.ll == DLAM for s in q))
    return q, ok

def interval(a, b):
    return base._box(base._point(a), base._point(b))

def _stats():
    return {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}

def _g_density_stable(s, t, L, stats):
    s, x, mu, eps, A, delta, delta_sq, gam, u, L2, q, rootq, W, W2, n, m, p, big_q = grouped._primitives(s, t, L)
    R, _, _, _ = base._R(u, gam, stats)
    gt = L * n / (W * q * rootq)
    alpha2 = u * R * R
    return s * (-mu * alpha2 - 2 * A * R * gt)

def g_box(tl, tr, ll, lr, panels):
    grid, root = base._partition(panels)
    t, lam = interval(tl, tr), interval(ll, lr)
    stats, z = _stats(), arb(0)
    for a, b in zip(grid, grid[1:]):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        z += _g_density_stable(base._box(aa, bb), t, lam, stats) * (bb-aa)
    return z, panels

def gt_box(tl, tr, ll, lr, panels):
    grid, root = base._partition(panels)
    t, lam = interval(tl, tr), interval(ll, lr)
    z, charts = arb(0), defaultdict(int)
    for si, (a, b) in enumerate(zip(grid, grid[1:])):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        s = base._box(aa, bb)
        if tr == T_HI and si == 0:
            val, chart = _gt_corner(s, t, lam)
            terms = (val,)
        else:
            chart, terms = _gt_ordinary(s, t, lam)
        charts[chart] += 1
        z += sum(terms, arb(0)) * (bb-aa)
    return z, dict(charts), panels

def bob_preflight():
    data = BOB_RECEIPT.read_bytes()
    text = data.decode()
    header = f"blob {len(data)}\0".encode()
    blob = hashlib.sha1(header + data).hexdigest()
    required = (
        "MACHINE_PASS / C1B_SUBGATE_ONLY / FULL_C1B_NOT_YET_CLOSED",
        BOB_EVIDENCE_HEAD, BOB_CONTRACT_BLOB, BOB_AMENDMENT_BLOB,
        "B_ob(lambda) < 0 for every lambda in [9/20,5/8]",
    )
    ok = all(x in text for x in required) and blob == BOB_RECEIPT_BLOB
    print("C1B_BOB_PIN_CHECK", "PASS" if ok else "FAIL",
          "receipt_blob", blob, "expected_receipt_blob", BOB_RECEIPT_BLOB,
          "evidence_head", BOB_EVIDENCE_HEAD,
          "contract_blob", BOB_CONTRACT_BLOB, "amendment_blob", BOB_AMENDMENT_BLOB)
    if not ok:
        raise SystemExit("BOB_RECEIPT_PIN_FAIL")

def predictor_scan(slab):
    lm = (slab.ll + slab.lr) / 2
    prev_t = T_LO
    prev, work = g_box(prev_t, prev_t, lm, lm, PRED_SCAN_PANELS)
    prev_mid = prev.mid()
    for k in range(1, 513):
        t = T_LO + Fraction(k, PRED_GRID_DEN)
        v, c = g_box(t, t, lm, lm, PRED_SCAN_PANELS)
        work += c
        if prev_mid > 0 and v.mid() < 0:
            return (prev_t, t), work
        prev_t, prev_mid = t, v.mid()
    return None, work

def choose_predictor(slab, previous_root):
    tcont = Fraction(9, 16) if previous_root is None else (previous_root[0] + previous_root[1]) / 2
    bracket, work = predictor_scan(slab)
    if bracket is None:
        print("C1B_PREDICTOR", slab.coarse, slab.depth, slab.ll, slab.lr,
              "P0", tcont, "P1 NONE", "P2 UNRESOLVED", "scan_cells", work)
        return None, None, work
    tscan = (bracket[0] + bracket[1]) / 2
    tc = tcont if abs(tcont-tscan) <= PRED_ACCEPT else tscan
    mode = "continuation" if tc == tcont else "relocated"
    print("C1B_PREDICTOR", slab.coarse, slab.depth, slab.ll, slab.lr,
          "P0", tcont, "P1", bracket, "P2", tc, "mode", mode, "scan_cells", work)
    return tc, mode, work

def tube_stage(slab, tc, stage):
    label, nt, nl, panels = stage
    tm, tp = max(T_LO, tc-W0), min(T_HI, tc+W0)
    lclamp, rclamp = tm == T_LO, tp == T_HI
    gt_bad = left_bad = right_bad = corner = cells = 0
    gt_worst = left_worst = right_worst = None
    for tl, tr in split(tm, tp, nt):
        for ll, lr in split(slab.ll, slab.lr, nl):
            try:
                v, charts, c = gt_box(tl, tr, ll, lr, panels)
                cells += c; corner += charts.get("corner_hull", 0); good = v.upper() < 0
            except (ValueError, ZeroDivisionError):
                v, good = None, False
            gt_bad += 0 if good else 1
            if v is not None and (gt_worst is None or v.upper() > gt_worst[0]):
                gt_worst = (v.upper(), tl, tr, ll, lr)
    for ll, lr in split(slab.ll, slab.lr, nl):
        try:
            v, c = g_box(tm, tm, ll, lr, panels); cells += c; good = v.lower() > 0
        except (ValueError, ZeroDivisionError):
            v, good = None, False
        left_bad += 0 if good else 1
        if v is not None and (left_worst is None or v.lower() < left_worst[0]):
            left_worst = (v.lower(), ll, lr)
        if not rclamp:
            try:
                v, c = g_box(tp, tp, ll, lr, panels); cells += c; good = v.upper() < 0
            except (ValueError, ZeroDivisionError):
                v, good = None, False
            right_bad += 0 if good else 1
            if v is not None and (right_worst is None or v.upper() > right_worst[0]):
                right_worst = (v.upper(), ll, lr)
    ok = gt_bad == left_bad == right_bad == 0
    print("C1B_TUBE_STAGE", slab.coarse, slab.depth, slab.ll, slab.lr, label,
          "tc", tc, "walls", (tm, tp), "left_clamp", lclamp, "right_clamp", rclamp,
          "right_mode", "B_ob_receipt" if rclamp else "finite_t_wall",
          "gt_bad", gt_bad, "left_bad", left_bad, "right_bad", right_bad,
          "corner_hull", corner,
          "gt_worst_upper", None if gt_worst is None else gt_worst[0].str(50),
          "left_worst_lower", None if left_worst is None else left_worst[0].str(50),
          "right_worst_upper", None if right_worst is None else right_worst[0].str(50))
    return ok, tm, tp, lclamp, rclamp, corner, cells, label

def tube_first_pass(slab, tc):
    total = corner = 0
    last = None
    for stage in T_STAGES:
        out = tube_stage(slab, tc, stage)
        last = out; total += out[6]; corner += out[5]
        if out[0]:
            print("C1B_TUBE_FIRST_PASS", slab.coarse, slab.depth, stage[0])
            return True, out[1], out[2], out[3], out[4], corner, total, stage[0]
    return False, last[1], last[2], last[3], last[4], corner, total, None

def root_localize(slab, tm, tp):
    lo, hi, work = tm, tp, 0
    reason = "MAX_STEPS"
    for step in range(1, ROOT_STEPS + 1):
        if hi - lo <= ROOT_TARGET:
            reason = "TARGET_WIDTH"; break
        mid = (lo + hi) / 2
        vals = []
        for ll, lr in split(slab.ll, slab.lr, ROOT_LBOXES):
            try:
                v, c = g_box(mid, mid, ll, lr, ROOT_PANELS); work += c
            except (ValueError, ZeroDivisionError):
                v = None
            vals.append(v)
        pos = all(v is not None and v.lower() > 0 for v in vals)
        neg = all(v is not None and v.upper() < 0 for v in vals)
        print("C1B_ROOT_STEP", slab.coarse, slab.depth, step, "mid", mid,
              "all_pos", pos, "all_neg", neg,
              "min_lower", None if any(v is None for v in vals) else min(v.lower() for v in vals).str(40),
              "max_upper", None if any(v is None for v in vals) else max(v.upper() for v in vals).str(40))
        if pos:
            lo = mid
        elif neg:
            hi = mid
        else:
            reason = "MID_SIGN_UNRESOLVED"; break
    ok = hi - lo <= ROOT_TARGET
    print("C1B_ROOT_ENCLOSURE", "PASS" if ok else "UNRESOLVED",
          slab.coarse, slab.depth, "T_star", (lo, hi), "width", hi-lo, "reason", reason)
    return ok, (lo, hi), work

def predictor_accept(tc, root):
    err = max(abs(tc-root[0]), abs(tc-root[1]))
    ok = err <= PRED_ACCEPT
    print("C1B_PREDICTOR_ACCEPT", "PASS" if ok else "FAIL",
          "tc", tc, "T_star", root, "sup_error", err, "limit", PRED_ACCEPT)
    return ok, err

def _e0_counts(tm, tp):
    wl = max(Fraction(0), tm - T_LO)
    wr = max(Fraction(0), T_MID_HI - tp)
    if wl == 0 and wr == 0: return 0, 0
    if wl == 0: return 0, E0_TBOXES
    if wr == 0: return E0_TBOXES, 0
    q = Fraction(E0_TBOXES) * wl / (wl + wr)
    nl = max(1, min(23, q.numerator // q.denominator))
    return nl, E0_TBOXES - nl

def exterior_seed(slab, tm, tp):
    nl, nr = _e0_counts(tm, tp)
    out = []
    if nl:
        for tl, tr in split(T_LO, tm, nl):
            for ll, lr in split(slab.ll, slab.lr, E0_LBOXES):
                out.append(EBox("L", tl, tr, ll, lr))
    if nr:
        for tl, tr in split(tp, T_MID_HI, nr):
            for ll, lr in split(slab.ll, slab.lr, E0_LBOXES):
                out.append(EBox("R", tl, tr, ll, lr))
    print("C1B_E0_ALLOCATION", slab.coarse, slab.depth, "left_t_boxes", nl, "right_t_boxes", nr,
          "left_range", (T_LO, tm), "right_range", (tp, T_MID_HI))
    return out

def e_children(b):
    tm, lm = (b.tl+b.tr)/2, (b.ll+b.lr)/2
    return [EBox(b.side, a, c, d, e) for a,c in ((b.tl,tm),(tm,b.tr))
            for d,e in ((b.ll,lm),(lm,b.lr))]

def eval_exterior(boxes, panels):
    unresolved, resolved, work, worstL, worstR = [], [], 0, None, None
    for b in boxes:
        try:
            v, c = g_box(b.tl, b.tr, b.ll, b.lr, panels); work += c
            good = v.lower() > 0 if b.side == "L" else v.upper() < 0
        except (ValueError, ZeroDivisionError):
            v, good = None, False
        (resolved if good else unresolved).append(b)
        if v is not None and b.side == "L" and (worstL is None or v.lower() < worstL):
            worstL = v.lower()
        if v is not None and b.side == "R" and (worstR is None or v.upper() > worstR):
            worstR = v.upper()
    return unresolved, resolved, work, worstL, worstR

def exterior_cover(slab, tm, tp):
    current = exterior_seed(slab, tm, tp)
    terminal, work = 0, 0
    if not current:
        print("C1B_EXTERIOR", slab.coarse, slab.depth, "EMPTY_REMAINDER", "PASS")
        return True, work
    for idx, (label, panels) in enumerate(E_STAGES):
        unresolved, resolved, w, worstL, worstR = eval_exterior(current, panels)
        work += w; terminal += len(resolved)
        live_terminal = terminal + len(unresolved)
        print("C1B_EXTERIOR_STAGE", slab.coarse, slab.depth, label,
              "input", len(current), "resolved_now", len(resolved), "unresolved", len(unresolved),
              "live_terminal", live_terminal,
              "worst_left_lower", None if worstL is None else worstL.str(50),
              "worst_right_upper", None if worstR is None else worstR.str(50))
        if live_terminal > E_BOX_CAP:
            return False, work
        if not unresolved:
            print("C1B_EXTERIOR_FIRST_PASS", slab.coarse, slab.depth, label)
            return True, work
        if idx == len(E_STAGES)-1:
            return False, work
        current = [c for b in unresolved for c in e_children(b)]
        if terminal + len(current) > E_BOX_CAP:
            return False, work
    return False, work

def exact_middle_partition(tm, tp):
    pieces = []
    if T_LO < tm: pieces.append(("L", T_LO, tm))
    pieces.append(("TUBE", max(T_LO, tm), min(T_MID_HI, tp)))
    if tp < T_MID_HI: pieces.append(("R", tp, T_MID_HI))
    nonempty = [(k,a,b) for k,a,b in pieces if a < b]
    ok = bool(nonempty) and nonempty[0][1] == T_LO and nonempty[-1][2] == T_MID_HI \
         and all(x[2] == y[1] for x,y in zip(nonempty, nonempty[1:]))
    return ok, nonempty

def attempt(slab, previous_root):
    work = {"predictor":0, "tube":0, "root":0, "exterior":0}
    tc, mode, w = choose_predictor(slab, previous_root); work["predictor"] += w
    if tc is None: return False, None, None, None, work, "PREDICTOR"
    tok, tm, tp, lc, rc, corner, w, tstage = tube_first_pass(slab, tc); work["tube"] += w
    if not tok: return False, None, None, None, work, "TUBE"
    rok, root, w = root_localize(slab, tm, tp); work["root"] += w
    if not rok: return False, None, None, None, work, "ROOT"
    aok, err = predictor_accept(tc, root)
    if not aok: return False, None, None, None, work, "PREDICTOR_ACCEPT"
    eok, w = exterior_cover(slab, tm, tp); work["exterior"] += w
    if not eok: return False, None, None, None, work, "EXTERIOR"
    pok, pieces = exact_middle_partition(tm, tp)
    print("C1B_MIDDLE_T_PARTITION", "PASS" if pok else "FAIL", slab.coarse, slab.depth, pieces)
    if not pok: return False, None, None, None, work, "T_PARTITION"
    rec = {"slab":slab, "tc":tc, "mode":mode, "root":root, "sup_error":err,
           "tm":tm, "tp":tp, "left_clamp":lc, "right_clamp":rc,
           "corner_hull":corner, "tube_stage":tstage, "pieces":pieces}
    return True, rec, root, tc, work, "PASS"

def preflight():
    slabs, ok = coarse_ledger()
    print("GLOBAL_AXIAL_C1B_CHECKER — IMPLEMENTED_PROTOTYPE / MACHINE_NOT_RUN / NOT_BINDING")
    print("CHECKER_KERNEL TRANSCRIBED_COPY_NOT_INDEPENDENT_DERIVATION")
    print("INDEPENDENCE_SCOPE PRECISION/PARTITION/GATING")
    print("BITS", BITS, "DEG", DEG, "USTAR", USTAR)
    print("LAMBDA_DOMAIN", L_LO, L_HI, "direction increasing")
    print("COARSE_LEDGER", "PASS" if ok else "FAIL", "count", len(slabs),
          "first", (slabs[0].ll, slabs[0].lr), "last", (slabs[-1].ll, slabs[-1].lr))
    print("PREDICTOR_ORDER continuation -> bracket_scan -> relocated")
    print("PREDICTOR_ACCEPT", PRED_ACCEPT, "ROOT_TARGET", ROOT_TARGET)
    print("CLAMP_RULE", "max(1/2,tc-w0)", "min(1,tc+w0)", "w0", W0)
    print("CORNER_RULE", "tr==1 and first s-panel => checker corner_hull")
    print("T_STAGES", T_STAGES, "ROOT", (ROOT_STEPS,ROOT_LBOXES,ROOT_PANELS))
    print("E_POLICY", E0_TBOXES, E0_LBOXES, E_STAGES, "cap", E_BOX_CAP)
    print("CAPS", "coarse", N_COARSE, "accepted", MAX_ACCEPTED, "attempted", MAX_ATTEMPTED,
          "max_depth", MAX_DEPTH)
    print("WORK_CEILINGS", ATTEMPT_WORK_CEILING, ACCEPTED_WORK_CEILING, GLOBAL_ATTEMPT_WORK_CEILING)
    if not ok: raise SystemExit("PREFLIGHT_FAIL")
    bob_preflight()

