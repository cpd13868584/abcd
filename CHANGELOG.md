# Changelog

## 0.6.0

- **`--only <type>` — generate a single diagram** on both commands. `/abcd-map --only class|data-model|architecture|domain|system-sequence|design-sequence` (reverse types; sequence types pair with `--flow`); `/abcd-model --only business-usecase|business-sequence|usecase|spec|analysis-class` (forward types). `/abcd-map` **refuses forward types** and points to `/abcd-model` — keeping the "requirements can't be reversed from code" boundary intact.

## 0.5.0

- **Command set simplified 5 → 3** (clearer names, less overlap): `/abcd-recover` → **`/abcd-map`** (map a codebase; `--flow` absorbs the old `/abcd-trace`); `/abcd-handoff` → **`/abcd-view`** (render/open the viewer); **`/abcd-sync` removed** (unproven drift-gate — re-add as `/abcd-check` if a real need emerges); `/abcd-trace` removed (now `/abcd-map --flow`).
- **HTML viewer is now core, not a separate "handoff" step**: `/abcd-model` and `/abcd-map` **auto-render `design/index.html`** at the end. `/abcd-view` is the standalone re-render (after hand-edits, or for a package you received). Rationale: rendered diagrams are the point for humans; the `.mmd`/`manifest` source stays the AI-facing single source of truth.
- **`/abcd-model` on existing code** now recovers the as-is (via `/abcd-map`) first, then runs the forward dialogue — instead of starting from nothing.
- **`setup` prunes stale `abcd-*` symlinks** that point into the repo but no longer exist, so renames/removals apply cleanly on update.

## 0.4.0

- **Self-teaching HTML viewer** (`build_index_html.py`): every generated `index.html` now opens with a legend — the four ABCD workflows, the core method in three lines, a one-line meaning for each diagram type *present in the package*, and what the provenance badges mean. New users (and anyone you share a package with) understand what they are looking at without opening the references.
- **`uncovered_flows` in the manifest**: reverse can now declare flows that exist in the code but were not recovered (`node` + `reason` + `code_hint`). The viewer renders them as a "Not covered yet" callout, so a partial reverse map never reads as the whole. Documented in `package-spec`; `/abcd-recover` fills it.
- **README: Concepts section** — a diagram catalog (what each type represents + who it is for) plus the provenance legend.

## 0.3.1

- **Docs in English** (`README`, all five `SKILL.md`, the four `shared/references/`, plus script comments and the HTML viewer UI). Only the book citation (潘加宇《软件方法》) and a few Chinese invocation triggers are kept — makes the skill cleanly shareable.
- **README: Prerequisites + Quickstart** added (Claude Code / python3 / optional plantuml+graphviz; new-project `/abcd-model` vs existing-code `/abcd-recover` → `/abcd-handoff`), and the Skills table refreshed for the v0.2–v0.3 features (HTML viewer, design-sequence, distilled OO class / data model).

## 0.3.0

- **Distilled OO class diagram from any code** (`/abcd-recover`): even for functional / data-oriented code, recover a true OO class diagram — attributes from data structures, **operations from free functions reassigned by Information Expert (GRASP) / responsibility assignment**, relations from FK + signatures + call graph. Distilled operations are marked `✦` and each traces to a real function (`file:line`); provenance `hybrid`. Rationale: OO is an analysis lens, not a property of the code's syntax — functional code still has a latent object model.
- **Three honest "structure" views, no more conflation** (`method-abcd` §4): (1) distilled OO class diagram (`type=class`, hybrid) — the default design class diagram; (2) data model (`type=data-model`, reverse) — entities / fields / FK from schema, never dressed up as an OO class diagram; (3) analysis domain model (stripped, conceptual). `diagram-syntax` + `package-spec` updated (`<<boundary>>`, operations, `data-model` type).

## 0.2.0

- **Design sequence diagrams (object/method level)**: `/abcd-trace --level design` and `/abcd-recover` now recover a design-level sequence whose lifelines are code modules/classes and whose messages are **real method calls** — the call graph for one flow. It's the most faithful reverse artifact (names come straight from code) and the best map for an AI to navigate and modify code. New `type: design-sequence`, file `recovered/sequences/<flow>.design.mmd`. Complements the coarser system-sequence (which keeps the system a black box).
- **as-is / to-be × level discipline** (`method-abcd` §5–6): reverse-from-code ≈ the *as-is*, but only complete at the system/design level; business-level as-is recovers just the system-touching skeleton, and any *to-be* (improvement) is forward dialogue only — modeled after plan-review-style role lenses (business-owner / engineering).
- **Self-contained HTML viewer** (`/abcd-handoff`): new `shared/scripts/build_index_html.py` generates `design/index.html` — diagrams grouped by A/B/C/D with provenance / level / type / gaps / code-ref annotations + a traceability table. Mermaid renders client-side via CDN (`mermaid@11`); the source never leaves the browser.
- **Offline PlantUML rendering**: new `shared/scripts/render_plantuml.sh` pre-renders use-case / activity diagrams to inline SVG via local `plantuml` + graphviz (fully offline, no data leaves the machine). The handoff flow installs plantuml when missing so the viewer shows real diagrams, not source dumps.

## 0.1.0 — unreleased

- Scaffold: repo structure, portable `setup` (symlinks `abcd-*` into the host skills dir), MIT license, README.
- Shared references (`shared/references/`): `package-spec.md` (design-package contract + manifest schema), `method-abcd.md` (the ABCD method encoded — constitution, business-sequence rules, use-case spec template, analysis stripping, class-diagram linter, forward/reverse boundary), `diagram-syntax.md`, `conventions.md`.
- `/abcd-recover` + `/abcd-trace`: reverse flows implemented, codified from a real dogfood (recovered a real service's email-outreach flow into design-level sequences + class diagram + a stripped analysis-level domain model).
- `/abcd-model`: forward flow implemented (A vision / business use-case / business sequence as-is→to-be → B system use-case / spec → C analysis), codified from the same dogfood; produced the full forward A/B series and a complete `design/` package (forward + reverse, cross-linked by `covers`).
- `/abcd-sync` + `/abcd-handoff`: implemented (sync = staleness diff + acceptance/constraint gate to catch AI drift; handoff = validate manifest + generate README index + render). **All five skills now have full flows.**
- Grounded in 潘加宇《软件方法》ABCD workflow.
