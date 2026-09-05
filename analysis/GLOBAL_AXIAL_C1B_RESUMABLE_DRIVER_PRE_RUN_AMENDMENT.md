# C1b resumable external-driver pre-run amendment

Status: `PREDECLARED_AMENDMENT / IMPLEMENTATION_NOT_STARTED / MACHINE_NOT_RUN / NOT_BINDING`

This amendment is committed before implementation of resumability or parallel external execution. It adds driver, ledger, resume, calibration, and receipt rules to the existing C1b contract stack. It does not alter any C1b mathematical gate, exact domain, predictor rule, tube width, clamp, corner treatment, T/E stage, root-localization rule, refinement rule, precision, strict-sign predicate, or work ceiling.

No implementation under this amendment may be used as evidence until the implementation receives a chat raw audit and all post-audit source/blob pins are fixed in a later pin commit.

## 1. Change boundary and kernel isolation

The permitted implementation change is limited to the external driver and persistence layer.

The following are kernel and must remain mathematically and computationally unchanged:

```text
density formulae
ordinary/corner chart selection
series/direct threshold and series degree
recurrences and tails
exact box-partition arithmetic
interval integration arithmetic
strict-sign predicates
T0/T1/T2 and E0/E1/E2 numerical gates
root localization and predictor-acceptance predicates
```

Before the first resumable run, the producer and checker C1b kernels must be extracted into separate lineage-specific modules by code movement only:

```text
producer/global_axial_c1b_kernel.py
checker/global_axial_c1b_kernel.py
```

The producer kernel may not import the checker kernel, and the checker kernel may not import the producer kernel. Each extracted kernel blob must be pinned after chat raw audit. The audit must verify that extraction is move-only relative to the pinned full-source pair:

```text
producer ancestor blob = e5927feb52561a79af909efbec04ea9baafdfdfb
checker ancestor blob  = f8b842c96d5ef5cec540752758cc377444b472b1
```

Any semantic kernel edit requires a new pre-run amendment and a new raw audit. Hash equality of the audited extracted kernel blobs is the binding kernel-immutability check for every segment and resume.

## 2. Separate append-only ledgers

Producer and checker run as independent processes in separate run directories and use separate ledgers:

```text
<producer-run-dir>/ledger.jsonl
<checker-run-dir>/ledger.jsonl
```

Neither lineage may read, import, copy, or derive runtime state from the other lineage's ledger, logs, checkpoints, predictor choices, certified roots, or completion status. Cross-lineage comparison occurs only after both lineages have independently completed.

Each ledger is append-only UTF-8 JSON Lines. Existing bytes may never be rewritten, truncated, reordered, or normalized in place.

### 2.1 Canonical record and hash chain

Every JSON object must be serialized for hashing with:

```text
UTF-8
json.dumps(..., sort_keys=True, separators=(",",":"), ensure_ascii=True)
no insignificant whitespace
exact rationals encoded as canonical "p/q" strings, including denominator 1
Arb values encoded as {"mid":"...","rad":"...","upper":"..."} with decimal strings
JSON float values forbidden in every record
```

Each record contains:

```text
sequence
record_type
prev_sha256
payload
record_sha256
```

For the first record, `prev_sha256` is 64 ASCII zeroes. For every later record it equals the preceding record's `record_sha256`.

`record_sha256` is SHA-256 of the canonical JSON serialization of

```text
{sequence, record_type, prev_sha256, payload}
```

with the `record_sha256` field omitted. Startup verification must recompute the complete chain from byte 0. Any parse error, sequence gap, hash mismatch, duplicate sequence, trailing partial line, or unexpected record type is an immediate launch refusal and makes that ledger `NOT_EVIDENCE`.

### 2.2 Header record

The first record is exactly one `header`. Its payload records at least:

```text
lineage = producer or checker
exact git HEAD and ref
clean-tree result
parent contract blob
all C1b amendment blobs
B_ob contract/amendment/receipt blobs
driver blob
lineage-specific kernel blob
requirements-prototype and requirements-interval blobs
downloaded wheel filenames and SHA-256 hashes
Python executable and full version
pip version and pip freeze --all
mpmath and python-flint versions
precision, degree, u-series threshold
all predictor/T/root/E stage declarations
all per-stage, per-attempt, accepted, attempted, and global work ceilings
CPU model / lscpu summary
OS / uname / os-release
UTC creation time
canonical-JSON and hash-chain version
```

The header is immutable for the lifetime of the ledger.

The pin manifest must not contain an expected `head` field. A manifest commit
cannot truthfully pin its own commit hash. Exact HEAD continuity is instead
recorded by `identity.head` in the immutable ledger header and enforced on
every resume by equality of all immutable header fields. The manifest still
pins the branch `ref`, clean tree, wheels, environment, and source blobs.

The source-blob set is exactly the following seven paths; the manifest itself
must not appear in `expected_blobs`:

```text
analysis/c1b_resumable_driver.py
producer/global_axial_c1b_gating.py
checker/global_axial_c1b_gating.py
producer/global_axial_c1b_kernel.py
checker/global_axial_c1b_kernel.py
producer/global_axial_c1b_producer.py
checker/global_axial_c1b_checker.py
```

### 2.3 Segment records

Every process start appends `segment_begin`; every graceful process end appends `segment_end`. Their payloads record:

```text
segment index
UTC start/end
reason = completed / requested_stop / failure
HEAD, clean-tree, blob, requirement, wheel, toolchain, precision, stage, and budget recheck result
cumulative completed work on entry/exit
next exact slab identity
```

### 2.4 Attempt and slab records

Before numerical work on any attempted slab, append `attempt_begin` with:

```text
attempt sequence
coarse index and refinement depth
exact lambda endpoints
continuation source and previous-root enclosure
cumulative work before attempt
```

A terminal `slab_record` records at least:

```text
attempt sequence
coarse index and refinement depth
exact lambda endpoints
predictor P0/P1/P2 steps and outcome
exact t_c and predictor mode
certified T_* enclosure
left/right clamp state
T0/T1/T2 attempted stages, unresolved counts, worst boxes and worst uppers
E0/E1/E2 attempted stages, unresolved counts, worst boxes and worst uppers
root-localization result and sup|t_c-T_*|
accept/refine/abort decision
exact child slabs when refined
corner_hull count
per-component and total work
cumulative work after the attempt
```

Only a terminal `slab_record` may advance the exact lambda ledger or update `previous_root`.

Optional `work_checkpoint` records may be appended after a complete declared stage solely to account for work. They may not be used to resume within a slab.

## 3. Resume and refusal rules

At startup, if a ledger exists, the driver must:

1. verify the full JSONL parse and hash chain;
2. compare every header pin and environment field against the current repository, wheel set, interpreter, package set, precision, stages, and budgets;
3. verify the current tree is clean;
4. reconstruct completed slab order, exact lambda adjacency, refinement tree, cumulative work, and last accepted certified root solely from terminal ledger records;
5. refuse launch on any mismatch.

A successful comparison is appended in the new `segment_begin`. One failed comparison is permanently `NOT_EVIDENCE`; deleting or replacing the failed ledger to obtain a pass is forbidden.

A ledger containing a terminal `slab_record` with `decision = ABORT` is not
resumable. That run is failed and remains `NOT_EVIDENCE`; any later attempt
must use a new, previously nonexistent `RUN_DIR`. An ABORT ledger may not be
deleted, truncated, copied, or relabelled as a resumable ledger.

Completed slabs are never recomputed. An attempt having `attempt_begin` but no terminal `slab_record` is interrupted and is discarded in full. No interval, stage, box queue, partial sum, predictor scan, or root-localization state from that attempt may be reused. The exact slab is restarted from its beginning.

The slab order is fixed in increasing lambda order, including deterministic left-child-before-right-child refinement. The continuation `previous_root` is read only from the last accepted terminal `slab_record`; it is not recomputed on resume.

### 3.1 Interrupted-work accounting

All work before interruption counts against the cumulative ceilings.

For a graceful requested stop, the driver appends exact completed-stage work and the partial attempt's known work before exit.

For an ungraceful interruption, the exact partial-stage work may be unknowable. On resume, every unmatched `attempt_begin` is therefore charged conservatively at the full declared per-attempt gating ceiling plus the full predictor-scan ceiling before that slab is restarted. This charge is appended as an `interrupted_attempt_charge` record. It counts toward global attempted work but does not advance the slab ledger.

Every appended `attempt_begin`, including one interrupted before a terminal `slab_record`, consumes one unit of `MAX_ATTEMPTED_SLABS=2100`. Restarting the discarded slab consumes another attempt unit. Repeated interruption of the same exact slab therefore consumes the attempted-slab cap and eventually forces `UNRESOLVED`; it may not be collapsed into one logical attempt.

No interruption may reduce cumulative work or reset an attempted-slab count. Ceiling checks include all prior segments, all `attempt_begin` records, completed attempts, graceful partial work, conservative interruption charges, and the current segment.

## 4. Producer/checker concurrency

Producer and checker may run sequentially or concurrently after this amendment is implemented and pinned.

Concurrent execution is permitted only when:

```text
separate OS processes
separate run directories
separate append-only ledgers
separate logs and temporary files
no shared writable state
no reading of the other lineage's ledger or output
independent resource ceilings
```

Parallel execution does not change the checker independence statement. Cross-lineage comparison is a post-run operation and may begin only after both final ledgers end in successful completion records.

## 5. Receipt additions

The final C1b receipt must additionally record:

```text
driver and extracted-kernel blobs for both lineages
ledger filenames, byte sizes, final record hashes, and complete-ledger SHA-256 hashes
number of segments and interruptions per lineage
every segment UTC start/end and termination reason
every resume pin/environment comparison result
every interrupted-attempt work charge
cumulative work carried across segments
final exact slab union and refinement lineage reconstructed from the ledgers
producer/checker post-completion comparison
```

If any resume comparison fails, either hash chain fails, an existing ledger is rewritten, an interrupted slab is partially reused, or a shared runtime state is detected, the affected lineage and combined receipt are `NOT_EVIDENCE`.

The receipt must state that the producer and checker gating modules are
byte-identical transcription copies. Their runtime independence consists of
separate processes, directories, ledgers, and writable state; their substantive
numerical independence resides in the separately audited 160-bit producer and
192-bit checker kernel modules. Parsed trace fields are receipt diagnostics
only. The gating decision is the kernel's returned `ok` value and must not be
recomputed, strengthened, weakened, or overridden from parsed trace text.

## 6. Preflight estimates and calibration

Before a full run, the driver must print and append to the header:

```text
140-coarse-slab exact ledger
T0/E0 early-pass work estimate
T2/E2 no-refinement work estimate
absolute accepted/attempted safety ceilings
predictor-scan work shown separately
estimated wall time for one lineage and for the selected sequential/concurrent plan
```

The obsolete parent ceiling `3,015,704,576` may not be reported as the active C1b ceiling. The active amended ceilings remain:

```text
accepted gating ceiling = 26,387,415,040
global attempted gating ceiling = 49,476,403,200
predictor scan work = separately accumulated
```

Before the C1b evidence run, execute the pinned C1c machine calculation on the external host as `DIAGNOSTIC / NOT_C1B_EVIDENCE` to measure panel-evaluation throughput. Record its HEAD, blobs, exact evaluation count, UTC duration, CPU/toolchain, and derived evaluations per second. The calibration may estimate time only; it may not change any C1b stage, gate, budget, or acceptance rule.

If the resulting selected execution plan is expected to exceed the available uninterrupted operating window, the resumable driver must be used. An estimate may not be converted into evidence.

Before the external host's environment is written into the pin manifest, run
`lscpu | head -20` twice in the intended execution environment and compare the
two byte streams. They must match. If a volatile line (for example, a scaling
frequency) is present, the exact exclusion rule and retained-line ordering must
be declared in a committed amendment before the manifest is created; it may not
be chosen after observing a resume mismatch.

## 7. Audit and pin order

The mandatory order is:

```text
1. commit this pre-run amendment;
2. implement kernel extraction and resumable drivers;
3. chat raw audit the driver diff and verify move-only kernel extraction;
4. commit post-audit driver/kernel/blob pins;
5. run pinned C1c calibration as DIAGNOSTIC;
6. emit and review both C1b pre-run headers;
7. start the full producer/checker run;
8. compare completed ledgers and construct the machine receipt.
```

No full C1b run started before step 4 is evidence under this amendment.
