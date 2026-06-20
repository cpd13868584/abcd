---
name: abcd-handoff
description: |
  通用：组装 README + manifest + 渲染图，把 design/ 设计包打包成可交接、可分享的形态。
  Use when asked to "打包设计包", "handoff this design", "package the design". (abcd)
allowed-tools:
  - Bash
  - Read
  - Write
---

# /abcd-handoff [path]

把 `design/` 设计包组装成可交接、可分享的形态。读 `shared/references/{package-spec.md, diagram-syntax.md}`。

## 1. 校验
- `manifest.json` 合法 JSON；`diagrams[].file` / `use_cases[].spec` 引用的文件都存在；`code_refs` 的 path 在目标项目里能找到。
- 报告缺失 / 悬挂引用。

## 2. 生成索引 README
- 从 `manifest` 生成 / 刷新 `design/README.md`：按 workflow（A/B/C/D）列出各图（标题 + `provenance`/`level` + `gaps`），给 AI 接收方一个入口。
- 用例规约缺活动图视图的，由路径段补生成 `<uc>.activity.puml`。

## 3. 渲染
- `.mmd` → `rendered/*.svg`（`mmdc`，或复用 gstack `/diagram`）；`.puml` → svg（`plantuml.jar`）。缺渲染器只告警（GitHub 原生渲染 mermaid）。

## 4. 打包（可选）
- 需要单文件分享时，把各图嵌进一份 md；或 `zip` 整个 `design/`。

产出：一份完整、可渲染、可导航（manifest 串联）的 `design/`，能直接交给人或另一个 AI agent。
