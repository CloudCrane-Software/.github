# docs/judge-paths.md —— 判官路径清单与「写不进去」保护规则

> **判官路径 = 门禁脚本 + 判据件**：改了它们 = 改了门本身。纪律红线（rt-e82/83
> 双案，制度-v1 §六.4）：**判官/门/判据件一改即拒收**。
>
> 本清单是判官路径的唯一定义源；`CODEOWNERS.template.md` 的路径段、卡面禁项、
> PR 自检清单均从这里派生。三处不一致 = 治理面漂移，同批修。

---

## 一、af 仓（产品码）

### 1.1 门禁脚本族（`ci/` 全族）

| 路径 | 作用 | 依据 |
|---|---|---|
| `ci/run.sh` | 十四步验收管道正本（fmt/clippy/test/…/step14） | af/ci/run.sh 头注 |
| `ci/gate_inputs_check.sh` | 门输入全集 sha256 钉对账（fail-closed） | af/ci/gate_inputs_check.sh:29-31 |
| `ci/provenance_check.sh` | step3 溯源门（共享 target 跨工作树假绿防护） | af/ci/run.sh:228-237 |
| `ci/clippy_gate.py` | clippy 警告基线门 | af/ci/run.sh:224-225 |
| `ci/k5-path-lint.py` | 判分链路径 lint（黑名单逐件 sha256 对锚） | af/ci/run.sh:219-220 |
| `ci/strategies_check.py` | 策略库全量校验（schema+index 计数+编译断言） | af/ci/run.sh:603-613, :658 |
| `ci/branches_check.py` / `ci/xcheck.py` / `ci/criteria_check.py` | step14 机读一致性三件（14a/14b/14c） | af/ci/run.sh:648-656 |
| `ci/harness_regression_gate.py` | harness 版本级回归门（14e） | af/ci/run.sh:614-622, :660 |
| `ci/fix_scan.py` / `ci/arm_wiring_check.py` / `ci/budget_cast_lint.py` | step13 横切与对称三机制 | af/ci/run.sh:589-594 |
| `ci/neutrality_gate.sh` / `ci/neutrality_scan.py` | 中立性门（step8） | af/ci/run.sh:385-387 |
| `ci/mutation_runner.sh` | mutations 元探针（注册表漂移/全量演练） | af/ci/run.sh:134, :194-210 |
| `ci/baseline_calc.sh` | 9a/9b 基线机算（verify-kani/verify-rocq） | af/ci/run.sh:492-495 |
| `ci/fix_verify.py` | 跨树收口门（机制③「门族全集单源」） | af/ci/gh_workflow_check.py:59-64 |
| `ci/gh_workflow_check.py` | GitHub 端 PR 反馈面静态自检器（F1 判据面） | af/ci/gh_workflow_check.py 头注 |
| `ci/step10/11/12_check.py`、`ci/task_package_manifest_check.py` 等其余 `ci/*.py` / `ci/*.sh` | 各 step 门本体 | af/ci/run.sh 全文 |
| `.github/workflows/f1.yml` | F1 快速门（判据面自检 step 恒跑 gh_workflow_check.py） | af/ci/gh_workflow_check.py:58-60 |

> `ci/` 门码面被 `ci/fix_verify.py` 机制③自动纳入逐树双核对账（提交面 oid +
> 工作树面 sha256）：门码被删/被改弱 ⇒ 该既有门红（机器面，非人工自觉）。

### 1.2 判据件（GATE_INPUTS 全集，af/ci/gate_inputs_check.sh:41-72）

| 路径 | 消费门 |
|---|---|
| `ci/neutrality-expected-fail.txt` / `ci/neutrality-wordlist.txt` / `ci/neutrality-golden-registry.tsv` | 中立性门（gate_inputs_check.sh:42-44） |
| `ci/scorechain-manifest.txt` | k5-path-lint（判分链登记表） |
| `ci/clippy-baseline.txt` | clippy_gate |
| `ci/arm-wiring.yaml` / `ci/branches.yaml` / `ci/criteria.yaml` / `ci/fix-scan.yaml` / `ci/budget-cast-whitelist.json` | 各 checker（arm_wiring_check.py:41 等） |
| `ci/debt-register.md` | arm_wiring_check.py:42 / budget_cast_lint（债册镜像） |
| `ci/subgates.list` | step14 子门全集正本（step12 名册绑定 + xcheck 子门级断言） |
| `ci/baselines/harness-regression-set.json` / `ci/baselines/harness-regression-tasks.json` | harness 回归门定义面（D-54） |
| `ci/baselines/kani-inv-harness.manifest` | 9b Kani 基线对账（run.sh:492-496） |
| `proofs/rocq-规范库-v0/theorems-manifest.txt` | 9a 定理清单对账（run.sh:431-456） |

**钉面（判据的判据，同锁）**：`ci/baselines/gate-inputs.sha256`（update 机生成、
禁手改）、`ci/baselines/mutations-registry.sha256`、`ci/baselines/clippy-baseline.sha256`、
`ci/baselines/task-package-writepoints.json`。

### 1.3 判分链判官件（k5 黑名单）

`crates/af-execline/src/judge.rs`（判分门本体）+ `af/packages/reportkit/` 包内
全部 `*.py`（report 判分脚本面：citation/rubric/render 三件）——黑名单定义与
下界自派生规则见 af/ci/k5-path-lint.py 头注。

### 1.4 仓根对账三件套与钉住件

`numbers.json`（计数复算正本）、`deliverables.yaml`（承诺-交付对账）、
`doc-claims.txt`（自述-实现对账）、`rust-toolchain.toml`（工具链钉住）。

---

## 二、factory-os 仓（工厂 OS 本体）

| 路径 | 作用 | 依据 |
|---|---|---|
| `tools/` 全族门脚本 | all-gates.sh（L1-L6 统一门）及各门件/探针（ledger/anchor/otel 专项门族等） | tools/all-gates.sh 头注；:919-969、:940、:1097-1100、:1230-1239 |
| `tools/gate-pins.list` | 门本体钉桩面（权威值外置；门本体/子探针/钉值三面绑定） | tools/gate-pins.list 头注 |
| `tools/gate-pins-refresh.sh` | 钉桩重锚唯一入口（改门/改探针/改钉值后必跑） | tools/gate-pins.list 维护契约 |
| `计划/研究组/方法论批-20261031/anchor-check.py` 及方法论正本 | 方法论锚点常驻门（锚点漂移即时红；改锚即改正本） | tools/all-gates.sh:940 |
| `账本/`、`波次清单/`、制度文档 | append-only 证明面（回写范式：只翻状态格+行尾 append） | 制度-v1 §三落账路 |

---

## 三、「写不进去」保护规则（五层，机器面非人工自觉）

1. **合不进去（结构性拒绝）**：仓级 CODEOWNERS 把上列路径锁 `@feasy898` +
   分支保护「Require review from Code Owners」（01-建设方案.md §二、§五 P1）。
   工人 App 的 PR 改判官路径 = 必须 @feasy898 批准 = 工人身份给不了 ⇒
   **直接合不进去**。G-JUDGE 从「事后闸红」升级为「合不进去」。
   org 级 CODEOWNERS 禁用（会波及 platform 仓）——仓级各挂一份。
2. **改判据即改门（钉面 fail-closed）**：判据正本逐件 sha256 钉于
   `ci/baselines/gate-inputs.sha256`；漂移/缺件/摘钉/钉外多行/漏造册一律红
   （gate_inputs_check.sh:22-28）。tools/ 面对应 gate-pins.list 钉桩：改门本体 /
   改子探针 / 改钉值三者任一未重锚即红（tools/gate-pins.list:10-18）。
3. **摘门保牌红线**：登记行与执行由 `ci/xcheck.py` gates-exec-binding 双向绑定
   （af/ci/run.sh:636-641）——删执行留登记行即红；门本体缺失显式红、不进 SKIP
   （tools/all-gates.sh 头注状态语义）；`ci/subgates.list` 名册被静默增删即钉漂移红。
4. **门失效自曝**：mutations 元探针 + 全量演练（run.sh step0）——探针被删/改即红；
   演练红 = 被测门未失败于删除/弱化 = 门失效（run.sh:186-210）。
5. **判据面自检**：`.github/workflows/f1.yml` 判据面自检 step 恒跑
   `gh_workflow_check.py`——谁把 PR 反馈面判据改弱，同一次 PR run 即红。

**有意变更判官路径的唯一正路**：运营者裁决 → 同批改判据/基线 + 机生成重钉
（`bash ci/gate_inputs_check.sh update` / `bash tools/gate-pins-refresh.sh`）+
登记依据（同批评审提交）→ 过 @feasy898 审批合入。工人通道禁行此路。
