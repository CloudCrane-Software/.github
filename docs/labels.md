# docs/labels.md —— label 分类法 = 状态机（org 治理面正本）

> 本分类法是 GitHub 板（issues）的**状态机**，与两套既有机器互为投影，不另立口径：
> - 波次执行器状态机（`tools/wave-runner.py`，制度-v1 §一）：
>   `queued→(占用闸)→dispatched→running→verifying→(绿)merge-check→merged→ledgered`；
>   任一步红 → `parked` + 异常队列。
> - 外派注册表统一态（`tools/dispatch-registry.py:9`）：
>   `queued → packaged → published → claimed → submitted → adjudicated → merged|rejected`。
>
> **正本口径（2026-11-06 D-79 批对齐在役）**：状态机标签 = `state:*` 五态
> （`state:queued→state:running→state:verifying→state:merged|state:rejected`）。
> 旧版 `wave/*` 七态词汇（含 `wave/claimed`）自本批起废弃，见下「废弃注记与对照表」；
> 收敛方向 = 正本对齐在役，**禁反向**把三板改成 `wave/*` 七态（planner 按在役口径
> 校验、fail-closed——Q1 M-8 实证）。
>
> 使用纪律：
> 1. **单一状态标签**：一张卡同时只挂一个 `state:*` 状态标签；转换 = 摘旧挂新
>    （与 registry 翻状态格同形态，不留双态）。
> 2. `legacy` / `blocked` 是叠加修饰位，可与状态标签共存（见下）。
> 3. 转换全部由确定性事件驱动（占用闸退出码、验收命令退出码+期望串、门裁决
>    GREEN/STALE_RED/RED），禁人工拍脑袋翻态；主代理只现身异常队列红件裁决。
> 4. 新建卡入场两路：planner 机建卡自动落 `state:queued`（`factory-os
>    .github/workflows/planner.yml:113`，状态机起点）；issue 表单模板
>    （`.github/ISSUE_TEMPLATE/card.yml`）当前仍落 `wave/queued`——该漂移在册
>    （改 card.yml 不属 D-79 卡 allowed_paths），随后续治理卡对齐；对齐前表单建的卡
>    以 `state:queued` 为准补挂。
> 5. `quality:*` / `perm/requested` / `ticket:*` 同为叠加/申请族位（见下定义），
>    **不占状态格**、不当状态标签用；其挂/摘同样由确定性事件驱动（机评落定、
>    申请评论、机检/终审裁决、回收动作），翻态纪律同 1/3。
> 6. `wave`（裸标签）与 `wave-NN` 是**波次归属标签**，只作检索/归波清点
>    （planner step10 清点逻辑按 `wave`/`wave-NN` 前缀，在役），不参与状态机。

---

## 状态标签定义与转换条件（在役五态）

### `state:queued` —— 已登记待派

- **定义**：卡面九项字段齐备（task_id/债号/证据/验收命令集/pinned base/允许路径/
  禁项/内存预算/通道），已进板但未派工。registry 侧对应 `queued/packaged/published`；
  runner 侧 `queued`。
- **进入**：planner 机建卡自动落（`planner.yml:113`）；或在途施工被占用闸拦下后
  重新排队（换锚债或登记新债行后）。
- **转出**：
  - → `state:running`：占用闸放行**且执行代理认领开工**（开卡翻牌，见「执行代理
    label 翻转范式」；放行判据原样保留：债号台账有行、无同锚并发、OOM 准入通过：
    anolis Σmem_budget ≤ 45G / 本机 ≈2G / gov ≤2G——制度-v1 §五）；
  - → `+blocked`（叠加）：占用闸 fail-closed BLOCK（台账无行的债号，制度-v1 §六.3）。

### `state:running` —— 已认领施工中（占用闸内）

- **定义**：执行代理已认领、占用闸持有中，覆盖从施工产物落盘到验收命令收卷的
  全程。吸收旧七态的 `wave/claimed`（认领段）与 `wave/running`（验收执行段）两格
  ——标签粒度对齐在役五态，细分不丢、由 registry/runner 态格继续承载（registry 侧
  `claimed`；runner 侧 `dispatched`+`running`）。
- **进入**：`state:queued` 占用闸放行 + 代理认领（开卡翻牌）。
- **转出**：
  - → `state:verifying`：验收命令全部退出码 0（期望串齐）；或 bot 通道交卷待裁决
    （registry 侧 `submitted/adjudicated`）；
  - → `+blocked`（叠加）+异常队列：验收命令红（退出码非零 / 期望串缺）或施工面
    fail-closed（runner 态 `parked`，制度-v1 §一）；认领异常释放则回
    `state:queued`（占用闸如实释放，禁 `--force-occupancy`）。

### `state:verifying` —— 判定与合线检查中

- **定义**：验收已收卷，处于确定性判定面：门裁决（GREEN / STALE_RED / RED）、
  merge-check 三分支范式（`--no-ff` 合入 → fmt+strategies+全量 test+clippy →
  FF push；退出码全 0）、provenance 三要素核对。runner 侧 `verifying`+`merge-check`；
  registry 侧 `submitted/adjudicated`。
- **进入**：`state:running` 验收命令全绿 / bot 通道交卷进入收割 sweep。
- **转出**：
  - → `state:merged`：merge-check 退出码全 0 且自动合并发生（GREEN →
    audited-green-content 自动 absorb）；
  - → `state:rejected`：RED / STALE_RED 且不可 absorb（含判官路径触碰被保护规则拒）；
  - → `+blocked`（叠加）：判定面自身不可证（缺件/坏 JSON/读数过期——按 rc=2
    非零即红处理）。

### `state:merged` —— 已合线

- **定义**：PR 已合入 pinned base（自动合并发生），git 历史即状态。registry 侧
  `merged`。
- **进入**：`state:verifying` merge-check 全绿（合线翻牌）。
- **转出**：
  - → （摘 `state:merged`，归档关闭 issue）：落账完成（`ledgered`：回写范式——
    只翻状态格 + 行尾 append 依据句，`wc -l` 不变 + append-only opcodes 核验通过），
    或判定为纯内容卡无需落账格。

### `state:rejected` —— 被拒收

- **定义**：验收红且不可 absorb，或触碰判官路径被 CODEOWNERS 保护规则直接拒
  （合不进去），或占用/内容漂移被裁决驳回。registry 侧 `rejected`；runner 侧红件
  `parked` 裁决驳回。
- **进入**：`state:verifying` RED / STALE_RED；或合线前保护规则拒；或异常队列
  红件裁决驳回（驳回翻牌）。
- **转出**：
  - → `state:queued`：按裁决修订后重派（新卡面或同卡更新，重新过占用闸；
    如 RT-E117 类「已被拒」卡的重做路径）；
  - → `+legacy`（叠加）：裁决认定不在关键路径、暂缓消化（01-建设方案.md §七）。

### `blocked` —— 阻塞（叠加修饰位）

- **定义**：当前步骤被 fail-closed 拦停，等待一个确定性解除条件。**不是终态**，
  与 `state:queued/running/verifying` 叠加挂；runner 侧同形态落异常队列
  （`parked`）。
- **典型触发**：占用闸 BLOCK（台账无债行）；判官路径触碰；判据漂移
  （gate_inputs 钉面 / gate-pins 钉桩失配）；OOM 准入拒绝；读数过期（死手断言）。
- **转出**：解除条件达成（登记债行 / 换锚 / 同批重钉 / 运营者裁决）后回到对应
  状态标签；整点巡检 cron 只扫异常队列 + 饱和度，绿件零打扰（制度-v1 §一）。

### `legacy` —— 遗留（叠加修饰位）

- **定义**：历史遗留、暂缓消化、**不在关键路径上**的卡（01-建设方案.md §七：
  本地 af clone 两波滞后修复、g10 重做（RT-E117 已被拒）、swev-pool 扩容、
  feeder 观察、tools .bak 清理（可选）等）。
- **进入**：新规划裁定 / `state:rejected` 转暂缓 / 旧系统迁入板面。
- **转出**：由本地 harness 按异常队列节奏消化（P5 后），消化 = 回到正常状态标签
  重新走机；legacy 只是优先级修饰，不豁免任何门。

---

## 执行代理 label 翻转范式（2026-11-06 D-79 收编）

执行代理（施工面 subagent / worker）在卡生命周期内的翻牌动作只有三个，**全部由
确定性事件触发**（使用纪律 3 原文有效，本段不新增任何人工翻态口）：

| 触发事件（确定性判据） | 翻转动作 | 时点 |
|---|---|---|
| **开卡（认领）**：占用闸放行（退出码 0）+ 执行代理开工 | 摘 `state:queued` 挂 `state:running` | 认领开工时点 |
| **合线**：merge 动作 API 回读成功（merge-check 全绿 / 门 GREEN 后 PUT merge 2xx） | 摘在途状态挂 `state:merged` | 合线时点 |
| **驳回**：验收退出码非零/期望串缺、门 RED/STALE_RED 不可 absorb、保护规则拒 | 摘在途状态挂 `state:rejected` | 红件裁决落定时点 |

- 转换 = **摘旧挂新不留双态**（使用纪律 1 同款：与 registry 翻状态格同形态）。
- 仍由确定性事件驱动：**占用闸退出码 / 验收退出码+期望串 / 门裁决**；
  禁人工拍脑袋翻态。
- **主代理只现身异常队列**红件裁决——翻牌是机器动作，不是人审动作。
- 中间态 `state:verifying` 同范式机挂机翻：挂牌时点 = 验收命令全绿交卷进入
  判定面；挂牌判据 = 验收退出码全 0 + 期望串齐（同「转换全部由确定性事件驱动」）。
- 三板（.github / factory-os / af）统一执行本范式；板面在役即
  `state:*` 五态（2026-11-06 GET /labels 全量回读在案）。

---

## `wave/*` 七态废弃注记与对照表（D-79 批）

**废弃范围**：`wave/queued`、`wave/claimed`、`wave/running`、`wave/verifying`、
`wave/merged`、`wave/rejected` 全族不再作为状态标签挂卡。

**废弃理由（词汇三处漂移实证，2026-11-06 取证）**：
1. staging 正本（本文件旧版）用 `wave/*` 七态（含 `claimed`）；
2. 在役三板 API 实读只有 `state:*` 五态、无任何 `wave/*` 状态标签（三板
   GET /labels 全量回读在案）；
3. planner（factory-os）按在役口径建卡与清点：建卡落 `state:queued`
   （`planner.yml:113`），正本注释同口径（`planner.yml:21`）。

三处唯一不动机器面的收敛点 = 正本改写在役五态（正本对齐在役；反向改板成
七态会触发 planner 校验 fail-closed——Q1 M-8 实证）。

**`wave/claimed` 单独说明**：五态标签粒度下无独立「认领」格；认领语义不丢——
由 registry `claimed` 态格、占用闸持有事实与 `state:running`（认领段）承载。
这是本批词汇收敛的核心削格点，其余五格一一对应、无损迁移。

| 旧 `wave/*` 七态 | 新 `state:*` 五态 | 迁移说明 |
|---|---|---|
| `wave/queued` | `state:queued` | 直迁 |
| `wave/claimed` | （并入 `state:running` 认领段） | **废弃削格**；细分由 registry/runner 态格承载 |
| `wave/running` | `state:running`（施工+验收执行段） | 与 claimed 合格 |
| `wave/verifying` | `state:verifying` | 直迁 |
| `wave/merged` | `state:merged` | 直迁 |
| `wave/rejected` | `state:rejected` | 直迁 |
| `wave`（裸） | 保留 | 改义为波次归属标签（纪律 6），非状态 |

---

## 新增 label 族定义（2026-11-06 D-79 批建；三板同步实建）

> 本节四个族全部为**叠加位/申请族位**：不占状态格、不触发状态机转换；
> 挂/摘由各自的确定性事件驱动（使用纪律 5）。三板（.github / factory-os / af）
> 已按本节定义 POST /labels 实建（幂等，已存在跳过）。

### `perm/requested` —— 权限扩大申请（叠加位，Q2 R-2）

- **定义**：worker 或 harness 发起权限扩大申请时挂（申请 comment 为审查取材，
  在役 label 族外新增的申请位）。
- **纪律**：审查取材 = 申请 comment + 卡面 + 既有审计线，**不采信 worker 自报**
  （外派纪律同款）；白名单类由 harness 规则机检（机械匹配 `scope_ask`：只读+
  公开+可逆），白名单外一律转人工终审，**不许默认放行**（fail-closed，与占用闸
  同语义）。
- **摘除**：裁决落定（自动放行 / 人工批 / 拒）即摘，裁决 comment 留痕即审计格。

### `ticket:requested` —— 稀缺资源票据申请（叠加位，Q6 §2.2）

- **定义**：在任务卡下贴标准化申请块（TICKET-REQUEST v1）申请 llm-gw /
  video-gw / gpu-anolis 票据时挂。
- **申请块字段**：ticket_type / task_ref（**必须指向在飞任务卡**）/ resource /
  amount / ttl / purpose / requester（**必须与任务卡在飞身份一致**）。

### `ticket:needs-human` —— 票据转人工裁决（叠加位，Q6 §2.3）

- **定义**：机检不通过或白名单外的申请转人工批时挂 + 运营者裁决评论
  （「超额人工」对应面：人只出现在白名单外）。
- **fail-closed 语义**：账本不可读 / task_ref 解析失败 / hold 命中 ⇒ 一律拒发
  不猜绿（bot-lane 同款）。

### `ticket:revoked` —— 票据已吊销（叠加位，Q6 回收面）

- **定义**：显式吊销回收时挂。回收三步：①摘 key-auth 消费者 ②openBao 侧删
  `kv/company/resource-ticket/<id>` ③板面 label→`ticket:revoked`。
- **纪律**：回收不依赖沙箱配合、不依赖票据本体内容——判定点（网关消费者表 /
  lane 账本 / 准入账本）摘行即断；票据不携带密码学权力。

### `quality:A|B|C|D` —— 派工质量机评（叠加位，Q1 §3.4）

- **定义**：环腿收卷时（merge 或 parked/rejected 裁决落定）由 harness 机写
  issue comment `planner-quality:` + 打叠加 label `quality:A|B|C|D`
  （叠加位纪律同 blocked/legacy）。
- **评分构成**：全部机器可导、**不引入人评**——派发期六要件机检通过数/6 与
  干跑预检 pass 率；施工期沙箱异议计数（/blocked /need-context /need-env）；
  验收期 gates 首过与否、追加 push 轮数、交卷清单未勾项数。
- **落盘与回流**：`factory-os/波次清单/wave-NN.quality.json`（append-only）
  → planner 组装 `planner_quality_recent` 回流下一波规划。
- **禁人工评档**：`quality:*` 只许机器写；人工评档视同人工拍脑袋翻态（纪律 3）。

---

## 转换总图（一屏版）

```text
                ┌──────────────────────────────────────────────┐
                │                state:queued                 │
                │  （卡面齐备待派；占用闸/OOM 准入前置）        │
                └──────┬───────────────────────┬──────────────┘
       占用闸放行+认领  │                       │ 占用闸 BLOCK
                （开卡翻牌）▼                       ▼
                ┌──────────────┐         （叠加 blocked）
                │ state:running│◄─────────────────┐
                │（认领→施工→   │  认领异常回队     │
                │ 验收命令执行）│───────────┐      │
                └──────┬───────┘  命令红    │      │
            命令全绿   │                    ▼      │
                （交卷）▼        （叠加 blocked + 异常队列）
                ┌───────────────┐  红/不可吸收 │
                │state:verifying│─────────┐    │
                └──────┬────────┘          │    │
           merge-check绿│                  ▼    ▼
                （合线翻牌）▼        ┌───────────────┐
                ┌──────────────┐     │state:rejected │──修订重派──▶ state:queued
                │ state:merged │     └──────┬────────┘
                └──────┬───────┘            │ 暂缓（叠加）
                落账完成 │                    ▼
                       ▼             （叠加 legacy）
                     归档
```

## 与判官路径的联动（红线）

- `state:rejected` 的常见成因之一是判官路径触碰——这不是普通的验收红，而是
  CODEOWNERS 保护规则的**结构性拒绝**（合不进去）。此类卡的重派必须先把改动
  移出判官路径，或走「判据变更 = 裁决 + 同批重钉」的正路（见 `docs/judge-paths.md`），
  禁用工人的普通 PR 通道硬闯。
