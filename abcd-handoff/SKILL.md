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

## 3. 生成 HTML viewer（人看的可视化，推荐）
- **先离线预渲染 PlantUML**：`bash <skill-dir>/shared/scripts/render_plantuml.sh design` → `rendered/<id>.svg`。**缺 `plantuml` 就装**（装了人打开 HTML 直接看图——别只给源码，源码人读效率低）：macOS `brew install plantuml`、Debian `sudo apt-get install -y plantuml`（含 graphviz，usecase 布局必需）；或设 `PLANTUML_JAR` + java。纯离线，图数据不出本机。
- **再生成 HTML**：`python3 <skill-dir>/shared/scripts/build_index_html.py design`（无 pip 依赖）→ `design/index.html`：按 A/B/C/D 分组，每图带 `provenance`/`level`/`type`/`gaps`/`code_refs` 注解 + 追溯链表。
- Mermaid 走 CDN（`mermaid@11`）浏览器**本地**渲染、源码不外泄；PlantUML 用上一步的 `rendered/<id>.svg` **内联**（没渲染成功才折叠源码兜底）。
- 自包含单文件，可直接发人 / 发另一个 AI agent（类比 gstack `plan-design-review` 的 HTML 产物）。

## 4. 渲染（可选；PlantUML 预渲染 + 离线 SVG）
- `.mmd` → `rendered/*.svg`（`mmdc`，或复用 gstack `/diagram`）；`.puml` → svg（`plantuml.jar`）。缺渲染器只告警（GitHub 原生渲染 mermaid；HTML viewer 用 CDN）。

## 5. 打包（可选）
- 需要单文件分享时，把各图嵌进一份 md；或 `zip` 整个 `design/`。

产出：一份完整、可渲染、可导航（manifest 串联）的 `design/`，能直接交给人或另一个 AI agent。
