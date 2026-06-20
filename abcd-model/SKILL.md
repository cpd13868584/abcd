---
name: abcd-model
description: |
  正向（旗舰）：对话式 A→B→C 业务建模 —— 愿景 → 业务用例/序列图（现状→改进）→
  系统用例/规约 → 分析类图。产物即驱动 AI 写代码（D）的 spec。Use when asked to
  "为业务建模", "abcd 建模", "正向建模", "model this business". (abcd)
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
  - Edit
  - Agent
  - AskUserQuestion
---

# /abcd-model [--to A|B|C] [path]

正向、对话式走《软件方法》ABCD：A 业务建模 → B 需求 → C 分析。**每层从上一层推导**；产物即驱动 AI 写 D 的 spec。已有代码时，可吃 `/abcd-recover` 的设计级资产作**对照起点**（别让正向模型与实现脱节）。

开工前按需读：`shared/references/method-abcd.md`（§2 A、§3 类图 linter、§5 规约模板、§6 边界）、`package-spec.md`、`diagram-syntax.md`。

## A 业务建模
- **A1 愿景（对话——只有人能答）**：业务意图不在代码里。用**爆炸法**定**老大**（系统最优先照顾谁；是具体的人/角色，**不是**团队领导）；定**目标组织** + **量化改进目标**（对组织行为的度量，非系统功能）。先读已有设计文档(docs/)harvest，**缺的问用户**；给草案就标 `待确认`，不替老大拍板。→ `A-business/vision.md` + `manifest.vision`。
- **A2 业务用例图**（PlantUML usecase）：组织对外价值。业务执行者(边界外) → 业务用例(=价值)；业务工人/业务实体**不上图**。→ `A-business/usecases.puml`。
- **A3 业务序列图**（Mermaid）**现状 → 改进**——招牌：
  - 现状**如实**（亲临现场 / 读文档 / 问人）；参与者只 业务工人 / 业务实体 / 时间；消息=责任（不写"请求"、不画返回）。
  - 套**四种改进模式**得改进版；**改进版指向待引入系统的每条消息 = 一个系统用例**。
  → `A-business/sequence-as-is.mmd` + `sequence-to-be.mmd`。

## B 需求
- **B1 系统用例图**（PlantUML usecase）：执行者 = 改进版业务序列图中与系统实线相连的对象；用例名动宾；主执行者→用例、辅执行者←用例。→ `B-requirements/usecases.puml`。
- **B2 用例规约**（hybrid，文本为源）：前置/后置=可检测状态；涉众利益；基本路径**四步曲**(请求/验证/改变/回应)；扩展 `Na`/`Na1`；补充约束四类。判据"**不这样不行**"。→ `specs/<uc>.md`，路径段机械生成 `<uc>.activity.puml`。

## C 分析
- **C1 分析类图**（Mermaid）：从规约名词/事件提炼实体类；套类图 linter（method-abcd §3）；有 `/abcd-recover` 的 `C-analysis/` 草模就交叉验证。→ `C-analysis/domain.mmd`。

## 收尾
- 写 manifest（见 package-spec）：`vision`、各图 `provenance=forward`/`level`、`use_cases`、`traceability`(用例→分析类→代码)、`ai_spec.is_implementation_input=true`（`constraints`/`acceptance` 供 `/abcd-sync` 验收）。
- **对话纪律**：A 的愿景/涉众利益**必须问人、不臆造**；代码/文档给不了的标 `gap`，不替老大决策。`--to A|B|C` 控制停在哪层。
