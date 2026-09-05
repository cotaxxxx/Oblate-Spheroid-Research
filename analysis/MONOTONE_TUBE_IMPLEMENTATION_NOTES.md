# Monotone tube implementation notes

Status: `PROTOTYPE_PLANNING / NOT_AUDITED / NOT_BINDING`

The fixed contract is `analysis/MONOTONE_TUBE_CONTRACT.md`.

Implementation must not intervalize the raw general-t formula across the north-pole corner `(s,t)=(0,1)`, because the naive `q` interval can contain zero. The next implementation step is therefore to derive a corner-regular expression from the exact identities in the contract before any Arb run is treated as meaningful.

The moving internal `gamma=1` locus is handled by the inherited factorized `u` chart. This is separate from the north-pole corner issue.

No PASS claim is authorized by this planning note.
