---
name: abcd-sync
description: |
  Gate: ① diagram vs code (catch stale docs) ② code vs the forward
  requirements/analysis model (catch AI drift, via ai_spec.acceptance).
  Use when asked to "sync design with code", "check code against the model",
  "校验代码是否跑偏". (abcd)
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - AskUserQuestion
---

# /abcd-sync [path]

A two-way acceptance gate between the design package and the code. Read `shared/references/package-spec.md` (manifest fields).

## 1. Diagram vs code (catch staleness)
- For `manifest.diagrams` with `provenance=reverse`, re-read the current code per their `code_refs` (schema / routes / call chain) and diff against the diagram:
  - entity / field / FK changed → class diagram stale; route / call chain changed → system sequence stale; `code_refs` line drift → needs update.
- Produce a **stale list** (which diagram, where it diverges, suggestion: re-run `/abcd-recover` for that diagram, or fix the code).

## 2. Code vs forward model (catch AI drift) — high value in the AI era
- Check each `manifest.ai_spec.acceptance` and `constraints` item still holds in the code (locate the relevant code via `traceability` / `code_refs`, read / grep to verify).
- Check the `traceability` links (use case→analysis class→code) still resolve (files / symbols still exist).
- Give **pass / fail + evidence (file:line)** per item; fail = code has drifted from the forward requirements / analysis model (AI may have gone off, or the requirement should update).

## 3. Report
Output a sync report: stale-diagram list + acceptance / constraint pass status + suggested actions (update diagram / fix code / go back to `/abcd-model` to change the model). **Does not auto-edit code**; mark "uncertain" when unsure and let a human decide.
