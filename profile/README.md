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

**af 黑灯工厂协作平面（本仓治理面）**

这里是 af 黑灯工厂的协作平面：`.github` 仓承载 org 级治理面（label 分类法、施工卡/PR 模板、可复用 `gates.yml` 验收工作流），`factory-os` 是工厂 OS 本体（门禁脚本在役件、账本、波次清单、制度），`af` 是产品码；一次规划、自派自收，验收/合线/落账全部确定性，本地只处理异常与生产面。

治理面正本（均在本仓，随合流落入）：

| 件 | 作用 |
|---|---|
| `.github/ISSUE_TEMPLATE/card.yml` | 施工卡 issue 表单——九项字段自包含，禁项置顶 |
| `.github/PULL_REQUEST_TEMPLATE.md` | PR 五段模板（五段骨架 + af 面字段） |
| `.github/workflows/gates.yml` | 可复用验收工作流：fmt → clippy → strategies_check → test → 专项门 |
| `docs/labels.md` | label 分类法 = GitHub 板状态机（`wave/*` 状态标签 + `blocked`/`legacy` 修饰位） |
| `docs/judge-paths.md` | 判官路径清单与「写不进去」保护规则（唯一定义源） |
| `CODEOWNERS.template.md` | 仓级 CODEOWNERS 模板（判官路径锁；org 级禁用，避免波及 platform 仓） |

**Protocol in one sentence** — executors are one-shot, sandboxed, authorized, budgeted
and lease-fenced; they complete engineering actions inside an evidence-and-rules loop,
cannot self-authorize, cannot exceed scope, and cannot grade their own exam.
