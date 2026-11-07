<!-- PR 五段模板（组织级默认模板，源: CloudCrane-Software/.github）。
     依据《建设方案-多Agent系统与GitOps》（PROP-0001）第 5 节开发工作流：
     提案 → 评审 → 灰度 → 融入；环境即交接物；门禁程序控制；失败现场保留。
     五段全部填写才可进入合并；门禁证据必须来自程序输出，不接受口头声称。

     【合流说明】本件由两套模板合并而成（合流 commit 见 git log，理由写在该
     commit body）：
       · 五段骨架（1 提案 / 2 评审 / 3 门禁证据 / 4 灰度 / 5 融入与失败现场）
         = 远端既有的 PROP-0001 五段式，逐字保留，未删未改；
       · af 黑灯工厂面字段 = 本仓治理面合流件，按语义并入对应段，不另起炉灶：
           §1 提案     ← 关联 issue（task_id / 债号 / 通道 / pinned base）
           §2 评审     ← 改动面（允许路径对账）+ 判官路径零改动声明
           §3 门禁证据 ← 验收命令实跑结果（命令 / 退出码 / 期望串）
           §5 融入     ← 归因（Co-Authored-By）+ 自检清单
     依据：30-工件/GitHub协作平面-建设方案/01-建设方案.md §二（per-task 身份与
     归因）、30-工件/波次自转器-20261106/制度-v1.md §三（自动收卷四路：绿判据 =
     命令退出码 + 期望串）。 -->

## 1. 提案（Propose）

<!-- 动机、目标与取舍；一句话"为什么现在做"。 -->
- 动机与目标：
- 关联工单 / ADR（WO-xxxx、docs/adr/xxxx）：
- 方案条款依据（PROP-0001 §）：

<!-- af 面：关联 issue——卡面 task_id / 债号原样抄录，便于看板与台账对账；
     `Closes #<issue 号>` 由施工卡 issue 表单（.github/ISSUE_TEMPLATE/card.yml）
     开出，af 产品仓按卡面九项字段填。 -->
- Closes #
- task_id：
- 债号（debt）：
- 通道（channel）：<!-- anolis-build / local-api / bot-lane / GLM-start-plan -->
- pinned base：

## 2. 评审（Review）

<!-- 影响面自查；边界与决策点核对（PROP-0001 §0.4 / §4.9：凡可能有两个决策点的，必须收敛为一个）。 -->
- 影响面（代码 / 配置 / 环境 / 数据）：
- 决策点核对（是否引入第二个决策点？边界归谁）：
- 环境即交接物（环境/配置变更落在哪个文件、哪个仓库）：

<!-- af 面：改动面——与卡面「允许路径」逐条对账；越界即拒收。 -->
- 允许路径（抄卡面）：
- 实际改动文件：

<!-- af 面：判官路径零改动声明。判官路径 = 门禁脚本 + 判据件，唯一定义源见
     `docs/judge-paths.md`。判官/门/判据件一改即被仓级 CODEOWNERS 保护规则拒收
     （合不进去），无评审例外（rt-e82/83 双案，制度-v1 §六.4）。 -->
- [ ] 本 PR 未触碰任何判官路径（清单见 `docs/judge-paths.md`）。

## 3. 门禁证据（Gate Evidence）

<!-- 程序控制的门禁：GuardrailRun 结果、CI 三层（L1/L2/L3）、测试命令与结论。
     贴命令与关键输出（不得含任何密钥值）；UNKNOWN 不得作为终态。 -->
- GuardrailRun / CI 结果：
- 命令与关键输出：

<!-- af 面：验收命令实跑结果——逐条抄卡面「验收命令集」：命令 + 退出码 + 期望串。
     Gates 工作流（fmt → clippy → strategies_check → test → 专项门）结果附在 PR
     checks（调用方 `uses: CloudCrane-Software/.github/.github/workflows/
     gates.yml@main`）；本表贴的是卡面点名的专项验收，两者不互相替代。
     期望串不出现 = 红，不进合线。 -->

| # | 命令（逐字） | 退出码 | 期望串 | 结果 |
|---|---|---|---|---|
| 1 |  |  |  | ⬜ |
| 2 |  |  |  | ⬜ |

<details><summary>实跑输出（尾部片段）</summary>

```bash
# 粘贴各命令尾部输出（含 SUMMARY/PASS 行）
```

</details>

## 4. 灰度（Canary）

<!-- 灰度范围、观察指标、自动回退条件；不需要灰度时写明理由。 -->
- 范围与观察指标：
- 回退条件：

## 5. 融入与失败现场（Integrate & Failure Site）

<!-- 合并后动作（文档/配置/下游同步）；回滚路径；若中途失败：失败现场保留位置（日志/复现步骤）。 -->
- 合并后动作：
- 回滚路径：
- 失败现场保留（如适用）：

<!-- af 面：归因——per-task 身份（01-建设方案.md §二）：App installation token
     推分支 + Co-Authored-By trailer。PR 作者 = App bot = 审计线；
     trailer 认领施工人。 -->
Co-Authored-By: <!-- 姓名 <邮箱> -->

<!-- af 面：自检清单 -->
- [ ] 卡面九项字段（task_id/债号/证据/验收命令集/pinned base/允许路径/禁项/内存预算/通道）与 issue 一致
- [ ] 无 secret 入 git（指纹+路径 only）
- [ ] 未 force push / 未 reset --hard / 未动历史记录
- [ ] 落账坐标（ledger）已填，待合线后按「只翻状态格 + 行尾 append 依据句」回写
- [ ] 无 workaround：解法循惯例、未来 agent 只凭仓内材料可懂（铁律 4）
