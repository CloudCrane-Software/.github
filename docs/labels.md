# docs/labels.md —— label 分类法 = 状态机（org 治理面正本）

> 本分类法是 GitHub 板（issues）的**状态机**，与两套既有机器互为投影，不另立口径：
> - 波次执行器状态机（`tools/wave-runner.py`，制度-v1 §一）：
>   `queued→(占用闸)→dispatched→running→verifying→(绿)merge-check→merged→ledgered`；
>   任一步红 → `parked` + 异常队列。
> - 外派注册表统一态（`tools/dispatch-registry.py:9`）：
>   `queued → packaged → published → claimed → submitted → adjudicated → merged|rejected`。
>
> 使用纪律：
> 1. **单一状态标签**：一张卡同时只挂一个 `wave/*` 状态标签；转换 = 摘旧挂新
>    （与 registry 翻状态格同形态，不留双态）。
> 2. `legacy` / `blocked` 是叠加修饰位，可与状态标签共存（见下）。
> 3. 转换全部由确定性事件驱动（占用闸退出码、验收命令退出码+期望串、门裁决
>    GREEN/STALE_RED/RED），禁人工拍脑袋翻态；主代理只现身异常队列红件裁决。
> 4. 新建卡由 issue 表单自动落 `wave/queued`（`.github/ISSUE_TEMPLATE/card.yml`）。

---

## 状态标签定义与转换条件

### `wave/queued` —— 已登记待派

- **定义**：卡面九项字段齐备（task_id/债号/证据/验收命令集/pinned base/允许路径/
  禁项/内存预算/通道），已进板但未派工。registry 侧对应 `queued/packaged/published`。
- **进入**：issue 按 `card.yml` 新建（自动挂）；或 `running/verifying` 之前被
  占用闸拦下后重新排队（换锚债或登记新债行后）。
- **转出**：
  - → `wave/claimed`：占用闸放行（债号台账有行、无同锚并发、OOM 准入通过：
    anolis Σmem_budget ≤ 45G / 本机 ≈2G / gov ≤2G——制度-v1 §五）；
  - → `blocked`：占用闸 fail-closed BLOCK（台账无行的债号，制度-v1 §六.3）。

### `wave/claimed` —— 已认领施工中（占用闸内）

- **定义**：某通道（anolis-build / local-api / bot-lane / GLM-start-plan）已认领，
  占用闸持有中，施工进行时。registry 侧对应 `claimed`。
- **进入**：`queued` 占用闸放行。
- **转出**：
  - → `wave/running`：施工产物落盘（沙箱推分支 / runner 上开跑）；
  - → `wave/queued`：认领释放（异常回队，占用闸如实释放，禁 `--force-occupancy`）；
  - → `blocked`：施工面 fail-closed（如 bot-lane 发布被占用闸如实拦、换锚或登记新债行）。

### `wave/running` —— 验收命令执行中

- **定义**：卡面「验收命令集」正在执行（PR 上 `gates.yml` 作业链
  fmt → clippy → strategies_check → test → 专项门 在跑，或沙箱/收割 sweep 在跑）。
- **进入**：`claimed` 产物落盘并触发验收。
- **转出**：
  - → `wave/verifying`：命令全部退出码 0（或 bot 通道交卷待裁决，registry 侧
    `submitted/adjudicated`）；
  - → `blocked`：命令红（退出码非零 / 期望串缺）→ 同时按制度-v1 §一 落异常队列
    （runner 态 `parked`）。

### `wave/verifying` —— 判定与合线检查中

- **定义**：验收已收卷，处于确定性判定面：门裁决（GREEN / STALE_RED / RED）、
  merge-check 三分支范式（`--no-ff` 合入 → fmt+strategies+全量 test+clippy →
  FF push；退出码全 0）、 provenance 三要素核对。
- **进入**：`running` 命令全绿 / bot 通道交卷进入收割 sweep。
- **转出**：
  - → `wave/merged`：merge-check 退出码全 0 且自动合并发生（GREEN →
    audited-green-content 自动 absorb）；
  - → `wave/rejected`：RED / STALE_RED 且不可 absorb（含判官路径触碰被保护规则拒）；
  - → `blocked`：判定面自身不可证（缺件/坏 JSON/读数过期——按 rc=2 非零即红处理）。

### `wave/merged` —— 已合线

- **定义**：PR 已合入 pinned base（自动合并发生），git 历史即状态。registry 侧
  `merged`。
- **进入**：`verifying` merge-check 全绿。
- **转出**：
  - → （摘 `wave/merged`，归档关闭 issue）：落账完成（`ledgered`：回写范式——
    只翻状态格 + 行尾 append 依据句，`wc -l` 不变 + append-only opcodes 核验通过），
    或判定为纯内容卡无需落账格。

### `wave/rejected` —— 被拒收

- **定义**：验收红且不可 absorb，或触碰判官路径被 CODEOWNERS 保护规则直接拒
  （合不进去），或占用/内容漂移被裁决驳回。registry 侧 `rejected`。
- **进入**：`verifying` RED / STALE_RED；或合线前保护规则拒。
- **转出**：
  - → `wave/queued`：按裁决修订后重派（新卡面或同卡更新，重新过占用闸；
    如 RT-E117 类「已被拒」卡的重做路径）；
  - → `legacy`（叠加）：裁决认定不在关键路径、暂缓消化（01-建设方案.md §七）。

### `blocked` —— 阻塞（叠加修饰位）

- **定义**：当前步骤被 fail-closed 拦停，等待一个确定性解除条件。**不是终态**，
  与 `wave/queued/claimed/running/verifying` 叠加挂；runner 侧同形态落异常队列
  （`parked`）。
- **典型触发**：占用闸 BLOCK（台账无债行）；判官路径触碰；判据漂移
  （gate_inputs 钉面 / gate-pins 钉桩失配）；OOM 准入拒绝；读数过期（死手断言）。
- **转出**：解除条件达成（登记债行 / 换锚 / 同批重钉 / 运营者裁决）后回到对应
  状态标签；整点巡检 cron 只扫异常队列 + 饱和度，绿件零打扰（制度-v1 §一）。

### `legacy` —— 遗留（叠加修饰位）

- **定义**：历史遗留、暂缓消化、**不在关键路径上**的卡（01-建设方案.md §七：
  本地 af clone 两波滞后修复、g10 重做（RT-E117 已被拒）、swev-pool 扩容、
  feeder 观察、tools .bak 清理（可选）等）。
- **进入**：新规划裁定 / `rejected` 转暂缓 / 旧系统迁入板面。
- **转出**：由本地 harness 按异常队列节奏消化（P5 后），消化 = 回到正常状态标签
  重新走机；legacy 只是优先级修饰，不豁免任何门。

---

## 转换总图（一屏版）

```text
                    ┌──────────────────────────────────────────────┐
                    │                 wave/queued                 │
                    │  （卡面齐备待派；占用闸/OOM 准入前置）        │
                    └──────┬───────────────────────┬──────────────┘
              占用闸放行    │                       │ 占用闸 BLOCK
                           ▼                       ▼
                    ┌─────────────┐         （叠加 blocked）
                    │ wave/claimed│◄────────────────┐
                    └──────┬──────┘  认领释放        │
                   产物落盘 │                         │
                           ▼                         │
                    ┌─────────────┐   命令红          │
                    │ wave/running│───────────────┐  │
                    └──────┬──────┘               │  │
                   命令全绿 │                      ▼  │
                           ▼                （叠加 blocked + 异常队列）
                    ┌─────────────┐   红/不可吸收   │
                    │wave/verifying│────────────┐  │
                    └──────┬──────┘             │  │
              merge-check绿 │                   ▼  ▼
                           ▼            ┌─────────────┐
                    ┌─────────────┐     │wave/rejected│──修订重派──▶ queued
                    │ wave/merged │     └──────┬──────┘
                    └──────┬──────┘            │ 暂缓（叠加）
                    落账完成 │                  ▼
                           ▼            （叠加 legacy）
                         归档
```

## 与判官路径的联动（红线）

- `wave/rejected` 的常见成因之一是判官路径触碰——这不是普通的验收红，而是
  CODEOWNERS 保护规则的**结构性拒绝**（合不进去）。此类卡的重派必须先把改动
  移出判官路径，或走「判据变更 = 裁决 + 同批重钉」的正路（见 `docs/judge-paths.md`），
  禁用工人的普通 PR 通道硬闯。
