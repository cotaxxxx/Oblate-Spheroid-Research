STATUS: PRE_RUN_AMENDMENT / BINDING (C1b preflight only)
PARENT: GLOBAL_AXIAL_C1B_RESUMABLE_DRIVER_PRE_RUN_AMENDMENT.md
SCOPE: canonicalization of the CPU identity block used by the pin
manifest. No gating mathematics, caps, ledger rules, or certified
objects are modified.

1. CAPTURE. The CPU identity capture is the first 20 lines of
   `LC_ALL=C lscpu`. Two captures are taken. Raw captures are
   stored verbatim in the preflight record as evidence and are
   never edited.

2. EXCLUSION RULE. A line is EXCLUDED iff its key (the text
   before the first ':' with surrounding whitespace stripped)
   is exactly one of:
       "CPU(s) scaling MHz"
       "CPU MHz"
   No other exclusion is permitted. Regex matching is not used.

3. CANONICAL FORM. CANONICAL_CPU_ID = the non-excluded lines,
   byte-for-byte, in original order. The manifest hashes the
   canonical form only.

4. PINNED KEY ORDER. EXPECTED_KEY_ORDER is the ordered list of
   keys of CANONICAL_CPU_ID, extracted from the preserved
   preflight record 20260905T133118Z (raw capture SHA-256
   7658e3555abb00f745db61b565baf1a869a58b2413b786f8931f4d9975caca85)
   and embedded verbatim below as committed bytes:       [
         "Architecture",
         "CPU op-mode(s)",
         "Address sizes",
         "Byte Order",
         "CPU(s)",
         "On-line CPU(s) list",
         "Vendor ID",
         "Model name",
         "CPU family",
         "Model",
         "Thread(s) per core",
         "Core(s) per socket",
         "Socket(s)",
         "Stepping",
         "Frequency boost",
         "CPU max MHz",
         "CPU min MHz",
         "BogoMIPS",
         "Flags"
       ]
   EXPECTED_EXCLUDED = exactly one line, key "CPU(s) scaling MHz".

5. CHECKS (all fail-closed, before manifest creation):
   (a) the two canonical forms are byte-identical;
   (b) the key order equals EXPECTED_KEY_ORDER;
   (c) the excluded set equals EXPECTED_EXCLUDED (count and key).   Any deviation, including a changed lscpu layout or an
   unexpected volatile key, aborts preflight.

6. NON-RETROACTIVITY. The preserved preflight record
   20260905T133118Z is historical and is not reinterpreted.
   A fresh preflight record is started after this amendment
   is committed.
