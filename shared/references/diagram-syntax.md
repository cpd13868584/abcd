# 图法速查 (diagram-syntax)

工具分工：**Mermaid** 画类图 / 序列图 / 状态机 / ER；**PlantUML** 画用例图（Mermaid 无原生 usecase；PlantUML 是 AI 生成 UML 的缺省表示）+ 用例规约的活动图视图。**语义规则见 `method-abcd.md`**；本文件只给语法模板与风格。

## 选型表

| 图 | 工具 | 后缀 |
|---|---|---|
| 业务用例图 / 系统用例图 | PlantUML | `.puml` |
| 业务序列图 / 系统序列图 | Mermaid `sequenceDiagram` | `.mmd` |
| 类图 / 领域模型 | Mermaid `classDiagram` | `.mmd` |
| 状态机 | Mermaid `stateDiagram-v2` | `.mmd` |
| ER | Mermaid `erDiagram` | `.mmd` |
| 用例规约活动图（视图） | PlantUML activity | `.activity.puml` |
| 架构图 | Mermaid `architecture-beta` / C4 | `.mmd` |

## 模板

### 用例图（PlantUML）
```plantuml
@startuml
left to right direction
actor 储户 as A1
rectangle ATM {
  usecase "取现金" as UC1
}
A1 --> UC1
@enduml
```

### 序列图（Mermaid）
```mermaid
sequenceDiagram
    actor U as 执行者
    participant S as 系统
    participant X as 外部系统
    U->>S: 动宾(参数)
    S->>X: 动宾
    X-->>S: 结果
    Note over S: path:line
```
- **业务序列图**：消息=责任、不写"请求"、不画返回、系统黑箱（method-abcd §2）。
- **系统序列图（逆向设计级）**：正常技术交互，可画返回；`Note` 挂 `文件:行`。

### 类图（Mermaid）
```mermaid
classDiagram
    class Order {
      string code
      decimal total
    }
    Order "1" --> "*" OrderItem : 包含
```
语义 / linter 见 method-abcd §3：只 泛化/关联/依赖；聚合空心◇ / 组合实心◆、菱形端=整体；默认普通关联；多重性只 `1`/`*`；类名单数名词。

### 状态机（Mermaid）
```mermaid
stateDiagram-v2
    [*] --> 待支付
    待支付 --> 已支付: 支付
    已支付 --> [*]
```

### ER（Mermaid）
```mermaid
erDiagram
    ORDER ||--o{ ORDER_ITEM : contains
```

### 活动图（PlantUML，用例规约路径视图）
```plantuml
@startuml
|执行者|
start
:输入金额;
|系统|
if (合法且余额足?) then (是)
  :扣减余额;
  :回应;
else (否)
  :提示;
endif
stop
@enduml
```

## 风格
- 标签用核心域术语、动宾；sentence case；少装饰。
- 逆向序列图用 `Note` 挂 `文件:行`（追溯）。
- 一张图只表达一个视角；跨图一致性靠 `manifest`（元模型层），别让各图自漂。
