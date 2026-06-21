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
---

# /abcd-trace <flow> [path] [--level system|design]

`/abcd-recover` 的轻量单流程版：出**一张序列图**（设计级），不做类图 / 剥离。日常高频用。

**两档粒度**（`--level`，默认 `system`）：
- `system`（默认）：泳道 = 本系统 + 外部系统/服务，消息 = 服务间调用 / endpoint。→ `sequences/<flow>.mmd`、`type=system-sequence`。
- `design`：泳道 = 系统**内部**代码模块/类，消息 = **真实方法调用**（顺调用链抽 `mod.method(args)` + 返回）。→ `sequences/<flow>.design.mmd`、`type=design-sequence`。最适合给 AI 导航代码。

读 `shared/references/diagram-syntax.md`（序列图模板）。

## 流程
1. 定位流程入口（路由 / handler `文件:行`）。
2. 顺调用链 handler → service → 外部系统 / DB，整理**有序消息列表**（参与者 → 参与者：做某事 + `文件:行`）；识别外部参与者。
3. 出 Mermaid `sequenceDiagram`：`system` → `<flow>.mmd`；`design` → `<flow>.design.mmd`（泳道=内部类/模块、消息=方法调用）。`Note` 挂 `文件:行`。
4. 更新 / 创建 manifest 里该图条目（`provenance=reverse, level=design, type=system-sequence|design-sequence, code_refs`）。

**只读不改**；消息 = 调用、忠于代码；拿不准标"不确定"。需要类图 / 剥离 / 整模块时改用 `/abcd-recover`。
