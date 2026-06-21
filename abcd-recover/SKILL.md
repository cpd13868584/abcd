---
name: abcd-recover
description: |
  Reverse: read code → design-level as-built (distilled OO class / data model /
  architecture / system & design sequence diagrams) + a stripped analysis-level
  domain model. Recovers the *design level* only; never fakes the requirements/business
  model. Use when asked to "recover design from code", "reverse this codebase",
  "逆向出设计包", "读代码出类图". (abcd)
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

Read code in reverse and produce a **design-level as-built** design package (+ a stripped analysis-level draft), written into the target project's `design/` (see package-spec). **Never invent the business/requirements layer from code.**

Read on demand (progressive disclosure):
- `shared/references/method-abcd.md` — §4 (stripping list, class linter, distillation), §6 (forward/reverse boundary)
- `shared/references/package-spec.md` — design-package structure + manifest schema
- `shared/references/diagram-syntax.md` — Mermaid / PlantUML templates

## Flow

### 0. Scope
Confirm the target directory; ask whether it's a **single flow** (`--flow outreach`) or a **whole module**. Prefer single flow.

### 1. Survey (hybrid: script skeleton + LLM semantics)
- **Deterministic skeleton** (run `shared/scripts/` if present, else read directly):
  - schema (SQL DDL / Drizzle / Prisma / SQLAlchemy / OpenAPI) → entities + fields + foreign keys + multiplicity.
  - route registration (controller / Hono / FastAPI / Tauri command) → entry list (method, path, handler `file:line`).
- **LLM semantics** (what scripts can't do): follow the call chain from each entry handler → service → external system / DB into an **ordered message list** (participant A → participant B: does something + `file:line`); identify external participants (DB, third parties, other services, LLMs).
- For a large codebase, survey in parallel with `Agent` (Explore). **Read-only, no edits, no invention**; mark "uncertain" when unsure.

### 2. Emit design-level artifacts → `recovered/` (provenance=reverse, level=design)
- One **system sequence diagram** per flow (Mermaid `sequenceDiagram`): participants = this system + external systems/services + actor; messages = service calls; hang `file:line` in `Note`. → `sequences/<flow>.mmd`, `type=system-sequence`.
- For key flows, also emit a **design sequence diagram (object/method level)**: open the "this system" box of the above — lifelines = internal code modules/classes, messages = **real method calls** (pull `mod.method(args)` + returns along the call chain), mark branches and idempotency/guards with `opt`/`alt`/`Note`. It is a call graph, the most faithful reverse view, the best map for AI to modify code. → `sequences/<flow>.design.mmd`, `type=design-sequence`.
- **Structure diagram (by code style, labeled honestly; recipe in method-abcd §4 three views)**:
  - **Distilled OO class diagram** (`type=class`, **hybrid**, default): attributes ← data, operations ← free functions reassigned by **Information Expert** (mark `✦`, traceable to `file:line`), relations ← FKs + signatures + call graph. → `recovered/<scope>.oo.mmd`.
  - **Data model** (`type=data-model`, reverse): schema → entities + fields + FKs, the persistence truth; **don't treat it as an OO class diagram**. → `recovered/class.mmd`.
- For a whole module, also emit an **architecture diagram** (architecture-beta / C4).

### 3. Strip → analysis-level `C-analysis/domain.mmd` (provenance=hybrid, level=analysis)
- Decontaminate per the method-abcd §4 stripping list (id / FK / status-string / timestamps / List impl / form-copied classes / perf redundancy); use the "what if removed? — 'perf problem' → delete" test.
- Apply the class-diagram linter (method-abcd §4): default plain association, no aggregate root, multiplicity only `1`/`*`, singular-noun class names, **lift domain concepts out of the polluted tables**, status → state machine (not an attribute).
- Mark entities this system doesn't own as "external, reference only".

### 4. Write manifest + README (see package-spec)
- Fill each diagram's `workflow/type/tool/provenance/level/gaps/code_refs(file:line)`.
- **gaps must honestly record what code can't give**: `"requirements layer not recovered (vision/system use case/spec) — needs /abcd-model forward"`.
- glossary (core-domain terms), traceability (use case→analysis class→code; use cases pending on reverse), `ai_spec.is_implementation_input=false`.

### 5. Boundary (hard discipline)
Reverse goes **only to the design level** + a stripped analysis draft. **Vision / system use case / use-case spec are never generated from code** — all go into `gaps`. Physically separate: reverse → `recovered/`; stripped analysis → `C-analysis/`.

### 6. Render (optional)
Mermaid: `mmdc`, or reuse gstack `/diagram`; use-case diagrams: PlantUML. Mermaid in `.md` renders natively on GitHub. For a shareable HTML viewer, run `/abcd-handoff`.

**When done**, tell the user: output is in `<target>/design/` (untracked), which `gaps` exist, and suggest `/abcd-model` to fill the requirements layer.
