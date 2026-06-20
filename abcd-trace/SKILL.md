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

# /abcd-trace <flow> [path]

`/abcd-recover` 的轻量单流程版：只出**一张系统序列图**（设计级），不做类图 / 剥离。日常高频用。

读 `shared/references/diagram-syntax.md`（序列图模板）。

## 流程
1. 定位流程入口（路由 / handler `文件:行`）。
2. 顺调用链 handler → service → 外部系统 / DB，整理**有序消息列表**（参与者 → 参与者：做某事 + `文件:行`）；识别外部参与者。
3. 出 Mermaid `sequenceDiagram` → `design/recovered/sequences/<flow>.mmd`，`Note` 挂 `文件:行`。
4. 更新 / 创建 manifest 里该图条目（`provenance=reverse, level=design, code_refs`）。

**只读不改**；消息 = 调用、忠于代码；拿不准标"不确定"。需要类图 / 剥离 / 整模块时改用 `/abcd-recover`。
