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
triggers:
  - sync 设计与代码
  - 校验代码是否跑偏
  - check code against the model
---

# /abcd-sync

两件事：重提取并 diff 图 vs 当前代码（防过时）；对照正向建出的需求/分析模型与 `manifest.ai_spec.acceptance` 校验代码有没有跑偏——AI 时代的高价值验收闸门。

> 🚧 **WIP** — 机制待定（见 `abcd-skill-brief.md` §5 B 组讨论）。契约字段见 `package-spec.md` 的 `ai_spec`。
