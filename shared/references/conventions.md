# 约定 (conventions)

## 命名
- 图 id：`<type>-<slug>`，如 `seq-outreach-send`、`class-asbuilt`、`domain-analysis`。
- 文件布局见 `package-spec.md`；用例规约 `B-requirements/specs/<usecase>.md`（+ 生成 `<usecase>.activity.puml`）。
- 类 / 属性命名纪律见 `method-abcd.md` §3（单数名词、无冗余后缀、核心域术语）。

## 代码链接（可追溯地图）
- 每个 diagram / use_case 填 `code_refs: [{symbol, path, lines}]`：`path` 相对目标项目根、`lines` 用 `起-止`。
- 序列图消息旁用 `Note` 标 `文件:行`；Mermaid 节点能加 `click` 跳转就加。
- `manifest.traceability` 串 `用例 → 分析类 → 代码`，支持业务 ↔ 代码双向下钻。

## provenance / level / gaps（逆向必标）
- `provenance`：`forward`（对话）| `reverse`（读代码）| `hybrid`（逆向骨架 → 对话补全）。
- `level`：`business` | `requirement` | `analysis` | `design`。
- 纯逆向 → `recovered/`（reverse + design）；剥离后的分析 → `C-analysis/`（hybrid + analysis）。
- **`gaps` 如实记代码给不了的**：需求层、人工 / 线下环节、现状全貌。
- **硬纪律**：需求层（愿景 / 系统用例 / 规约）永不 `reverse`；无依据不编。

## 渲染产物
- `rendered/*.svg` 是给人看的派生物，可 `.gitignore`；AI 读源码。
