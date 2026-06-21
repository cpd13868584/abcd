# Changelog

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
