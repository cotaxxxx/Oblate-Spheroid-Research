#!/usr/bin/env python3
"""C1b full-cover producer skeleton with binding geometry policy fixed.

Status: IMPLEMENTED_PROTOTYPE / MACHINE_NOT_RUN / NOT_BINDING.
This file is intentionally committed before any full C1b evidence run.
"""
from __future__ import annotations

import argparse
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction

from flint import arb, ctx

from producer import global_axial_c0_producer as base
from producer.global_axial_c0_producer_v2 import _g_density_stable
from producer.monotone_tube_refinement_producer import _ordinary as _gt_ordinary
from producer.monotone_tube_refinement_producer import _corner as _gt_corner

BITS = 160
DEG = 50
USTAR = Fraction(3, 5)
L_LO, L_HI = Fraction(9, 20), Fraction(5, 8)
DLAM = Fraction(1, 800)
N_COARSE = 140
MAX_DEPTH = 3
MAX_ACCEPTED = 1120
MAX_ATTEMPTED = 2100
T_LO, T_MID_HI, T_HI = Fraction(1, 2), Fraction(31, 32), Fraction(1)
W0 = Fraction(1, 16)
PRED_ACCEPT = Fraction(1, 64)
ROOT_TARGET = Fraction(1, 128)
T_STAGES = (("T0", 8, 4, 4096), ("T1", 16, 8, 4096), ("T2", 32, 16, 8192))
ROOT_STEPS, ROOT_LBOXES, ROOT_PANELS = 12, 16, 8192
E0_TBOXES, E0_LBOXES = 24, 8
E_STAGES = (("E0", 1024), ("E1", 2048), ("E2", 4096))
E_BOX_CAP = 4096
PRED_GRID_DEN, PRED_SCAN_PANELS = 1024, 256
BOB_RECEIPT = "analysis/GLOBAL_AXIAL_C1B_BOB_MACHINE_RECEIPT.md"


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


def g_box(tl, tr, ll, lr, panels):
    grid, root = base._partition(panels)
    t, lam = interval(tl, tr), interval(ll, lr)
    stats = {"series": 0, "direct": 0, "series_hits_moving_u0": 0, "chart_unresolved": 0}
    z = arb(0)
    cells = 0
    for a, b in zip(grid, grid[1:]):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        z += _g_density_stable(base._box(aa, bb), t, lam, stats) * (bb-aa)
        cells += 1
    return z, cells


def gt_box(tl, tr, ll, lr, panels):
    grid, root = base._partition(panels)
    t, lam = interval(tl, tr), interval(ll, lr)
    z = arb(0)
    charts = defaultdict(int)
    cells = 0
    for si, (a, b) in enumerate(zip(grid, grid[1:])):
        aa = root if a == base.SQRT2 else base._point(a)
        bb = root if b == base.SQRT2 else base._point(b)
        s = base._box(aa, bb)
        if tr == T_HI and si == 0:
            chart, terms = _gt_corner(s, t, lam)
        else:
            chart, terms = _gt_ordinary(s, t, lam)
        charts[chart] += 1
        z += sum(terms, arb(0)) * (bb-aa)
        cells += 1
    return z, dict(charts), cells


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
    gt_bad = left_bad = right_bad = 0
    corner = cells = 0
    gt_worst = left_worst = right_worst = None
    for tl, tr in split(tm, tp, nt):
        for ll, lr in split(slab.ll, slab.lr, nl):
            try:
                v, charts, c = gt_box(tl, tr, ll, lr, panels); cells += c
                corner += charts.get("corner_hull", 0)
                good = v.upper() < 0
            except (ValueError, ZeroDivisionError):
                v, good = None, False
            gt_bad += 0 if good else 1
            if v is not None and (gt_worst is None or v.upper() > gt_worst[0]):
                gt_worst = (v.upper(), tl, tr, ll, lr, v)
    for ll, lr in split(slab.ll, slab.lr, nl):
        try:
            v, c = g_box(tm, tm, ll, lr, panels); cells += c; good = v.lower() > 0
        except (ValueError, ZeroDivisionError):
            v, good = None, False
        left_bad += 0 if good else 1
        if v is not None and (left_worst is None or v.lower() < left_worst[0]):
            left_worst = (v.lower(), ll, lr, v)
        if not rclamp:
            try:
                v, c = g_box(tp, tp, ll, lr, panels); cells += c; good = v.upper() < 0
            except (ValueError, ZeroDivisionError):
                v, good = None, False
            right_bad += 0 if good else 1
            if v is not None and (right_worst is None or v.upper() > right_worst[0]):
                right_worst = (v.upper(), ll, lr, v)
    ok = gt_bad == left_bad == right_bad == 0
    print("C1B_TUBE_STAGE", slab.coarse, slab.depth, slab.ll, slab.lr, label,
          "tc", tc, "walls", (tm, tp), "left_clamp", lclamp, "right_clamp", rclamp,
          "right_mode", "B_ob_receipt" if rclamp else "finite_t_wall",
          "gt_bad", gt_bad, "left_bad", left_bad, "right_bad", right_bad,
          "corner_hull", corner,
          "gt_worst_upper", None if gt_worst is None else gt_worst[0].str(50),
          "left_worst_lower", None if left_worst is None else left_worst[0].str(50),
          "right_worst_upper", None if right_worst is None else right_worst[0].str(50))
    return ok, tm, tp, lclamp, rclamp, corner, cells


def preflight():
    slabs, ok = coarse_ledger()
    print("C1B_PREFLIGHT — STRUCTURAL / NOT_EVIDENCE")
    print("BITS", BITS, "DEG", DEG, "USTAR", USTAR)
    print("LAMBDA_DOMAIN", L_LO, L_HI, "direction increasing")
    print("COARSE_LEDGER", "PASS" if ok else "FAIL", "count", len(slabs),
          "first", (slabs[0].ll, slabs[0].lr), "last", (slabs[-1].ll, slabs[-1].lr))
    print("EXACT_ADJACENCY", all(a.lr == b.ll for a, b in zip(slabs, slabs[1:])))
    print("PREDICTOR_ORDER continuation -> bracket_scan -> relocated")
    print("PREDICTOR_ACCEPT", PRED_ACCEPT, "ROOT_TARGET", ROOT_TARGET)
    print("CLAMP_RULE", "max(1/2,tc-w0)", "min(1,tc+w0)", "w0", W0)
    print("CORNER_RULE", "tr==1 and first s-panel => corner_hull")
    print("T_STAGES", T_STAGES)
    print("E_POLICY", E0_TBOXES, E0_LBOXES, E_STAGES, "cap", E_BOX_CAP)
    print("CAPS", N_COARSE, MAX_ACCEPTED, MAX_ATTEMPTED)
    if not ok:
        raise SystemExit("PREFLIGHT_FAIL")


def smoke(index, tc):
    ctx.prec = BITS; base.ctx.prec = BITS
    slabs, ok = coarse_ledger()
    if not ok or not (0 <= index < len(slabs)):
        raise SystemExit("BAD_LEDGER_OR_INDEX")
    slab = slabs[index]
    print("C1B_SMOKE — NOT_FULL_EVIDENCE", "slab", slab, "tc", tc)
    for st in T_STAGES:
        ok, *_ = tube_stage(slab, tc, st)
        if ok:
            print("C1B_SMOKE_FIRST_PASS", st[0]); return
    raise SystemExit("SMOKE_UNRESOLVED")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ledger-only", action="store_true")
    ap.add_argument("--smoke-slab", type=int)
    ap.add_argument("--tc", type=str)
    args = ap.parse_args()
    ctx.prec = BITS; base.ctx.prec = BITS
    if args.ledger_only:
        preflight(); return
    if args.smoke_slab is not None:
        if args.tc is None:
            raise SystemExit("--tc exact rational required for smoke")
        smoke(args.smoke_slab, Fraction(args.tc)); return
    raise SystemExit("FULL_DRIVER_NOT_YET_ENABLED: commit producer/checker pair before evidence run")


if __name__ == "__main__":
    main()
