# 设计包契约 (package-spec)

abcd 所有指令产出 / 消费这一份标准结构。**人**看 `rendered/*.svg`；**AI**读 `.mmd` / `.puml` 源码 + `manifest.json`。一份源，两种消费。

## 目录结构

```
design/
  README.md                 # 索引：一句话目标 + 各图导览（AI 接收方入口）
  manifest.json             # 机器可读地图（见下 schema）—— 单一事实源 / 元模型层
  00-glossary.md            # 统一语言 / 核心域术语表
  A-business/               # 正向：业务建模
    vision.md               # 愿景：老大 + 目标组织 + 量化改进目标
    usecases.puml           # 业务用例图（PlantUML）
    sequence-as-is.mmd      # 业务序列图 · 现状
    sequence-to-be.mmd      # 业务序列图 · 改进
  B-requirements/           # 正向：需求
    usecases.puml           # 系统用例图（PlantUML）
    specs/<usecase>.md            # 用例规约（结构化文本，单一源，含全部字段）
    specs/<usecase>.activity.puml # 路径段机械生成的活动图（视图）
  C-analysis/               # 正向：分析
    domain.mmd              # 分析类图 / 领域模型
    states/<entity>.mmd     # 实体状态机（可选）
  recovered/                # 逆向：设计级 as-built（与正向物理隔离）
    class.mmd
    architecture.mmd
    sequences/<flow>.mmd
    business-sequence-skeleton.mmd   # 业务序列图骨架（gap-marked，待 /abcd-model 补全）
  rendered/*.svg            # 渲染图（给人看；AI 直接读源码，无需 rendered）
```

**为什么 `A-/B-/C-` 与 `recovered/` 物理隔离**：让"需求 ≠ 设计、正向 ≠ 逆向"这条纪律落到目录上。逆向产物只在 `recovered/`，永不冒充正向的需求/业务模型。

## `manifest.json` schema

```jsonc
{
  "system": "系统名",
  "purpose": "一句话：这个系统为什么存在",
  "generated": "ISO 时间",

  "vision": {                              // A 层，正向唯一来源
    "boss": "老大（具体姓名 + 职位）",
    "organization": "目标组织",
    "goals": [{ "metric": "可度量的组织级改进指标", "baseline": "", "target": "" }]
  },
  "glossary": [{ "term": "", "definition": "", "core_domain": true }],

  "diagrams": [
    {
      "id": "biz-seq-checkout-tobe",
      "workflow": "A",                     // A|B|C|D
      "type": "business-sequence",         // usecase|business-usecase|business-sequence|system-sequence|class|state|er|architecture
      "tool": "mermaid",                   // mermaid|plantuml
      "provenance": "forward",             // forward|reverse|hybrid
      "level": "business",                 // business|requirement|analysis|design
      "phase": "to-be",                    // as-is|to-be（业务序列图专用）
      "confidence": 1.0,
      "gaps": [],                          // 逆向骨架 / hybrid 缺口，如 ["人工业务工人未知","现状缺失"]
      "file": "A-business/sequence-to-be.mmd",
      "rendered": "rendered/biz-seq-checkout-tobe.svg",
      "title": "结算下单（改进版）",
      "covers": ["uc-checkout"],           // 关联用例 id
      "code_refs": [
        { "symbol": "CheckoutController.submit", "path": "src/checkout/controller.ts", "lines": "12-88" }
      ]
    }
  ],

  "use_cases": [
    { "id": "uc-checkout", "actor": "Customer", "name": "结算下单",
      "spec": "B-requirements/specs/checkout.md",
      "realized_by": ["Order", "Payment"],     // 实现它的分析类
      "code_refs": [ /* 同上结构 */ ] }
  ],

  // 三段追溯链：用例 → 分析类 → 代码符号（支持业务↔代码双向导航）
  "traceability": [
    { "use_case": "uc-checkout", "analysis_classes": ["Order", "Payment"], "code": ["src/order/", "src/payment/"] }
  ],

  // 正向产物可直接当实现任务输入；sync 用 acceptance 验收 AI 产出
  "ai_spec": { "is_implementation_input": true, "constraints": [], "acceptance": [] }
}
```

## 三个硬字段（务必填对）

- **`provenance`** = `forward` | `reverse` | `hybrid`
- **`level`** = `business` | `requirement` | `analysis` | `design`
- **`gaps`** = 逆向骨架 / hybrid 产物的缺口清单（人工环节、现状缺失、待问询补全等）

落地规则：
- 纯逆向产物：`provenance=reverse`、`level=design`、带 `gaps`，放 `recovered/`。
- 正向产物：`provenance=forward`，放 `A-/B-/C-`。
- 对话补全的业务序列图：`provenance=hybrid`，放 `A-business/`。
- **需求层（vision / 系统用例 / 用例规约）永不 `reverse`。**

## 三段追溯链

`用例 → 分析类 → 代码符号`，由 `manifest.traceability` + 各 `diagram`/`use_case` 的 `code_refs` 承载。这让接收方（人或 AI）能从业务用例下钻到代码、也能从代码上溯到它满足的业务价值。这是"业务/技术/代码一目了然"的技术实现。
