#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tools/ci-gates-selftest.py — ci-gates.yml（org 第一批六门）自检 + 变异负控（A-7 自体应用）。

卡面: factory-os issue #8（w04-org-ci-gates-firstbatch / D-75 / L-01）。
判据正本: 30-工件/CI流水线研究-20261106/Q1-门机制分级.md §2.1 A-1/A-3/A-4/A-7/A-8/A-9
  与 A-22（af/ci/gh_workflow_check.py:12-40 R01–R22 口径；判据面本体本卡零改动，本件
  只是对 ci-gates.yml 的独立机判面）。

验收命令（卡面验收命令集 1/2/4，本地可机判，不依赖 Actions 执行面）:
  python3 -I tools/ci-gates-selftest.py                 # 基线全绿 + 变异全红 → exit 0
  python3 -I tools/ci-gates-selftest.py --workflow PATH # 指定被检件（默认仓根相对路径）

断言面（基线必须全绿）:
  1. YAML 可解析（PyYAML safe_load 优先；PyYAML 缺席时退内建最小结构解析——卡面验收 4
     允许「等价自检件内解析步」；两种方法都在输出里点名）
  2. on.workflow_call 与 inputs 在场
  3. 六门步各在（A-1/A-3/A-4/A-7/A-8/A-9，各带 run 体）——编号=Q1-门机制分级.md:148/:150/
     :151/:154/:155/:156
  4. 全文无吞红字面量（管管空格真）与 continue-on-error 真（拼接构造，防自指误伤）
  5. permissions = contents: read（顶层语义对账）；全文无 contents: write
  6. uses: 只引本组织 CloudCrane-Software/（零外部 action，A-22 口径；本件应为零 uses）
  7. 禁提权触发（pull_request 下划线 target）；每 job timeout-minutes ≤45；顶层
     concurrency（group + cancel-in-progress）在场

变异负控（A-7 自体应用：删它必须红）5 种 ≥3，每种变异下本自检必红并点名变异:
  M1 删门步（整块摘除 A-8 步）            → 「六门缺席:A-8」
  M2 插吞红（run 内追加管管空格真）        → 「吞红」
  M3 权限翻转（contents: read → write）   → 「permissions」
  M4 删 workflow_call 触发（换 dispatch）  → 「workflow_call」
  M5 插外部 action（uses: actions/…）     → 「外部 action」

退出码: 0=基线绿 ∧ 变异负控全红（点名）；1=有违；2=用法/环境错。
零第三方依赖（PyYAML 在场则用，缺席退内建）；python3 -I 直跑。
"""

import argparse
import os
import re
import sys

ORG = "CloudCrane-Software"
GATES = ("A-1", "A-3", "A-4", "A-7", "A-8", "A-9")
WF_DEFAULT = os.path.join(".github", "workflows", "ci-gates.yml")

# 被禁字面量以拼接构造，防本自检件对自身/被检件注释发生自指误伤：
ABSORB_RUN = "|" + "| true"          # 管-管-空格-真（吞红写法一）
ABSORB_COE = "continue-on-" + "error: true"  # 吞红写法二（step 级放行）
TRIGGER = "pull_request" + "_target"  # 提权触发（R03）

try:
    import yaml  # PyYAML（系统 dist-packages；python3 -I 下仍可见用户级除外）
    HAVE_YAML = True
except ImportError:  # pragma: no cover - 环境相关
    yaml = None
    HAVE_YAML = False


def parse_doc(text):
    """返回 (doc|None, method, err|None)。PyYAML 优先；缺席退内建最小结构解析。"""
    if HAVE_YAML:
        try:
            return yaml.safe_load(text), "pyyaml.safe_load", None
        except Exception as exc:  # 解析不了 = fail-closed 红
            return None, "pyyaml.safe_load", str(exc)
    errs = []
    seen_at = {}
    for lineno, raw in enumerate(text.splitlines(), 1):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = raw[: len(raw) - len(raw.lstrip())]
        if "\t" in indent:
            errs.append(f"L{lineno}: 缩进含 TAB")
            continue
        m = re.match(r"^(\s*)([^#\-\s][^:]*):(\s|$)", raw)
        if not m:
            # 列表项（- 开头）或块标量正文——最小解析只对键行做重复键检查
            continue
        key = m.group(2).strip()
        sig = (len(indent), key)
        if sig in seen_at:
            errs.append(f"L{lineno}: 同层重复键 {key}（首见 L{seen_at[sig]}）")
        else:
            seen_at[sig] = lineno
    method = "builtin-minimal-parser"
    if errs:
        return None, method, "; ".join(errs[:5])
    return {"_structural_ok": True}, method, None


def steps_of(doc, text):
    """返回 [(name, has_run, indent)]。PyYAML 路径取结构；内建路径按行扫。"""
    steps = []
    if HAVE_YAML and isinstance(doc, dict):
        jobs = doc.get("jobs")
        if isinstance(jobs, dict):
            for jb in jobs.values():
                for st in (jb or {}).get("steps") or []:
                    if isinstance(st, dict):
                        steps.append((st.get("name") or "", "run" in st, None))
        return steps
    cur_indent = None
    for raw in text.splitlines():
        m = re.match(r"^(\s*)-\s+name:\s*(.*)$", raw)
        if m:
            cur_indent = len(m.group(1))
            steps.append((m.group(2).strip().strip('"'), False, cur_indent))
            continue
        if steps and raw.strip():
            ind = len(raw) - len(raw.lstrip())
            if cur_indent is not None and ind <= cur_indent:
                cur_indent = None
            elif cur_indent is not None and re.match(r"^\s*run:", raw):
                nm, _, ci = steps[-1]
                steps[-1] = (nm, True, ci)
    return steps


def violations(text):
    """核心机判：返回 (违规列表, 解析方法)。空列表=基线绿。"""
    vs = []
    doc, method, perr = parse_doc(text)
    if perr:
        vs.append(f"yaml解析失败[{method}]: {perr}")
        return vs, method
    structured = HAVE_YAML and isinstance(doc, dict) and "jobs" in doc

    # 2. workflow_call + inputs 在场
    if structured:
        trig = doc.get("on")
        if trig is None:
            trig = doc.get(True)  # PyYAML 1.1 把裸 on 解析成布尔 True
        call = (trig or {}).get("workflow_call") if isinstance(trig, dict) else None
        if not call:
            vs.append("workflow_call 触发缺席")
        elif not isinstance(call, dict) or "inputs" not in call:
            vs.append("workflow_call inputs 缺席")
    else:
        if not re.search(r"^on:\s*$", text, re.M) or not re.search(r"^\s+workflow_call:\s*$", text, re.M):
            vs.append("workflow_call 触发缺席")
        if not re.search(r"workflow_call:\s*\n\s+inputs:", text):
            vs.append("workflow_call inputs 缺席")

    # 3. 六门步各在（带 run 体）
    steps = steps_of(doc, text)
    for g in GATES:
        if not any(g in nm and has_run for nm, has_run, _ in steps):
            vs.append(f"六门缺席:{g}")

    # 4. 吞红字面量（拼接构造禁词，全文扫描）
    if ABSORB_RUN in text:
        vs.append("吞红在场:" + ABSORB_RUN)
    if ABSORB_COE in text:
        vs.append("吞红在场:" + ABSORB_COE)

    # 5. permissions 顶层语义对账（contents: read；全文无 write）
    if structured:
        perms = doc.get("permissions")
        if perms != {"contents": "read"}:
            vs.append(f"permissions 非 contents: read（实得 {perms!r}）")
    else:
        if not re.search(r"^permissions:\n  contents: read\s*$", text, re.M):
            vs.append("permissions 非 contents: read")
    if re.search(r"contents:\s*write", text):
        vs.append("permissions 出现 write")

    # 6. uses 只引本组织（零外部 action；覆盖列表项形态「- uses:」）
    for ref in re.findall(r"^\s*(?:-\s+)?uses:\s*(\S+)", text, re.M):
        if not ref.startswith(ORG + "/"):
            vs.append(f"外部 action:{ref}")

    # 7. A-22 其余：提权触发 / timeout / concurrency
    if TRIGGER in text:
        vs.append("禁用触发在场:" + TRIGGER)
    if structured:
        jobs = doc.get("jobs") or {}
        if not isinstance(jobs, dict) or not jobs:
            vs.append("jobs 缺席")
        else:
            for jn, jb in jobs.items():
                tm = (jb or {}).get("timeout-minutes")
                if not isinstance(tm, int) or tm > 45:
                    vs.append(f"job {jn} timeout-minutes 缺席或超限(≤45)")
        cc = doc.get("concurrency")
        if not (isinstance(cc, dict) and cc.get("group") and cc.get("cancel-in-progress") is True):
            vs.append("顶层 concurrency（group+cancel-in-progress）缺席")
    else:
        if "timeout-minutes:" not in text:
            vs.append("timeout-minutes 缺席")
        if not re.search(r"^concurrency:", text, re.M):
            vs.append("顶层 concurrency 缺席")

    return vs, method


# ---- 变异负控（A-7 自体应用：删它必须红） ------------------------------------

M2_ANCHOR = 'python3 -I .ci-gates-out/runner.py "$CI_GATES_MANIFEST" .ci-gates-out || HARNESS_RC=$?'


def mut_drop_step_a8(text):
    lines = text.splitlines()
    out, i, n, removed = [], 0, len(lines), False
    while i < n:
        m = re.match(r"^(\s{6})- name: ", lines[i])
        if m and "A-8" in lines[i]:
            removed = True
            j = i + 1
            while j < n and (lines[j].startswith(" " * 8) or not lines[j].strip()):
                j += 1
            i = j
            continue
        out.append(lines[i])
        i += 1
    if not removed:
        raise AssertionError("M1 锚点未命中——自检件与工作流件结构漂移，先修自检件")
    return "\n".join(out) + "\n"


def mut_absorb_red(text):
    if M2_ANCHOR not in text:
        raise AssertionError("M2 锚点未命中——自检件与工作流件结构漂移，先修自检件")
    injected = M2_ANCHOR + "\n" + " " * 10 + 'python3 -I .ci-gates-out/runner.py "$CI_GATES_MANIFEST" .ci-gates-out ' + ABSORB_RUN
    return text.replace(M2_ANCHOR, injected, 1)


def mut_perm_write(text):
    if text.count("contents: read") != 1:
        raise AssertionError("M3 锚点不唯一——自检件与工作流件结构漂移，先修自检件")
    return text.replace("contents: read", "contents: write", 1)


def mut_drop_call(text):
    if "  workflow_call:" not in text:
        raise AssertionError("M4 锚点未命中——自检件与工作流件结构漂移，先修自检件")
    return text.replace("  workflow_call:", "  workflow_dispatch:", 1)


def mut_insert_action(text):
    anchor = "    steps:"
    if anchor not in text:
        raise AssertionError("M5 锚点未命中——自检件与工作流件结构漂移，先修自检件")
    return text.replace(anchor, anchor + "\n" + " " * 6 + "- uses: actions/checkout@v4", 1)


MUTATIONS = (
    ("M1 删门步(A-8)", mut_drop_step_a8, "A-8"),
    ("M2 插吞红", mut_absorb_red, "吞红"),
    ("M3 权限翻转(write)", mut_perm_write, "permissions"),
    ("M4 删workflow_call触发", mut_drop_call, "workflow_call"),
    ("M5 插外部action", mut_insert_action, "外部 action"),
)


def main(argv=None):
    ap = argparse.ArgumentParser(
        prog="ci-gates-selftest.py",
        description="ci-gates.yml 第一批六门：基线自检 + 变异负控（A-7 自体应用）")
    ap.add_argument("--workflow", default=WF_DEFAULT,
                    help="被检工作流件路径（默认仓根相对 .github/workflows/ci-gates.yml）")
    args = ap.parse_args(argv)
    if not os.path.isfile(args.workflow):
        print(f"selftest: 被检件缺席 {args.workflow}", file=sys.stderr)
        return 2
    with open(args.workflow, encoding="utf-8") as fh:
        text = fh.read()

    fails = []
    base_vs, method = violations(text)
    if base_vs:
        fails.append(("基线", base_vs))
        for v in base_vs:
            print("基线红: " + v)
    else:
        print(f"基线绿（解析方法={method}；六门在位；无吞红；权限只读；零外部 action）")

    mut_reports = []
    for name, fn, marker in MUTATIONS:
        try:
            mut_text = fn(text)
        except AssertionError as exc:
            fails.append((name, [str(exc)]))
            mut_reports.append(f"{name}: 变异器自坏——{exc}")
            continue
        vs, _ = violations(mut_text)
        named = [v for v in vs if marker in v]
        if not vs:
            mut_reports.append(f"{name}: 未红（零违规）——负控失守")
            fails.append((name, ["变异后零违规——负控失守"]))
        elif not named:
            mut_reports.append(f"{name}: 红但未点名（violations={vs}）")
            fails.append((name, [f"变异后红但未点名期望标记 {marker!r}: {vs}"]))
        else:
            mut_reports.append(f"{name}: 必红 ✓ 点名「{named[0]}」")

    print("—— 变异负控（A-7 自体应用：删它必须红）——")
    for r in mut_reports:
        print("  " + r)
    if fails:
        print(f"selftest: 红 → exit 1（违例组 {len(fails)}）")
        for name, vs in fails:
            for v in vs:
                print(f"  [{name}] " + v)
        return 1
    print(f"selftest: 全绿 exit 0（基线绿 + {len(MUTATIONS)} 变异全红且点名；解析={method}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
