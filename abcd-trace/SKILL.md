---
name: abcd-trace
description: |
  逆向（日常高频）：单个端到端流程 → 一张系统序列图（设计级）。从入口顺着调用链
  抽出"系统 ↔ 外部系统/服务"的协作。Use when asked to "trace this flow",
  "画出这个流程的时序图", "trace the login flow". (abcd)
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
triggers:
  - trace this flow
  - 画出这个流程的时序图
  - 这个流程的时序
  - trace the flow
---

# /abcd-trace <flow>

给定一个端到端流程（如 `login`、`checkout`），从入口顺调用链抽出一张**系统序列图**（设计级，`provenance: reverse`）。`/abcd-recover` 的轻量单流程版。

> 🚧 **WIP** — 流程实现中。画法/语义见 `shared/references/diagram-syntax.md`（序列图）与 `method-abcd.md`；完整设计见 `abcd-skill-brief.md` §3 / §5。
