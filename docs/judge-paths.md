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
| `.github/workflows/gates.yml` | PR 验收门接线件（required check `gates` 上下文；内联五步剖面：fmt --check＋K5 路径 lint／clippy -D warnings（R09 禁降级成基线门）／af-dsl+af-compiler 快速测试／判据面自检恒跑；F2 全量门不走 Actions=R11）。**L2 合流级全门剖面升级在飞：af#5/#6 open 未合线（2026-11-06 回读），本行按 live main=9c6f0544 实况录，未照抄研究稿终态** | af/.github/workflows/gates.yml 头注（raw 实读 2026-11-06） |

> `ci/` 门码面被 `ci/fix_verify.py` 机制③自动纳入逐树双核对账（提交面 oid +
> 工作树面 sha256）：门码被删/被改弱 ⇒ 该既有门红（机器面，非人工自觉）。
>
> af 切 org 门（`uses: CloudCrane-Software/.github/.github/workflows/ci-gates.yml@main`）
> 终态待后段合线后另批更新（编排面称 af#20；2026-11-06 回读 af 仓 issue 20 = 404 未建）。

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
| `tools/test-manifest.list` | PR 门剖面① py_compile 件数下限判据源（`#L1_PY_COUNT_MIN` 声明现读；下限不写死在门内防第二真源，RT-E84③ 删件并同步改声明也红） | factory-os/.github/workflows/gates.yml:161-180（all-gates.sh:644 同款读法；raw 实读 2026-11-06） |
| `tools/mirror-scan-allowlist.json` | PR 门剖面② bot-scrub 树扫豁免面（判据件：pattern/file/reason/expires 四键缺一不认；**行钉**——条目带 line 必与命中行同号，行漂移不豁免；expires 2026-12-05 到期不复审整体失效回红=有意设计的时间炸弹，factory-os#2/D-72） | factory-os/.github/workflows/gates.yml:286-310、头注:33-44（raw 实读 2026-11-06） |
| `tools/test-ledger-migration-recon.py` | PR 门剖面③ 账本迁移对账门判别力自证（`--selftest` 内嵌夹具 25 例含 tamper 反例；无参实跑判据面在仓外 ⇒ PR 面只验判别力） | factory-os/.github/workflows/gates.yml:401-411（raw 实读 2026-11-06） |
| `.github/workflows/gates.yml` | PR 门接线件（五步剖面：分工声明／检出 PR 头树／①py_compile 全量 tools/＋件数下限对账／②bot-scrub 树扫 fail-closed，扫描内核=mirror-disclose.sh 内嵌 scan_text() 经 AST 切取复用／③对账判别力自证）；作业名恒 `gates`=分支保护 required check 上下文。注：factory-os 仓级 CODEOWNERS 实况未单列此行（af 实况有列 `/​.github/workflows/gates.yml`）——派生缺口如实记录，留 factory-os 侧批修 | factory-os/.github/workflows/gates.yml:87-112（raw 实读 2026-11-06） |
| `tools/swev-judge-v2.py` 及同族三件（`swev-judge-v2-zero-scan.py`／`swev-judge-v2-replay.py`／`swev-judge-v2-selftest.py`） | swev 判分链判官件族：v2 判分器本体（D-32 三缺陷修复版，判分门）+ 零状态普查/交付回放/正反例自测三伴件（改任一件=改判分判据面） | tools/swev-judge-v2.py 头注（D-32/红队裁决 R4/R5/R7）；三伴件头注同源 |
| `tools/card-selfcontainment-check.py`、`tools/dispatch-occupancy-check.py` | 派前三闸两件机检本体：审卡闸（六要件自包含，RULE_TABLE sha256 与 planner step 08 互钉）／占用闸（防双解占用；登记前 BLOCK fail-closed） | tools/card-selfcontainment-check.py 头注（Q1 §3.1；D-97=factory-os#30）；tools/dispatch-occupancy-check.py 头注 |
| `计划/研究组/方法论批-20261031/anchor-check.py` 及方法论正本 | 方法论锚点常驻门（锚点漂移即时红；改锚即改正本） | tools/all-gates.sh:940 |
| `账本/`、`波次清单/*.md`、制度文档 | append-only 证明面/制度面（回写范式：只翻状态格+行尾 append）。波次清单锁面=**`*.md` 口径**（制度-v1.md 等制度/草稿文档），与 factory-os 仓级 CODEOWNERS 实况逐字对齐 | 制度-v1 §三落账路；factory-os CODEOWNERS:33/:47（2026-11-06 实读） |

> **波次清单 `*.md` 口径修正（2026-11-06 P4，是修正不是弱化）**：`/波次清单/wave-*.json`
> （manifest）移出判官锁——manifest 是规划产物，planner 环定时产→推 planner/&lt;wave&gt;
> 分支→开 PR→gates 绿后 squash 合线（两段式）；若锁 `/波次清单/` 整目录，planner 自动
> PR 触碰即需 code owner 批准 ⇒ 0 批准自动合线不成立、规划环首波卡死。判据件定义不变
> （tools/ 门本体、账本三件套、制度文档）；后续若 manifest 被赋予判据属性，回锁须同批
> 重钉并登记依据。出处：factory-os 仓级 `CODEOWNERS:39-47`（实读）。
>
> **裁 9 补条（2026-11-07，运营者准；是补名不是扩权）**：M-4 判官面判定从「双源
> （CODEOWNERS 实读派生 ∪ 本登记表静态族）」改**单源=本登记表点名单**（双源时代
> CODEOWNERS 源把 `/tools/` 整树判官面化，误拦首张真卡 `tools/disk-waterline-carrier.py`
> 等非登记表路径；今日 57+ 张 tools/ PR 经标准流合线实证）。按「判据只许变严以
> 登记表点名单+补条方式满足」纪律，同批补名四类公认判官件：swev 判分链判官件族
> （v2 本体+零状态普查/回放/自测三伴件）与派前三闸两件机检本体（审卡闸/占用闸）
> ——此前仅靠 CODEOWNERS 派生进场，单源后不点名即丢判官面识别。factory-os 侧
> `JUDGE_STATIC_FACTORYOS` 常量同批补名（门本体两件），planner step 08 M-4 与
> 审卡闸双镜同步；`tools/swev-judge-v2*.py` 由关键词族 `judge` 命中（无需补名即红）。
>
> 出处注（仓外工作区面，非判官路径）：`计划/…/anchor-check.py` 与对账门无参判据面
> （逃逸问题台账.md 等）为仓外工作区件——factory-os 仓内无该路径，仓级 CODEOWNERS
> 实况不锁空路径；门本体消费位（all-gates.sh:940）在 `/tools/` 锁内。

---

## 三、.github 仓（org 治理面）

| 路径 | 作用 | 依据 |
|---|---|---|
| `.github/workflows/gates.yml` | org 可复用验收工作流正本（workflow_call `special_gates` 点选；作业链 fmt→clippy→strategies_check→test→专项门 ledger/anchor/otel = af F2 全量门 Actions 形态；调用方先 checkout，零外部 action） | .github/workflows/gates.yml 头注（本仓实读 2026-11-06） |
| `.github/workflows/ci-gates.yml` | org 可复用 CI 门（第一批六门，workflow_call；门0 铸 runner 判别机；A-1 退出码语义／A-3 钉桩双消费面对账失配即红不执行／A-4 登记↔执行双向绑定／A-7 判别力负向自测／A-8 真空求值防护／A-9 死手断言）。入参默认 `tools/ci-gates-manifest.list`／`tools/ci-gates-pins.list`／`tools/ci-gates-criteria` 为**调用仓侧**消费位（判据件随调用仓，不属本仓清单） | .github/workflows/ci-gates.yml:1-107（本仓实读；selftest 实跑 exit 0=基线绿+5 变异全红，2026-11-06） |
| `tools/ci-gates-selftest.py` | ci-gates.yml 静态自检＋变异负控件（A-7 自体应用：M1 删门步／M2 插吞红／M3 权限翻转／M4 删 workflow_call／M5 插外部 action 各必红并点名；本地可机判，不依赖 Actions 执行面） | tools/ci-gates-selftest.py:1-35（本仓实读） |

> org 仓根 CODEOWNERS 实况=`* @feasy898` 全局兜底（本仓 CODEOWNERS:5）——上列三件
> 与本清单皆在锁内；af/factory-os 两仓实况则裁剪为「只锁判官路径、无兜底行」（各仓
> CODEOWNERS 头注明示有意裁剪）。仓外研究稿/暂存树（30-工件/、staging/）只作出处注，
> 不入判官路径清单。

---

## 四、「写不进去」保护规则（五层，机器面非人工自觉）

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
