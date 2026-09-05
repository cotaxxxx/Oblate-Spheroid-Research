# External Judge receipt template — oblate boundary t-derivative

Status: `PENDING_JUDGE / NOT_BINDING`

This file is a receipt template only. The implementation actor must not insert a PASS verdict.

## Required pins

- request commit: `a439fe7cb983ac89134b2d03d253a0d6e89d5f74`
- audited source commit: `23cd08741ba797597c1d6ba9c74da41bdb66b1c4`
- producer blob SHA: `00e3986b728f6b21ddc42131c132585da568b830`
- checker blob SHA: `ae2b06659c657a1584c79e88c532ea2862726538`
- Actions run id: `33354706446`

## Scope

```text
t = 1 only
lambda in [5/8,33/50]
quantity = partial_t g_axis_ob(1,lambda)
claim = sign only
required sign = NEG
gating predicate = independent checker full-domain upper endpoint < 0
```

No point expectation, branch existence statement, monotone-tube statement, census identification, or off-axis claim is included in this receipt scope.

## Judge record fields

The external Judge record must include:

- judge/auditor identifier;
- audit date;
- the five pins above;
- confirmation that the scope is exactly the `t=1` sign claim stated above;
- symbolic correspondence verdict;
- producer/checker independence verdict;
- Actions receipt verification;
- final `PASS` or `FAIL`;
- exceptions or unresolved obligations, if any.

A PASS in an external Judge record does not by itself certify the later monotone tube or census identification.
