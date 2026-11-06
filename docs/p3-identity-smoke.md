# P3-1 工人身份链 E2E 冒烟记录

## 目的
验证 harness-worker 通道的工人身份链：Repo-Writer App installation token → task/ 分支 →
PR（Bot 作者）→ commit 归因 trailer → squash 合线。对应施工卡 af#2（[P3-1] 工人身份链
E2E 冒烟）。本文件为该卡唯一允许的新增件（docs/ 下记录件，不触碰任何判官/门/判据路径）。

## 执行时刻
- 执行时刻（UTC）: 2026-11-06T09:24:16Z
- 执行时刻（本地）: 2026-11-06T17:24:16+0800
- token 铸造窗口: iat/exp = 1793956996/1793957656（JWT iss=App_ID 5122476，iat-60/exp+600）

## token 指纹
- installation token sha256[:12] = `d0ac062846b5`
- 纪律：token/私钥/JWT 的值禁打印禁落盘，本件仅留指纹（sha256 前 12 位）。

## 身份链验证点
1. PR 作者为 App 身份 repo-writer4agent（user.type=Bot，非人类账号）。
2. commit 归因 trailer：Co-Authored-By: Repo-Writer4Agent <5122476+repo-writer4agent[bot]>。
3. squash 合线（该仓禁 merge commit）后本文件出现在 main。
4. 全程输出零凭据字样（私钥 mktemp 0600、用后 shred；token 仅经环境变量 + credential helper）。

## 通道
harness-worker：baoq 取 App 私钥 → openssl 铸 RS256 JWT →
POST /app/installations/166164132/access_tokens 取 installation token。
