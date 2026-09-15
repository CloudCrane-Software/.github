# CloudCrane-Software

A one-person software company. Every public repository in this organization is part of
a governance system and a library of composable capability assets.

**How we work**

- Development is performed by AI coding agents. Humans own goals and acceptance — nothing else.
- Every external action passes through an action gateway that binds four things to each
  action: authorization (mandate → grant), budget (reservation), lease (fencing epoch)
  and evidence. No action is an untracked side effect.
- Every capability is an immutable asset: `SKILL.md + spec/ + eval/ + evidence/` (signed).
  Reuse requires evidence digest match; agent memory is never authority.
- Eval gates are independent of the implementation. Thresholds change only through
  human-approved PRs. Product code and eval assets are never modified in the same change.

**Repositories**

| Repo | Role |
|---|---|
| [`kernel`](https://github.com/CloudCrane-Software/kernel) | Governance kernel monorepo — six-table ledger, OPA policies, action gateway, reconciler |
| [`platform`](https://github.com/CloudCrane-Software/platform) | Deployment & docs — compose stack, Caddy reverse proxy, server scripts, ADRs |
| [`skills`](https://github.com/CloudCrane-Software/skills) | Capability assets — spec + eval + signed evidence per capability |
| [this repo](https://github.com/CloudCrane-Software/.github) | Org-level configuration — templates and reusable workflows |

**Protocol in one sentence** — executors are one-shot, sandboxed, authorized, budgeted
and lease-fenced; they complete engineering actions inside an evidence-and-rules loop,
cannot self-authorize, cannot exceed scope, and cannot grade their own exam.
