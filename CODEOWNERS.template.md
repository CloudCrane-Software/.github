# CODEOWNERS.template.md —— 仓级 CODEOWNERS 模板（判官路径锁 @feasy898）

> **本件是模板，不是生效件。** 每个仓在**自己的仓根**放一份 `CODEOWNERS`
> （从下面「模板正文」复制，按仓裁剪路径段）。
>
> ★ **勿放 org 级**：org 级 `CODEOWNERS`（`.github` 仓根）会作用于组织下**所有**
>   仓，包括 platform 仓——本方案的判官路径锁只针对 af 黑灯工厂面，平台仓既有
>   漂移一律不碰（01-建设方案.md §二「判官面结构性保护」+ §八「platform 仓既有
>   漂移不碰」）。故：**仓级各挂一份，org 级禁用。**
>
> ★ **锁住 ≠ 拦住**：CODEOWNERS 须配合分支保护「Require review from Code Owners」
>   才生效（01-建设方案.md §五 P1：main 要求 PR + required check `gates` + 不
>   bypass）。生效后，工人 App 的 PR 改判官路径 = 必须 @feasy898 批准 = 工人
>   身份给不了 ⇒ **直接合不进去**（G-JUDGE 从「事后闸红」升级为「合不进去」）。

---

## 模板正文（复制到各仓根，改名 `CODEOWNERS`）

```gitignore
# =============================================================================
# CODEOWNERS —— 判官路径锁（仓级正本；org 级禁用：会波及 platform 仓）
#
# 判官路径 = 门禁脚本 + 判据件（定义见 .github 仓 docs/judge-paths.md）。
# 纪律：判官/门/判据件一改即拒收（rt-e82/83 双案）——改这些路径的 PR 被
#   保护规则拒，无评审例外；有意变更判据走裁决 + 同批重钉（gate_inputs_check
#   update / gate-pins-refresh），不走工人 PR。
# =============================================================================

# 默认兜底：全仓归 @feasy898（最严口径；仓内只放必要协作者时改这行）
* @feasy898
```

## 按仓裁剪示例

### af 仓（产品码；门禁件在 `ci/`，判据件同目录 + 仓根对账三件套）

```gitignore
# 门禁脚本族（ci/*.py / ci/*.sh：run.sh 十四步管道 + 各 checker + 门）
/ci/                              @feasy898
# 判分链判官件（k5-path-lint 黑名单：判分门本体 + report 判分脚本面）
/crates/af-execline/src/judge.rs  @feasy898
/af/packages/reportkit/           @feasy898
# 判据正本与对账面（gate_inputs_check.sh 的 GATE_INPUTS 族）
/ci/baselines/                    @feasy898
/proofs/rocq-规范库-v0/           @feasy898
/numbers.json                     @feasy898
/deliverables.yaml                @feasy898
/doc-claims.txt                   @feasy898
/rust-toolchain.toml              @feasy898
```

### factory-os 仓（工厂 OS 本体；tools/ 门禁脚本在役件 + 账本/波次/制度）

```gitignore
# 门禁脚本族（tools/ 全族：all-gates.sh、gate-pins.list 钉桩面、各门件与探针）
/tools/                           @feasy898
# 方法论锚点正本（anchor-check.py 消费面）
/计划/研究组/方法论批-20261031/     @feasy898
# 账本与波次清单、制度（append-only 证明面）
/账本/                            @feasy898
/波次清单/                        @feasy898
```

---

## 维护纪律

1. 判官路径清单以 `.github` 仓 `docs/judge-paths.md` 为唯一定义源；本模板的路径段
   从该清单派生，两处不一致 = 治理面漂移，同批修。
2. 新增判官路径 = 同批改：① 本模板（对应仓段）② `docs/judge-paths.md` ③ 相关
   门输入钉面（如 af 仓 `ci/baselines/gate-inputs.sha256`，经
   `bash ci/gate_inputs_check.sh update` 机生成重钉）。
3. 删路径段 = 摘锁，必须显式走评审（同「摘门保牌」纪律：静默删锁即红）。
