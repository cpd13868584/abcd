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
  - AskUserQuestion
triggers:
  - 为业务建模
  - abcd 建模
  - 正向建模
  - model this business
---

# /abcd-model [--to A|B|C]

对话式走完《软件方法》ABCD 正向链：愿景（老大+组织+量化目标）→ 业务用例图 → 业务序列图（现状→改进）→ 系统用例图 + 用例规约 → 分析类图。每层从上一层推导；改进版业务序列图指向系统的每条消息 = 一个系统用例。可吃 `/abcd-recover` 的骨架作起点，再主动问询补全。

> 🚧 **WIP** — 流程实现中。方法步骤（爆炸法定老大、四种改进模式、四步曲规约、剥离与 linter）见 `shared/references/method-abcd.md`；产出结构见 `shared/references/package-spec.md`。
