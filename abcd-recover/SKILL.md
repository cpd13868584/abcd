---
name: abcd-recover
description: |
  逆向：读代码 → 设计级 as-built（类图 / 架构图 / 系统交互序列图）+ 剥离后的分析级领域模型。
  只恢复"设计级"，绝不冒充需求/业务模型。Use when asked to "逆向出设计包", "读代码出类图",
  "recover design from code", "reverse this codebase". (abcd)
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
  - Agent
  - AskUserQuestion
---

# /abcd-recover [path] [--flow <name>]

逆向读代码，产出**设计级 as-built** 设计包（+ 剥离的分析级草模），写进目标项目的 `design/`（见 package-spec）。**绝不从代码臆造业务/需求层。**

开工前按需读（渐进式披露）：
- `shared/references/method-abcd.md` — §3–4（分析剥离清单、类图 linter）、§6（正逆边界）
- `shared/references/package-spec.md` — 设计包结构 + manifest schema
- `shared/references/diagram-syntax.md` — Mermaid / PlantUML 图法模板

## 流程

### 0. 定范围
确认目标目录；问清是**单流程**（`--flow 达人外联`）还是**整模块**。单流程优先。

### 1. 测绘（hybrid：脚本骨架 + LLM 语义）
- **确定性骨架**（有脚本就跑 `shared/scripts/`，否则直接读）：
  - schema（SQL DDL / Drizzle / Prisma / SQLAlchemy / OpenAPI）→ 实体 + 字段 + 外键 + 多重性。
  - 路由注册（controller / Hono / FastAPI / Tauri command）→ 入口列表（method, path, handler `文件:行`）。
- **LLM 语义**（脚本做不了的）：从入口顺调用链 handler → service → 外部系统 / DB，整理成**有序消息列表**（参与者 A → 参与者 B：做某事 + `文件:行`）；识别外部参与者（DB、第三方、其他服务、LLM）。
- 大库用 `Agent`（Explore）并行测绘。**只读、不改、不臆造**；拿不准标"不确定"。

### 2. 出设计级产物 → `recovered/`（provenance=reverse, level=design）
- 每个流程一张**系统序列图**（Mermaid `sequenceDiagram`）：参与者 = 本系统 + 外部系统/服务 + actor；消息 = 服务间调用；`Note` 挂 `文件:行`。→ `sequences/<flow>.mmd`、`type=system-sequence`。
- 关键流程可再出**设计序列图（对象/方法级）**：把上面那张里的"本系统"盒子拆开——泳道 = 内部代码模块/类，消息 = **真实方法调用**（顺调用链抽 `mod.method(args)` + 返回），`opt`/`alt`/`Note` 标分支与幂等/守门。它是 call graph、逆向最忠实，最适合给 AI 导航改代码。→ `sequences/<flow>.design.mmd`、`type=design-sequence`。
- **类图**（Mermaid `classDiagram`）：涉及实体的 as-built 结构，**保留** id / 外键 / status（这就是设计级）。
- 整模块时另出**架构图**（architecture-beta / C4）。

### 3. 剥离 → 分析级 `C-analysis/domain.mmd`（provenance=hybrid, level=analysis）
- 按 method-abcd §4 剥离清单去污染（id / 外键 / status 串 / 时间戳 / List 实现 / 单据照搬类 / 性能冗余）；用"去掉它会怎样？——'有性能问题'就删"测试。
- 套类图 linter（method-abcd §3）：默认普通关联、无 aggregate root、多重性只 `1`/`*`、类名单数名词、**把领域概念从被污染表里提炼出来**、status → 状态机（不作属性）。
- 本系统不维护的实体标"外部，仅引用"。

### 4. 写 manifest + README（见 package-spec）
- 每图填 `workflow/type/tool/provenance/level/gaps/code_refs(文件:行)`。
- **gaps 必须如实记代码给不了的**：`"业务/需求层未恢复（愿景/系统用例/规约）——需 /abcd-model 正向补全"`。
- glossary（核心域术语）、traceability（用例→分析类→代码，逆向时用例待补）、`ai_spec.is_implementation_input=false`。

### 5. 边界（硬纪律）
逆向**只到设计级** + 剥离的分析级草模。**愿景 / 系统用例 / 用例规约绝不从代码生成**，一律入 `gaps`。产物物理隔离：reverse → `recovered/`；剥离后的分析 → `C-analysis/`。

### 6. 渲染（可选）
Mermaid：`mmdc` 或复用 gstack `/diagram`；用例图：PlantUML。`.md` 内 mermaid 在 GitHub 原生可看。

**完成后**告诉用户：产出在 `<target>/design/`（未跟踪）、有哪些 `gaps`、建议接 `/abcd-model` 补需求层。
