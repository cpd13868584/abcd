---
name: abcd-trace
description: |
  Reverse (daily, high-frequency): one end-to-end flow → one sequence diagram
  (design level). Follow the call chain from the entry to extract the collaboration.
  Use when asked to "trace this flow", "trace the login flow",
  "画出这个流程的时序图". (abcd)
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
---

# /abcd-trace <flow> [path] [--level system|design]

The lightweight single-flow version of `/abcd-recover`: emit **one sequence diagram** (design level), no class diagram / stripping. For daily, high-frequency use.

**Two granularities** (`--level`, default `system`):
- `system` (default): lifelines = this system + external systems/services, messages = service calls / endpoints. → `sequences/<flow>.mmd`, `type=system-sequence`.
- `design`: lifelines = **internal** code modules/classes, messages = **real method calls** (pull `mod.method(args)` + returns along the call chain). → `sequences/<flow>.design.mmd`, `type=design-sequence`. Best for AI to navigate code.

Read `shared/references/diagram-syntax.md` (sequence template).

## Flow
1. Locate the flow's entry (route / handler `file:line`).
2. Follow the call chain handler → service → external system / DB into an **ordered message list** (participant → participant: does something + `file:line`); identify external participants.
3. Emit Mermaid `sequenceDiagram`: `system` → `<flow>.mmd`; `design` → `<flow>.design.mmd` (lifelines = internal classes/modules, messages = method calls). Hang `file:line` in `Note`.
4. Update / create the diagram's manifest entry (`provenance=reverse, level=design, type=system-sequence|design-sequence, code_refs`).

**Read-only**; messages = calls, faithful to code; mark "uncertain" when unsure. For a class diagram / stripping / whole module, use `/abcd-recover`.
