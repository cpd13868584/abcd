# abcd

Turn a software system — existing code, or a fresh design discussion — into a standardized **diagram-as-code design package** that both humans (rendered diagrams) and AI agents (the `.mmd` / `.puml` source + `manifest.json`) can consume.

`abcd` packages the **ABCD modeling workflow** from 潘加宇《软件方法》(Pan Jiayu, *Software Methodology*, UMLChina) as a set of Claude Code skills. It guides you and the AI to model **business-first**, derive each layer from the one above, and emit method-correct UML/Mermaid that makes a system's business / requirements / analysis / code legible at a glance — both for humans and for the next AI agent.

> **Why "abcd":** A Business modeling · B Requirements · C Analysis · D Design — the book's four modeling workflows, and this tool's backbone.

## Prerequisites

- **Claude Code** — abcd is a set of Claude Code skills. The `/abcd-*` commands run *inside* Claude Code; this is not a standalone CLI.
- **git + bash** to install — macOS / Linux work directly; on Windows use WSL or Git-Bash.
- **python3** — for the HTML viewer generator (preinstalled on macOS and most Linux).
- Optional, for offline use-case / activity diagrams: **plantuml + graphviz** (the render step in `/abcd-map`, `/abcd-model`, or `/abcd-view` installs them if missing). Mermaid renders via a CDN, so viewing the HTML needs internet.

No API keys or accounts are required, and your code stays on your machine (only the Mermaid library is fetched from a CDN when viewing).

## Install

```bash
git clone https://github.com/cpd13868584/abcd ~/.claude/skills/abcd
cd ~/.claude/skills/abcd && ./setup
```

`setup` symlinks each `abcd-*` skill into `~/.claude/skills/` so Claude Code discovers it (portable — works from wherever you clone). Restart Claude Code or rescan skills, and the `/abcd-*` commands are available.

## Quickstart

**Model a new system (forward, dialogue-driven):**

```
/abcd-model
```

Claude walks you through A→B→C: vision → business sequence (as-is → to-be) → system use cases / specs → analysis class model, then renders the HTML viewer. Vision and requirements come from conversation (a hard rule of the method), so expect to answer questions — it is not one-button generation. Point it at existing code and it recovers the as-is (via `/abcd-map`) first, then dialogues the business *why*.

**Map an existing codebase's as-is (reverse):**

```
/abcd-map               # whole module → class / data-model / sequence diagrams + a stripped domain model
/abcd-map --flow login  # one flow → its sequence diagram(s) (--level system|design)
```

`model` and `map` both write a `design/` package **and auto-render an `index.html` viewer**. To re-render after editing a diagram, or to view a package someone sent you:

```
/abcd-view              # (re)render design/index.html — open it in a browser
```

All commands are project-agnostic: point them at any project.

## Skills

| Command | Mode | What it does |
|---|---|---|
| `/abcd-model` | forward | Dialogue-driven A→B→C modeling: vision → business sequence (as-is → to-be) → system use cases / specs → analysis class model. On existing code, recovers the as-is first. Output doubles as an AI implementation spec. Auto-renders the viewer. |
| `/abcd-map` | reverse | Read code → design-level as-built: distilled OO class diagram (attributes + operations) + data model + system & design sequence diagrams + a stripped analysis domain model. `--flow <name>` maps a single flow. Auto-renders the viewer. |
| `/abcd-view` | util | (Re)render a `design/` package into a self-contained `index.html` viewer — after hand-edits, or for a package you received. |

## Method (the important part)

Grounded in 《软件方法》's core discipline:

- **Profit = Requirements − Design.** AI collapses the cost of design/coding (D), so value moves upstream to **business modeling (A)** — exactly where this tool focuses.
- **You cannot reverse-engineer requirements from code.** Reverse recovers the *design-level* as-built only; business and requirements must be modeled forward, with you in the loop. `abcd` keeps the two physically separate (`A-/B-/C-` vs `recovered/`) and never lets reverse masquerade as requirements.
- **OO is an analysis lens, not a code-syntax property.** Even functional / data-oriented code has a latent object model: `/abcd-map` distills a true OO class diagram (attributes + operations) by reassigning free functions to their owning class via Information Expert / responsibility assignment — distinct from the raw data model.
- **Diagrams aren't drawings.** `manifest.json` is the metamodel layer that keeps every diagram one consistent, navigable model (business ↔ code).

The encoded rules live in [`shared/references/method-abcd.md`](shared/references/method-abcd.md); the package contract in [`shared/references/package-spec.md`](shared/references/package-spec.md).

## Concepts — what each diagram means

The same system is modeled at four levels (A→D); each diagram type answers a different question. Every diagram carries badges telling you its **provenance** (where it came from) and **level**.

| Diagram | Workflow | What it represents |
|---|---|---|
| Business use case | A | The value the organization delivers to its actors — business outcomes, not system features. |
| Business sequence | A | Who does what, in what order, to deliver that value. `as-is` = how it works today; `to-be` = the improved flow the system is meant to enable. |
| System use case | B | A goal a user achieves *with the system* — the contract for what to build. |
| Activity diagram | B | The basic + alternate paths of one use case (the spec's path view). |
| Domain / analysis model | C | The conceptual object model — vocabulary and relationships, implementation stripped out. |
| Class diagram (design) | D | The distilled object model: classes with attributes **and operations**, recovered from code via Information Expert / responsibility assignment. |
| Data model | D | Entities, fields and foreign keys from the schema — structure only, *not* an OO class diagram. |
| System sequence | D | One flow with each service as a black box (service ↔ service). |
| Design sequence | D | The same flow drilled into code: lifelines are modules/classes, messages are real method calls (the call graph). |

**Provenance:** `forward` = modeled with you, top-down · `reverse` = recovered from code (the as-is) · `hybrid` = recovered skeleton + modeling judgment.

Reverse only maps the flows it actually traced. When a recovered package leaves a known flow uncovered, it is declared in the manifest's `uncovered_flows` and surfaced in the HTML viewer — so a partial map never reads as the whole. The same legend is embedded at the top of every generated `index.html`.

## Credit

The methodology is from 潘加宇《软件方法》(Pan Jiayu, *Software Methodology*, UMLChina, <https://umlchina.com/book/softmeth.htm>). `abcd` is an independent tool that **encodes and applies** that method; it does not reproduce the book's text. Please support the author and buy the book.

## License

MIT — see [LICENSE](LICENSE).
