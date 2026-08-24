# Research Rules

Applies to all repositories and working files of this project.
These rules are normative. Where a rule and a convenience conflict, the rule wins.

---

## 1. Evidence classes

Every quantity, file, and statement carries exactly one class.

| Class | Meaning |
|---|---|
| `DIAGNOSTIC_ONLY` | Exploratory. Floating point, scans, plots, continuations. |
| `NOT_BINDING` | May not be cited as support for any claim in a manuscript. |
| `PROTOTYPE` | Code that runs but has not been audited. |
| `NOT_AUDITED` | Fixed source, no independent audit yet. |
| `AUDITED_SOURCE` | Independently audited source at a fixed hash. |
| `CERTIFIED` | Clean-room produced certificate with complete dependency chain. |

`CERTIFIED` is forbidden until the entire chain is present. There is no
partial `CERTIFIED`.

## 2. Derivation class of every number

No numeric constant is recorded without its derivation class:

- `EXACT` — closed form, with the closed form written next to it.
- `CERTIFIED_ENCLOSURE` — interval with a certificate reference.
- `HIGH_PRECISION` — multiprecision evaluation, with dps and quadrature stated.
- `FLOAT` — double precision.
- `EXTRAPOLATED` — inferred from other data, with the source data named.

`EXTRAPOLATED` values are never used as brackets, seeds for uniqueness
arguments, or reproduction targets without restating their class at the point
of use. An extrapolated value that is later computed directly is replaced, not
annotated.

## 3. Two-layer certification

Local execution produces candidate evidence only. The sole authoritative path
is a clean-room run that regenerates every artifact from committed code and
fixed configuration. No locally generated data enters that run.

An artifact that cannot be attributed to a fixed source hash is outside the
proof path, regardless of whether its contents look correct.

## 4. Producer and auditor are different actors

The party that implements does not certify. The party that audits does not
write to the implementation branch. Simultaneous writes to the same branch or
the same file are forbidden.

Before any tag push, the artifact is independently verified.

## 5. Expectations precede implementation

Control values are fixed and committed before the evaluator that will be
tested against them exists. A control is never regenerated, overwritten, or
adjusted by the evaluator it constrains.

A test that does not exercise the implementation is not a control. Name it so
that it cannot be mistaken for one.

## 6. Precision invariant

The checker reconstructs enclosures at precision greater than or equal to the
precision used by the producer. This is enforced in code, not by convention.

## 7. Scope of a claim

A certificate certifies exactly what its conclusion sentence says, on exactly
the parameters it names. It does not extend to neighbouring parameters, to the
general case, or to the theorem the work is aimed at.

A search that detects no additional object is not a nonexistence proof. It is
recorded with its domain, mesh, arithmetic, stopping criteria, and unresolved
cells, and it is classed `DIAGNOSTIC_ONLY`.

## 8. Analytic and machine obligations are separate

Statements requiring proof (regularity, uniform asymptotics, interchange of
limits, real analyticity) are never included in a machine conclusion. They are
listed as named lemmas with their own status, and the machine certificate
records that it does not establish them.

Singular limits of a parameter are separate obligations and are excluded from
any finite-window claim.

## 9. Provenance

A reconstruction is a new object. It is committed under a new name and a new
hash and never presented as the original. Equivalence to a lost original is
claimed only through explicit regression against fixed external anchors.

Failures are kept: timeouts, rejected runs, mismatches, and unresolved
incidents remain in the record. Nothing is deleted to make the history read
better.

## 10. Naming

Every quantity specific to one case carries a case marker. Bare symbols that
exist in more than one case are forbidden as file stems, function names, and
serialization keys.

## 11. Stopping

When a required input is missing, unexpanded, or ambiguous, work stops. The
missing item is recorded. Nothing is inferred to fill the gap, and no
placeholder is committed that could later be mistaken for a determination.

## 12. Machine assistance

Output from any automated assistant is candidate evidence at best. It is
audited on the same terms as any other contribution.

An assertion that some term, result, or convention is established requires a
citation. An uncited claim of established usage is treated as unsupported and
removed.

Responsibility for every statement in a manuscript rests with the author,
irrespective of how the statement was produced. Where computation is part of
a proof, the manuscript states what was computed, by what method, and what
remains assumed.

## 13. Publication discipline

Diagnostic material does not enter a manuscript as support. Where a diagnostic
motivated a direction, it is described as such.

The scope of a paper is fixed before writing, and claims that depend on
obligations assigned to a later paper are not made in an earlier one.
