---
name: abcd-sync
description: |
  闸门：① 图 vs 代码（防文档过时）② 代码 vs 正向需求/分析模型（抓 AI 写代码跑偏，
  靠 ai_spec.acceptance）。Use when asked to "sync 设计与代码", "校验代码是否跑偏",
  "check code against the model". (abcd)
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - AskUserQuestion
---

# /abcd-sync [path]

设计包与代码的双向验收闸门。读 `shared/references/package-spec.md`（manifest 字段）。

## 1. 图 vs 代码（防过时）
- 对 `manifest.diagrams` 里 `provenance=reverse` 的图，按其 `code_refs` 重读当前代码（schema / 路由 / 调用链），与图内容 diff：
  - 实体 / 字段 / 外键变了 → 类图过时；路由 / 调用链变了 → 系统序列图过时；`code_refs` 行号漂移 → 待更新。
- 产出**过时清单**（哪张图、哪处不符、建议：重跑 `/abcd-recover` 该图 或 改代码）。

## 2. 代码 vs 正向模型（抓 AI 跑偏）—— AI 时代高价值
- 逐条核对 `manifest.ai_spec.acceptance` 与 `constraints` 是否仍在代码中成立（按 `traceability` / `code_refs` 定位相关代码读 / grep 验证）。
- 核对 `traceability`（用例→分析类→代码）链接是否还解析得到（文件 / 符号还在）。
- 每条给 **pass / fail + 证据（文件:行）**；fail = 代码偏离了正向需求 / 分析模型（可能 AI 写歪了，或需求该更新）。

## 3. 报告
输出 sync 报告：过时图清单 + acceptance / constraint 通过情况 + 建议动作（更新图 / 修代码 / 回 `/abcd-model` 改模型）。**不自动改代码**；拿不准标"不确定"，让人决策。
