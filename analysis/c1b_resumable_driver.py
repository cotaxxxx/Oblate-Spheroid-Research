#!/usr/bin/env python3
"""Non-mathematical persistence and accounting for resumable C1b runs.

This module deliberately does not import a numerical package. Its public data
boundary consists of integers, strings, Fractions, lists, and dictionaries.
Lineage code owns every numerical predicate and decides what work to report.
"""
from __future__ import annotations

import hashlib
import importlib.metadata
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

PINS_PATH = Path("analysis/GLOBAL_AXIAL_C1B_RESUMABLE_PINS.json")
CHAIN_VERSION = "C1B_JSONL_CHAIN_V1"
ZERO_HASH = "0" * 64
REQUIRED_C1B_BLOB_PATHS = (
    "analysis/c1b_resumable_driver.py",
    "producer/global_axial_c1b_gating.py",
    "checker/global_axial_c1b_gating.py",
    "producer/global_axial_c1b_kernel.py",
    "checker/global_axial_c1b_kernel.py",
    "producer/global_axial_c1b_producer.py",
    "checker/global_axial_c1b_checker.py",
)
PINNED_ENVIRONMENT_FIELDS = (
    "python_executable",
    "python_version",
    "pip_version",
    "pip_freeze_all",
    "packages",
    "platform",
    "uname",
    "lscpu_head",
    "os_release",
)


def utc_now():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def run_text(args):
    return subprocess.run(args, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()


def rational_text(value):
    if not isinstance(value, Fraction):
        raise TypeError(type(value))
    return f"{value.numerator}/{value.denominator}"


def fraction_from_text(text):
    if not isinstance(text, str):
        raise TypeError(type(text))
    return Fraction(text)


def no_float(obj, path="$"):
    if isinstance(obj, float):
        raise TypeError(f"JSON float forbidden at {path}")
    if isinstance(obj, dict):
        for key, value in obj.items():
            no_float(value, f"{path}.{key}")
    elif isinstance(obj, (list, tuple)):
        for index, value in enumerate(obj):
            no_float(value, f"{path}[{index}]")


def canonical_bytes(obj):
    no_float(obj)
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def hash_payload(sequence, record_type, prev_sha256, payload):
    body = {
        "sequence": sequence,
        "record_type": record_type,
        "prev_sha256": prev_sha256,
        "payload": payload,
    }
    return hashlib.sha256(canonical_bytes(body)).hexdigest()


class Ledger:
    def __init__(self, path):
        self.path = Path(path)
        self.records = []
        self.last_hash = ZERO_HASH
        if self.path.exists():
            self._load_verify()

    def _load_verify(self):
        data = self.path.read_bytes()
        if data and not data.endswith(b"\n"):
            raise SystemExit("LEDGER_TRAILING_PARTIAL_LINE")
        previous = ZERO_HASH
        for expected, raw in enumerate(data.splitlines()):
            try:
                record = json.loads(raw.decode("utf-8"))
            except Exception as exc:
                raise SystemExit(f"LEDGER_PARSE_FAIL {expected}: {exc}")
            if record.get("sequence") != expected:
                raise SystemExit(f"LEDGER_SEQUENCE_FAIL {expected}")
            if record.get("prev_sha256") != previous:
                raise SystemExit(f"LEDGER_PREV_HASH_FAIL {expected}")
            expected_hash = hash_payload(
                expected, record.get("record_type"), previous, record.get("payload")
            )
            if record.get("record_sha256") != expected_hash:
                raise SystemExit(f"LEDGER_RECORD_HASH_FAIL {expected}")
            previous = expected_hash
            self.records.append(record)
        self.last_hash = previous

    def append(self, record_type, payload):
        sequence = len(self.records)
        record_hash = hash_payload(sequence, record_type, self.last_hash, payload)
        record = {
            "sequence": sequence,
            "record_type": record_type,
            "prev_sha256": self.last_hash,
            "payload": payload,
            "record_sha256": record_hash,
        }
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("ab") as handle:
            handle.write(canonical_bytes(record) + b"\n")
            handle.flush()
            os.fsync(handle.fileno())
        self.records.append(record)
        self.last_hash = record_hash
        return record


def git_blob(path):
    return run_text(["git", "hash-object", path])


def environment_snapshot(pin_spec):
    blobs = {path: git_blob(path) for path in sorted(pin_spec["blob_paths"])}
    try:
        lscpu = run_text(["lscpu"]).splitlines()[:20]
    except Exception:
        lscpu = []
    freeze = run_text([sys.executable, "-m", "pip", "freeze", "--all"]).splitlines()
    packages = {}
    package_names = pin_spec.get("package_names", ["mpmath", "python-" + "fl" + "int"])
    for name in package_names:
        try:
            packages[name] = importlib.metadata.version(name)
        except importlib.metadata.PackageNotFoundError:
            packages[name] = "MISSING"
    wheels = {}
    wheel_dir = Path(pin_spec["wheel_dir"])
    if wheel_dir.is_dir():
        for path in sorted(wheel_dir.iterdir()):
            if path.is_file():
                wheels[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    os_release_path = Path("/etc/os-release")
    os_release = os_release_path.read_text(encoding="utf-8").splitlines() \
        if os_release_path.is_file() else []
    return {
        "head": run_text(["git", "rev-parse", "HEAD"]),
        "ref": run_text(["git", "rev-parse", "--abbrev-ref", "HEAD"]),
        "clean_status": run_text(["git", "status", "--porcelain=v1"]),
        "blobs": blobs,
        "expected_blobs": pin_spec["expected_blobs"],
        "python_executable": sys.executable,
        "python_version": sys.version,
        "pip_version": importlib.metadata.version("pip"),
        "pip_freeze_all": freeze,
        "packages": packages,
        "platform": platform.platform(),
        "uname": platform.uname()._asdict(),
        "lscpu_head": lscpu,
        "os_release": os_release,
        "wheel_sha256": wheels,
    }


def verify_identity(identity, pin_spec):
    failures = []
    if "head" in pin_spec:
        failures.append("SELF_REFERENTIAL_HEAD_PIN")
    if identity["ref"] != pin_spec["ref"]:
        failures.append("REF")
    if identity["clean_status"] != "":
        failures.append("DIRTY_TREE")
    required_blob_paths = set(REQUIRED_C1B_BLOB_PATHS)
    if set(pin_spec.get("blob_paths", ())) != required_blob_paths:
        failures.append("BLOB_PATH_SCHEMA")
    if set(pin_spec.get("expected_blobs", {})) != required_blob_paths:
        failures.append("EXPECTED_BLOB_SCHEMA")
    if identity["blobs"] != pin_spec.get("expected_blobs"):
        failures.append("BLOBS")
    if identity["wheel_sha256"] != pin_spec["wheel_sha256"]:
        failures.append("WHEELS")
    expected_environment = pin_spec.get("expected_environment")
    if not isinstance(expected_environment, dict):
        failures.append("EXPECTED_ENVIRONMENT_MISSING")
    else:
        missing = [key for key in PINNED_ENVIRONMENT_FIELDS
                   if key not in expected_environment]
        extra = sorted(set(expected_environment) - set(PINNED_ENVIRONMENT_FIELDS))
        if missing or extra:
            failures.append("EXPECTED_ENVIRONMENT_SCHEMA")
        else:
            for key in PINNED_ENVIRONMENT_FIELDS:
                if identity.get(key) != expected_environment[key]:
                    failures.append("ENV_" + key.upper())
    if failures:
        raise SystemExit("PIN_IDENTITY_FAIL " + ",".join(failures))


def load_pins():
    if not PINS_PATH.exists():
        return None
    return json.loads(PINS_PATH.read_text(encoding="utf-8"))


def resume_state(records):
    """Recover persistence facts; lineage code reconstructs mathematical state."""
    attempted = 0
    accepted_work = 0
    global_work = 0
    accepted = []
    terminal = []
    terminal_attempts = set()
    charged_attempts = set()
    begun = set()
    for record in records:
        kind = record["record_type"]
        payload = record["payload"]
        if kind == "attempt_begin":
            attempted += 1
            begun.add(payload["attempt_sequence"])
        elif kind == "interrupted_attempt_charge":
            charged_attempts.add(payload["attempt_sequence"])
            global_work += int(payload["charged_work"])
        elif kind == "slab_record":
            terminal_attempts.add(payload["attempt_sequence"])
            terminal.append(payload)
            work = int(payload["result"]["work_total"])
            global_work += work
            if payload["decision"] == "ACCEPT":
                accepted.append(payload)
                accepted_work += work
            elif payload["decision"] not in ("REFINE", "ABORT"):
                raise SystemExit("LEDGER_BAD_DECISION")
    return {
        "attempted": attempted,
        "accepted_work": accepted_work,
        "global_work": global_work,
        "accepted": accepted,
        "terminal": terminal,
        "unmatched": sorted(begun - terminal_attempts - charged_attempts),
    }


def check_ceiling(value, ceiling, label):
    if not isinstance(value, int) or not isinstance(ceiling, int):
        raise TypeError("budget values must be integers")
    if value > ceiling:
        raise SystemExit(label)


def within_ceiling(value, ceiling):
    if not isinstance(value, int) or not isinstance(ceiling, int):
        raise TypeError("budget values must be integers")
    return value <= ceiling


def next_segment_index(records):
    return sum(record["record_type"] == "segment_begin" for record in records)
