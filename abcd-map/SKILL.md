---
name: abcd-map
description: |
  Reverse: read code → map an existing codebase into a design-level as-built
  package (distilled OO class / data model / architecture / system & design
  sequence diagrams) + a stripped analysis-level domain model, then auto-render an
  HTML viewer. Recovers the *design level* only; never fakes the requirements/
  business model. `--flow <name>` maps a single end-to-end flow. Use when asked to
  "map this codebase", "reverse this code", "analyze the as-is", "逆向出设计包",
  "读代码出类图", "画出这个流程的时序图". (abcd)
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
  - Write
  - Agent
  - AskUserQuestion
---

# /abcd-map [path] [--flow <name>] [--level system|design]

Read code in reverse → a **design-level as-built** package (+ a stripped analysis-level draft) under the target project's `design/`, then **auto-render the HTML viewer**. **Never invent the business/requirements layer from code.**

Read on demand (progressive disclosure):
- `shared/references/method-abcd.md` — §4 (stripping list, class linter, distillation), §6 (forward/reverse boundary)
- `shared/references/package-spec.md` — design-package structure + manifest schema
- `shared/references/diagram-syntax.md` — Mermaid / PlantUML templates

## Scope: whole module vs single flow
- **`--flow <name>`** (lightweight, high-frequency): map just one end-to-end flow → its sequence diagram(s); skip class/stripping. The common daily case.
- **no `--flow`** (whole module): the full package below.
- **`--level system|design`** picks sequence granularity (for a flow, default emits both): `system` = service ↔ service black box; `design` = internal modules/classes + real method calls.

## Flow (whole module)

### 1. Survey (hybrid: script skeleton + LLM semantics)
- **Deterministic skeleton** (run `shared/scripts/` if present, else read directly): schema (SQL DDL / Drizzle / Prisma / SQLAlchemy / OpenAPI) → entities + fields + foreign keys + multiplicity; route registration (controller / Hono / FastAPI / Tauri command) → entry list (method, path, handler `file:line`).
- **LLM semantics** (what scripts can't do): follow the call chain from each entry handler → service → external system / DB into an **ordered message list** (participant A → participant B: does something + `file:line`); identify external participants (DB, third parties, other services, LLMs).
- For a large codebase, survey in parallel with `Agent` (Explore). **Read-only, no edits, no invention**; mark "uncertain" when unsure.

### 2. Emit design-level artifacts → `recovered/` (provenance=reverse, level=design)
- One **system sequence diagram** per flow (Mermaid `sequenceDiagram`): participants = this system + external systems/services + actor; messages = service calls; hang `file:line` in `Note`. → `sequences/<flow>.mmd`, `type=system-sequence`.
- For key flows, also a **design sequence diagram (object/method level)**: open the "this system" box — lifelines = internal code modules/classes, messages = **real method calls** along the call chain, mark branches / idempotency / guards with `opt`/`alt`/`Note`. It is a call graph — the most faithful reverse view, the best map for an AI to modify code. → `sequences/<flow>.design.mmd`, `type=design-sequence`.
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
- **Declare uncovered flows**: if you recovered some flows but others plainly exist in the code (other nodes / endpoints / jobs), list them in `manifest.uncovered_flows` (`node` + `reason` + `code_hint`) so a partial map never reads as the whole — the viewer renders them as a "Not covered yet" callout.
- glossary (core-domain terms), traceability (use case→analysis class→code; use cases pending on reverse), `ai_spec.is_implementation_input=false`.

### 5. Boundary (hard discipline)
Reverse goes **only to the design level** + a stripped analysis draft. **Vision / system use case / use-case spec are never generated from code** — all go into `gaps`. Physically separate: reverse → `recovered/`; stripped analysis → `C-analysis/`.

### 6. Auto-render the viewer (always — diagrams are for humans to see, don't stop at source files)
- Pre-render PlantUML offline: `bash <abcd-repo>/shared/scripts/render_plantuml.sh design` (the `shared/` dir is in the abcd repo root, one level up from this skill folder). If `plantuml` is missing, install it (`brew install plantuml` / `apt-get install -y plantuml`, includes graphviz) so use-case/activity diagrams render as images, not source.
- Build the viewer: `python3 <abcd-repo>/shared/scripts/build_index_html.py design` → `design/index.html` (no pip deps; Mermaid renders client-side via CDN, source never leaves the browser).
- Tell the user the path to open. Re-render later (after hand-editing a `.mmd`, or to view a package someone sent you) with `/abcd-view`.

**Single flow (`--flow`)**: do steps 1–2 for that flow only (its sequence diagram(s)), add/refresh its manifest entry, then step 6. Skip 3–5.

**When done**, tell the user: output is in `<target>/design/` (untracked) + `index.html` to open, which `gaps` / `uncovered_flows` remain, and suggest `/abcd-model` to add the requirements layer (the business *why*, which code can't give).
