---
name: abcd-model
description: |
  Forward (flagship): dialogue-driven A→B→C business modeling — vision → business
  use-case / sequence (as-is → to-be) → system use cases / specs → analysis class model.
  The output doubles as the spec that drives AI to write code (D); `--only <type>`
  produces a single forward diagram. Use when asked to "model this business",
  "abcd model", "forward modeling", "为业务建模", "正向建模". (abcd)
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

# /abcd-model [--to A|B|C] [--only <type>] [path]

Walk 潘加宇《软件方法》 ABCD forward and in dialogue: A business modeling → B requirements → C analysis. **Each layer derives from the one above**; the output is the spec that drives AI to write D. When code already exists, **first run `/abcd-map`** to recover the design-level as-is, then take those assets as a **reference starting point** (don't let the forward model drift from the implementation).

Read on demand: `shared/references/method-abcd.md` (§2 A, §3 spec template, §4 class linter, §6 boundary), `package-spec.md`, `diagram-syntax.md`.

## A — Business modeling
- **A1 Vision (dialogue — only a human can answer)**: business intent is not in the code. Use the **"explosion" test** to pin the **boss** (whom the system serves first; a concrete person/role, **not** the team lead); set the **target organization** + **quantified improvement goal** (a metric on org behavior, not a system feature). First harvest existing design docs (docs/), **ask the user for what's missing**; mark drafts `to-confirm`, don't decide for the boss. → `A-business/vision.md` + `manifest.vision`.
- **A2 Business use-case diagram** (PlantUML usecase): the org's value to the outside. Business actor (beyond the boundary) → business use case (= value); business workers/entities **stay off the diagram**. → `A-business/usecases.puml`.
- **A3 Business sequence diagram** (Mermaid) **as-is → to-be** — the flagship:
  - The as-is is **faithful** (on-site / read docs / ask people); with code present you can first `/abcd-map` the "skeleton touching the system", then fill the manual/offline/verbal parts; participants are only business worker / business entity / time; message = responsibility (no "request", no returns).
  - **The to-be comes from forward dialogue** — apply the **four improvement patterns**, and like `plan-ceo-review` / `plan-eng-review` probe repeatedly from the "business-owner / engineering" lenses and make suggestions, without deciding for the boss; **every to-be message pointing at the system-to-be = one system use case**.
  → `A-business/sequence-as-is.mmd` + `sequence-to-be.mmd`.

## B — Requirements
- **B1 System use-case diagram** (PlantUML usecase): actors = the objects with a solid line to the system in the to-be business sequence; use-case names are verb-object; primary actor → use case, secondary actor ← use case. → `B-requirements/usecases.puml`.
- **B2 Use-case spec** (hybrid, text is the source): pre/post-conditions = detectable states; stakeholder interests; basic path **four steps** (request/validate/change/respond); extensions `Na`/`Na1`; four kinds of supplementary constraint. Test: **"can't do without it"**. → `specs/<uc>.md`, with `<uc>.activity.puml` generated from the path steps.
- **B3 Contract** (optional, for parallel work): synthesize a per-use-case contract — interface (messages/signatures from the sequences) + pre/post + invariants + state-transition rules + Given/When/Then acceptance. A *synthesis* of spec + sequences + `ai_spec`, **not** new invention; **skip for solo, sequential implementation**. → `contracts/<uc>.md`, `type=contract` (see method-abcd §3).

## C — Analysis
- **C1 Analysis class diagram** (Mermaid): distill entity classes from the spec's nouns/events; apply the class-diagram linter (method-abcd §4); cross-check against `/abcd-map`'s `C-analysis/` draft if present. → `C-analysis/domain.mmd`.

## Wrap-up
- Write the manifest (see package-spec): `vision`, each diagram's `provenance=forward`/`level`, `use_cases`, `traceability` (use case→analysis class→code), `ai_spec.is_implementation_input=true` (`constraints`/`acceptance` as the implementation contract).
- **Auto-render the viewer** (always — the diagrams are for humans to see): `bash <abcd-repo>/shared/scripts/render_plantuml.sh design` then `python3 <abcd-repo>/shared/scripts/build_index_html.py design` → `design/index.html` (the `shared/` dir is in the abcd repo root, one level up from this skill folder; install `plantuml` if missing so use-case diagrams render as images). Tell the user the path; re-render later with `/abcd-view`.
- **Scope flags**: `--to A|B|C` stops at a layer; **`--only <type>`** produces a single forward artifact — `business-usecase` · `business-sequence`(`:as-is`|`:to-be`) · `usecase` · `spec` · `analysis-class` · `contract` — gathering only that artifact's prerequisite context by dialogue (don't fabricate), then rendering.
- **Dialogue discipline**: A's vision / stakeholder interests **must be asked, never invented**; mark `gap` for what code/docs can't give; don't decide for the boss.
