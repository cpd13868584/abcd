---
name: abcd-handoff
description: |
  通用：组装 README + manifest + 渲染图，把 design/ 设计包打包成可交接、可分享的形态。
  Use when asked to "打包设计包", "handoff this design", "package the design". (abcd)
allowed-tools:
  - Bash
  - Read
  - Write
triggers:
  - 打包设计包
  - handoff this design
  - package the design
---

# /abcd-handoff

把 `design/` 设计包组装成交接物：生成索引 `README.md`、校验 `manifest.json` 一致性、渲染 `.mmd`/`.puml` 到 `rendered/*.svg`（Mermaid 可复用 gstack `/diagram`，PlantUML 自带）。

> 🚧 **WIP** — 流程实现中。设计包结构见 `shared/references/package-spec.md`；渲染见 `shared/references/diagram-syntax.md`。
