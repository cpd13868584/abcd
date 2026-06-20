# abcd

Turn a software system — existing code, or a fresh design discussion — into a standardized **diagram-as-code design package** that both humans (rendered diagrams) and AI agents (the `.mmd` / `.puml` source + `manifest.json`) can consume.

`abcd` packages the **ABCD modeling workflow** from 潘加宇《软件方法》(*Software Methodology*, UMLChina) as a set of Claude Code skills. It guides you and the AI to model **business-first**, derive each layer from the one above, and emit method-correct UML/Mermaid that makes a system's business / requirements / analysis / code legible at a glance — both for humans and for the next AI agent.

> **Why "abcd":** A 业务建模 (Business modeling) · B 需求 (Requirements) · C 分析 (Analysis) · D 设计 (Design) — the book's four modeling workflows, and this tool's backbone.

## Install

```bash
git clone https://github.com/<you>/abcd ~/.claude/skills/abcd
cd ~/.claude/skills/abcd && ./setup
```

`setup` symlinks each `abcd-*` skill into `~/.claude/skills/` so Claude Code discovers it (portable — works from wherever you clone). Restart Claude Code or rescan skills, and the `/abcd-*` commands are available.

Optional local renderers (Mermaid renders natively on GitHub; install these for offline SVG/PNG):
- Mermaid: `npm i -g @mermaid-js/mermaid-cli` — or reuse [gstack](https://github.com/garrytan/gstack) `/diagram` if installed.
- Use-case diagrams (PlantUML): `brew install plantuml`.

## Skills

| Command | Mode | What it does |
|---|---|---|
| `/abcd-model` | forward | Dialogue-driven A→B→C modeling: vision → business sequence (as-is → to-be) → system use cases / specs → analysis class model. Output doubles as an AI implementation spec. |
| `/abcd-recover` | reverse | Read code → design-level as-built (class / architecture / system-sequence diagrams) + a business-sequence skeleton. |
| `/abcd-trace <flow>` | reverse | One end-to-end flow → system sequence diagram. |
| `/abcd-sync` | gate | Check code still satisfies the forward requirements/analysis model (catch AI drift) + flag stale diagrams. |
| `/abcd-handoff` | util | Assemble README + manifest + rendered diagrams into a shareable package. |

## Method (the important part)

Grounded in 《软件方法》's core discipline:

- **利润 = 需求 − 设计** (Profit = Requirements − Design). AI collapses the cost of design/coding (D), so value moves upstream to **business modeling (A)** — exactly where this tool focuses.
- **You cannot reverse-engineer requirements from code.** Reverse recovers the *design-level* as-built only; business and requirements must be modeled forward, with you in the loop. `abcd` keeps the two physically separate (`A-/B-/C-` vs `recovered/`) and never lets reverse masquerade as requirements.
- **Diagrams aren't drawings.** `manifest.json` is the metamodel layer that keeps every diagram one consistent, navigable model (business ↔ code).

The encoded rules live in [`shared/references/method-abcd.md`](shared/references/method-abcd.md); the package contract in [`shared/references/package-spec.md`](shared/references/package-spec.md).

## Credit

The methodology is from 潘加宇《软件方法》(UMLChina, <https://umlchina.com/book/softmeth.htm>). `abcd` is an independent tool that **encodes and applies** that method; it does not reproduce the book's text. Please support the author and buy the book.

## License

MIT — see [LICENSE](LICENSE).
