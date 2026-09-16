# ADR 0001: required approvals in a single-account organization

> **SUPERSEDED by ADR 0003 (2026-09-16)** — the merge-gate mechanism described
> below was removed by owner decision; auto-merge is now the principle.

## Context
Manual §3.2 requires `required_approving_review_count=1` (the human approves
every PR). GitHub structurally forbids PR authors from approving their own
PRs; this org has exactly one member who is also the author of every
agent-submitted PR.

## Decision
- Keep `required_approving_review_count=0` (setting 1 would deadlock every PR).
- Every public repo runs `.github/workflows/merge-gate.yml` on each PR: the
  job hangs on the `eval-gate` environment whose required reviewer is the
  owner, and `human-approval` is a REQUIRED status check. Merging is
  therefore impossible without a human click — the manual's intent, enforced.
- Combined with: strict status checks, no force pushes, linear history,
  admins included, CODEOWNERS human-owned eval assets.

## Consequences
- All agent PRs now wait for human environment approval before merge.
- If a second account/bot is added later, revisit and set the count to 1.
