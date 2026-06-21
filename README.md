# abcd

Turn a software system — existing code, or a fresh design discussion — into a standardized **diagram-as-code design package** that both humans (rendered diagrams) and AI agents (the `.mmd` / `.puml` source + `manifest.json`) can consume.

`abcd` packages the **ABCD modeling workflow** from 潘加宇《软件方法》(Pan Jiayu, *Software Methodology*, UMLChina) as a set of Claude Code skills. It guides you and the AI to model **business-first**, derive each layer from the one above, and emit method-correct UML/Mermaid that makes a system's business / requirements / analysis / code legible at a glance — both for humans and for the next AI agent.

> **Why "abcd":** A Business modeling · B Requirements · C Analysis · D Design — the book's four modeling workflows, and this tool's backbone.

## Prerequisites

- **Claude Code** — abcd is a set of Claude Code skills. The `/abcd-*` commands run *inside* Claude Code; this is not a standalone CLI.
- **git + bash** to install — macOS / Linux work directly; on Windows use WSL or Git-Bash.
- **python3** — for the HTML viewer generator (preinstalled on macOS and most Linux).
- Optional, for offline use-case / activity diagrams: **plantuml + graphviz** (the `/abcd-handoff` flow installs them if missing). Mermaid renders via a CDN, so viewing the HTML needs internet.

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

Claude walks you through A→B→C: vision → business sequence (as-is → to-be) → system use cases / specs → analysis class model. Vision and requirements come from conversation (a hard rule of the method), so expect to answer questions — it is not one-button generation.

**Analyze an existing codebase's as-is (reverse):**

```
/abcd-recover           # whole module → class / data-model / sequence diagrams + a stripped domain model
/abcd-trace <flow>      # one flow → a sequence diagram (--level system|design)
```

**See the diagrams:**

```
/abcd-handoff           # → design/index.html — open it in a browser
```

Both modes are project-agnostic: point them at any project.

## Skills

| Command | Mode | What it does |
|---|---|---|
| `/abcd-model` | forward | Dialogue-driven A→B→C modeling: vision → business sequence (as-is → to-be) → system use cases / specs → analysis class model. Output doubles as an AI implementation spec. |
| `/abcd-recover` | reverse | Read code → design-level as-built: distilled OO class diagram (attributes + operations) + data model + system & design sequence diagrams + a stripped analysis domain model. |
| `/abcd-trace <flow>` | reverse | One end-to-end flow → one sequence diagram (`--level system\|design`). |
| `/abcd-sync` | gate | Check code still satisfies the forward requirements/analysis model (catch AI drift) + flag stale diagrams. |
| `/abcd-handoff` | util | Assemble a self-contained `index.html` viewer + README + rendered diagrams into a shareable package. |

## Method (the important part)

Grounded in 《软件方法》's core discipline:

- **Profit = Requirements − Design.** AI collapses the cost of design/coding (D), so value moves upstream to **business modeling (A)** — exactly where this tool focuses.
- **You cannot reverse-engineer requirements from code.** Reverse recovers the *design-level* as-built only; business and requirements must be modeled forward, with you in the loop. `abcd` keeps the two physically separate (`A-/B-/C-` vs `recovered/`) and never lets reverse masquerade as requirements.
- **OO is an analysis lens, not a code-syntax property.** Even functional / data-oriented code has a latent object model: `/abcd-recover` distills a true OO class diagram (attributes + operations) by reassigning free functions to their owning class via Information Expert / responsibility assignment — distinct from the raw data model.
- **Diagrams aren't drawings.** `manifest.json` is the metamodel layer that keeps every diagram one consistent, navigable model (business ↔ code).

The encoded rules live in [`shared/references/method-abcd.md`](shared/references/method-abcd.md); the package contract in [`shared/references/package-spec.md`](shared/references/package-spec.md).

## Credit

The methodology is from 潘加宇《软件方法》(Pan Jiayu, *Software Methodology*, UMLChina, <https://umlchina.com/book/softmeth.htm>). `abcd` is an independent tool that **encodes and applies** that method; it does not reproduce the book's text. Please support the author and buy the book.

## License

MIT — see [LICENSE](LICENSE).
