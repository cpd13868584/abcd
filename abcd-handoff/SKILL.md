---
name: abcd-handoff
description: |
  Utility: assemble README + manifest + rendered diagrams into a shareable,
  handoff-ready design package (incl. a self-contained HTML viewer).
  Use when asked to "package the design", "handoff this design", "打包设计包". (abcd)
allowed-tools:
  - Bash
  - Read
  - Write
---

# /abcd-handoff [path]

Assemble the `design/` package into a shareable, handoff-ready form. Read `shared/references/{package-spec.md, diagram-syntax.md}`.

## 1. Validate
- `manifest.json` is valid JSON; every file referenced by `diagrams[].file` / `use_cases[].spec` exists; each `code_refs` path resolves in the target project.
- Report any missing / dangling references.

## 2. Generate the index README
- From `manifest`, generate / refresh `design/README.md`: list diagrams by workflow (A/B/C/D) with title + `provenance`/`level` + `gaps`, giving an AI consumer an entry point.
- For a use-case spec missing its activity-diagram view, generate `<uc>.activity.puml` from the path steps.

## 3. Generate the HTML viewer (human-facing visualization, recommended)
- **Pre-render PlantUML offline first**: `bash <skill-dir>/shared/scripts/render_plantuml.sh design` → `rendered/<id>.svg`. **If `plantuml` is missing, install it** (so a human opening the HTML sees real diagrams, not source — source is slow for humans to read): macOS `brew install plantuml`, Debian `sudo apt-get install -y plantuml` (includes graphviz, required for usecase layout); or set `PLANTUML_JAR` + java. Fully offline; diagram data never leaves the machine.
- **Then build the HTML**: `python3 <skill-dir>/shared/scripts/build_index_html.py design` (no pip deps) → `design/index.html`: grouped by A/B/C/D, each diagram annotated with `provenance`/`level`/`type`/`gaps`/`code_refs` + a traceability table.
- Mermaid renders client-side via CDN (`mermaid@11`), source never leaves the browser; PlantUML uses the `rendered/<id>.svg` from the previous step **inlined** (falls back to folded source only if rendering didn't succeed).
- Self-contained single file, ready to send to a person or another AI agent (like gstack `plan-design-review`'s HTML output).

## 4. Render (optional; PlantUML pre-render + offline SVG)
- `.mmd` → `rendered/*.svg` (`mmdc`, or reuse gstack `/diagram`); `.puml` → svg (`plantuml.jar`). A missing renderer only warns (GitHub renders mermaid natively; the HTML viewer uses CDN).

## 5. Package (optional)
- For single-file sharing, embed the diagrams into one md; or `zip` the whole `design/`.

Output: a complete, renderable, navigable (manifest-linked) `design/`, ready to hand to a person or another AI agent.
