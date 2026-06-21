# conventions

## Naming
- Diagram id: `<type>-<slug>`, e.g. `seq-outreach-send`, `class-asbuilt`, `domain-analysis`.
- File layout: see `package-spec.md`; use-case spec at `B-requirements/specs/<usecase>.md` (+ generated `<usecase>.activity.puml`).
- Class / attribute naming discipline: see `method-abcd.md` §4 (singular noun, no redundant suffix, core-domain terms).

## Code links (the traceable map)
- Every diagram / use_case carries `code_refs: [{symbol, path, lines}]`: `path` relative to the target project root, `lines` as `start-end`.
- Next to a sequence-diagram message, hang `file:line` in a `Note`; add a Mermaid `click` to jump where possible.
- `manifest.traceability` strings `use case → analysis class → code`, supporting business ↔ code drill-down both ways.

## provenance / level / gaps (mandatory on reverse)
- `provenance`: `forward` (dialogue) | `reverse` (read code) | `hybrid` (reverse skeleton → completed by dialogue).
- `level`: `business` | `requirement` | `analysis` | `design`.
- Pure reverse → `recovered/` (reverse + design); stripped analysis → `C-analysis/` (hybrid + analysis).
- **`gaps` honestly records what code can't give**: the requirements layer, manual / offline steps, the full as-is.
- **Hard discipline**: the requirements layer (vision / system use case / spec) is never `reverse`; fabricate nothing without evidence.

## Rendered artifacts
- `rendered/*.svg` are human-facing derivatives, safe to `.gitignore`; AI reads the source.
