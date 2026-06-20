---
name: abcd-recover
description: |
  逆向：读代码 → 设计级 as-built（类图 / 架构图 / 系统交互序列图）+ 业务序列图骨架。
  只恢复"设计级"，绝不冒充需求/业务模型。Use when asked to "逆向出设计包", "读代码出类图",
  "recover design from code", "reverse this codebase". (abcd)
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
  - AskUserQuestion
triggers:
  - 逆向出设计包
  - 读代码出类图
  - recover design from code
  - reverse this codebase
---

# /abcd-recover

读现有代码，产出**设计级 as-built** 的 diagram-as-code 设计包：类图、架构图、系统交互序列图（`provenance: reverse`，放 `recovered/`）+ 业务序列图骨架（再由 `/abcd-model` 对话补全）。

> 🚧 **WIP** — 流程实现中。硬纪律与契约见仓库 `shared/references/`（`method-abcd.md` 的"逆向剥离 / 类图 linter"、`package-spec.md` 的设计包结构），完整设计见 `abcd-skill-brief.md` §3 / §6 / §7。
