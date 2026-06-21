---
name: abcd-view
description: |
  Render an abcd design package into a self-contained HTML viewer and report the
  path to open. model/map already auto-render; reach for this to re-render after
  hand-editing a .mmd, or to visualize a design/ package someone handed you (that
  you didn't generate). Use when asked to "view the diagrams", "render the design",
  "出图", "打开设计图", "重新渲染设计包". (abcd)
allowed-tools:
  - Bash
  - Read
  - Write
---

# /abcd-view [path]

Render a `design/` package (default `./design`) into `design/index.html`. `model` / `map` already do this automatically — use `/abcd-view` to **re-render** after you hand-edit a diagram, or to **render a package you received** but didn't generate yourself. Read `shared/references/package-spec.md` if the manifest shape is unclear.

## 1. Validate
- `manifest.json` is valid JSON; every file referenced by `diagrams[].file` / `use_cases[].spec` exists; each `code_refs` path resolves in the target project. Report any missing / dangling reference (don't silently skip).

## 2. Refresh the index README (optional)
- From `manifest`, refresh `design/README.md`: diagrams by workflow (A/B/C/D) with title + `provenance`/`level` + `gaps` — an entry point for an AI consumer. For a use-case spec missing its activity view, generate `<uc>.activity.puml` from the path steps.

## 3. Render the HTML viewer
- **Pre-render PlantUML offline first**: `bash <abcd-repo>/shared/scripts/render_plantuml.sh design` → `rendered/<id>.svg` (the `shared/` dir is in the abcd repo root, one level up from this skill folder). If `plantuml` is missing, install it so a human opening the HTML sees real diagrams, not source: macOS `brew install plantuml`, Debian `sudo apt-get install -y plantuml` (includes graphviz, needed for usecase layout); or set `PLANTUML_JAR` + java. Fully offline.
- **Then build**: `python3 <abcd-repo>/shared/scripts/build_index_html.py design` (no pip deps) → `design/index.html`: a self-teaching legend + diagrams grouped by A/B/C/D (each annotated `provenance`/`level`/`type`/`gaps`/`code_refs`) + traceability + any `uncovered_flows`. Mermaid renders client-side via CDN; the source never leaves the browser.

## 4. Package (optional)
- For single-file sharing, embed diagrams into one md, or `zip` the whole `design/`.

Output: a self-contained `design/index.html` ready to open or send to a person / another AI agent. Tell the user the path.
