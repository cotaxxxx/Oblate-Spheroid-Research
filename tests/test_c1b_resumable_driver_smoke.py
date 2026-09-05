#!/usr/bin/env python3
"""Calculation-free end-to-end smoke tests for the C1b resumable driver."""
from __future__ import annotations

import copy
import tempfile
import unittest
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from analysis import c1b_resumable_driver as persistence
from checker import global_axial_c1b_gating as checker_gating
from producer import global_axial_c1b_gating as gating


@dataclass(frozen=True)
class StubSlab:
    coarse: int
    depth: int
    ll: Fraction
    lr: Fraction

    def children(self):
        middle = (self.ll + self.lr) / 2
        return (
            StubSlab(self.coarse, self.depth + 1, self.ll, middle),
            StubSlab(self.coarse, self.depth + 1, middle, self.lr),
        )


class StubKernel:
    BITS = 160
    DEG = 50
    USTAR = Fraction(3, 5)
    L_LO = Fraction(0)
    L_HI = Fraction(1)
    N_COARSE = 1
    MAX_DEPTH = 0
    MAX_ACCEPTED = 1
    MAX_ATTEMPTED = 3
    T_STAGES = (("T0", 1, 1, 1),)
    ROOT_STEPS = 1
    ROOT_LBOXES = 1
    ROOT_PANELS = 1
    E0_TBOXES = 1
    E0_LBOXES = 1
    E_STAGES = (("E0", 1),)
    PRED_SCAN_PANELS = 1
    ATTEMPT_WORK_CEILING = 10
    ACCEPTED_WORK_CEILING = 10
    GLOBAL_ATTEMPT_WORK_CEILING = 2000
    ctx = SimpleNamespace(prec=0)
    base = SimpleNamespace(ctx=SimpleNamespace(prec=0))
    calls = 0

    @classmethod
    def coarse_ledger(cls):
        return [StubSlab(0, 0, cls.L_LO, cls.L_HI)], True

    @classmethod
    def preflight(cls):
        return None

    @classmethod
    def attempt(cls, slab, previous_root):
        cls.calls += 1
        root = (Fraction(1, 2), Fraction(1, 2))
        record = {
            "mode": "STUB",
            "tc": Fraction(1, 2),
            "root": root,
            "left_clamp": False,
            "right_clamp": False,
            "corner_hull": 0,
            "tube_stage": "T0",
            "sup_error": Fraction(0),
            "pieces": [("TUBE", Fraction(0), Fraction(1))],
        }
        work = {"predictor": 1, "tube": 1, "root": 1, "exterior": 1}
        return True, record, root, Fraction(1, 2), work, "PASS"


def identity():
    blobs = {path: "b" * 40 for path in persistence.REQUIRED_C1B_BLOB_PATHS}
    return {
        "head": "a" * 40,
        "ref": "smoke",
        "clean_status": "",
        "blobs": blobs,
        "expected_blobs": blobs,
        "python_executable": "/usr/bin/python3",
        "python_version": "3.smoke",
        "pip_version": "smoke",
        "pip_freeze_all": ["stub==1"],
        "packages": {"stub": "1"},
        "platform": "smoke-platform",
        "uname": {"system": "smoke"},
        "lscpu_canonical": "d" * 64,
        "os_release": ["NAME=smoke"],
        "wheel_sha256": {"stub.whl": "c" * 64},
    }


def pins(snapshot):
    return {
        "ref": snapshot["ref"],
        "blob_paths": list(persistence.REQUIRED_C1B_BLOB_PATHS),
        "expected_blobs": snapshot["blobs"],
        "wheel_dir": "unused",
        "wheel_sha256": snapshot["wheel_sha256"],
        "expected_environment": {
            key: copy.deepcopy(snapshot[key])
            for key in persistence.PINNED_ENVIRONMENT_FIELDS
        },
    }


class C1BResumableSmoke(unittest.TestCase):
    def setUp(self):
        StubKernel.calls = 0
        gating._stop_requested = False
        checker_gating._stop_requested = False
        self.snapshot = identity()
        self.manifest = {
            "producer": pins(self.snapshot),
            "checker": pins(self.snapshot),
        }

    def run_driver(self, run_dir, module=gating, lineage="producer"):
        with mock.patch.object(persistence, "load_pins", return_value=self.manifest), \
             mock.patch.object(persistence, "environment_snapshot",
                               return_value=copy.deepcopy(self.snapshot)):
            module.run_full(StubKernel, lineage, run_dir)

    def test_fresh_end_to_end_and_completed_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            producer_dir = Path(directory) / "producer"
            checker_dir = Path(directory) / "checker"
            self.run_driver(producer_dir)
            self.run_driver(checker_dir, checker_gating, "checker")
            self.assertEqual(StubKernel.calls, 2)
            ledger = persistence.Ledger(producer_dir / "ledger.jsonl")
            self.assertEqual(
                [record["record_type"] for record in ledger.records],
                ["header", "segment_begin", "attempt_begin", "slab_record", "segment_end"],
            )
            self.run_driver(producer_dir)
            self.run_driver(checker_dir, checker_gating, "checker")
            self.assertEqual(StubKernel.calls, 2, "completed slab was recomputed")

    def test_unmatched_attempt_is_charged_and_restarted(self):
        with tempfile.TemporaryDirectory() as directory:
            ledger = persistence.Ledger(Path(directory) / "ledger.jsonl")
            ledger.append(
                "header",
                gating.header_payload(
                    StubKernel, "producer", self.manifest["producer"], self.snapshot
                ),
            )
            ledger.append("attempt_begin", {
                "attempt_sequence": 1,
                **gating.slab_payload(StubKernel.coarse_ledger()[0][0]),
                "previous_root": None,
                "cumulative_work_before": 0,
                "utc": persistence.utc_now(),
            })
            self.run_driver(directory)
            ledger = persistence.Ledger(Path(directory) / "ledger.jsonl")
            charge = [record for record in ledger.records
                      if record["record_type"] == "interrupted_attempt_charge"]
            self.assertEqual(len(charge), 1)
            self.assertEqual(charge[0]["payload"]["charged_attempt_unit"], 1)
            final = [record for record in ledger.records
                     if record["record_type"] == "segment_end"][-1]["payload"]
            self.assertEqual(final["attempted"], 2)

    def test_identity_and_header_mismatches_refuse_resume(self):
        changed_head = copy.deepcopy(self.snapshot)
        changed_head["head"] = "d" * 40
        persistence.verify_identity(changed_head, self.manifest["producer"])
        bad = copy.deepcopy(self.snapshot)
        bad["python_version"] = "changed"
        with self.assertRaisesRegex(SystemExit, "ENV_PYTHON_VERSION"):
            persistence.verify_identity(bad, self.manifest["producer"])
        with tempfile.TemporaryDirectory() as directory:
            self.run_driver(directory)
            original_degree = StubKernel.DEG
            StubKernel.DEG += 1
            try:
                with self.assertRaisesRegex(SystemExit, "RESUME_HEADER_CONTRACT_MISMATCH"):
                    self.run_driver(directory)
            finally:
                StubKernel.DEG = original_degree

    def test_arb_record_has_both_directed_endpoints(self):
        self.assertEqual(
            gating.arb_decimal_record("[1.25 +/- 0.05]"),
            {"mid": "1.25", "rad": "0.05", "lower": "1.20", "upper": "1.30"},
        )


if __name__ == "__main__":
    unittest.main()
