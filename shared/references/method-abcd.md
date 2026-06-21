# abcd method reference (method-abcd)

A condensed encoding of the ABCD workflow from 潘加宇《软件方法》(Pan Jiayu, *Software Methodology*, UMLChina), serving as the shared rule source for every abcd command (progressive disclosure: SKILL.md references this file on demand). For deeper UML semantics, defer to the book: <https://umlchina.com/book/softmeth.htm>. This file encodes rules; it does not reproduce the book's text.

---

## 0. Three constitutional rules (every command obeys)

1. **Profit = Requirements − Design.** Requirements = "sells well" (stakeholder view: package functions for the system); Design = "low cost" (internal view: partition by coupling/cohesion). Neither derives from the other; they are not one-to-one.
2. **AI collapses D; value moves up to ABC (especially A).** In the ABC workflows AI is not yet an "expert" — only a very smart student. Use this method to **detoxify** and guide it.
3. **You cannot reverse-engineer requirements / business from code.** What reverse gives is inherently **design-level** and polluted with non-core-domain noise. Whether a use case should exist, whether a relation is generalization or association, whether it is composition — judge from **domain logic, not from code**.

---

## 1. ABCD and the derivation discipline

| Workflow | One line | Sharper name |
|---|---|---|
| A Business modeling | Locate the target organization to improve + the problem it most needs fixed | Organization improvement |
| B Requirements | The overall behavior the system-to-be must have | System responsibility |
| C Analysis | The core-domain mechanism the system must encapsulate | Core-domain logic |
| D Design | Map the core-domain mechanism to an implementation | Implementation |

**Each layer derives from the one above.** Core engine (A→B): draw the business sequence **as-is** → apply the improvement patterns → **to-be** → on the to-be, **every message pointing at the system-to-be = one system use case**.

The book leans on 5 diagrams, 3 of them core: **use-case diagram / class diagram / sequence diagram**.

---

## 2. A — Business modeling

### Vision (`A-business/vision.md`)
**Boss + target organization + quantified improvement goal.**
- The **boss (老大)** = the representative of the target organization, **one concrete person** (name + title) whose interest the system serves first. Pin the boss with the **"explosion" test**: if you could pitch the system to only one person and say only one sentence, that person / that sentence is the boss / the vision. Your own team lead is not the boss (they are "the one who decides the boss").
- The **goal** = a measurable improvement to **organization behavior** (not a system feature, not a quality requirement). Drill an adjective down to a metric ("convenient" → average number of operations to complete one order).

### Business use-case diagram (PlantUML `usecase`)
The organization's "value to the outside" view. Elements: **business actor** (outside the organization, beyond the boundary), **business use case** (= the value an actor gets from the organization, ellipse), **boundary box** (marks which organization is under study; beginners must draw it).
- Business workers and business entities **do not appear** on the business use-case diagram (they are cost, not value).
- Business use-case names **forbid** system-flavored words like add/view/enter/query/edit/configure ("query XX" → "understand XX").

### Business sequence diagram (Mermaid `sequenceDiagram`) — the flagship
The "organization collaborating internally via the system" view.
- **Only three kinds of participant**: business worker `«business worker»`, business entity `«business entity»` (incl. existing software systems, ATMs and other non-human intelligent systems), and **time**. Name as `:role`.
- **A message = responsibility assignment, not a data flow**: verb-object, **never write the word "request"**, **never draw return messages**; data is only an input/output parameter.
- **The system is always a black box**: draw only its messages with the outside, **never its internal components / internal steps**.
- Non-intelligent things (forms/paper) cannot be participants, only message **parameters**.
- Branch / loop with `opt` / `loop` / `alt`.
- **The as-is must be faithful** (drawn from on-site observation) — it is the basis for improvement.

**Four improvement patterns** (apply each when deriving to-be from as-is):
1. **Physical flow → information flow**: extract the valuable information from physical things and exchange it via software (little room left here).
2. **Improve information flow**: poor multi-system communication → introduce a system in the middle to coordinate, cutting human/system interactions.
3. **Encapsulate domain logic**: distill the expert's judgment/calculation into the system (hardest; the most room today).
4. **Abu method (阿布思考法)**: first assume unlimited resources and draw the perfect plan, then "knock it off" with the resources you actually have.

→ On the to-be business sequence diagram, **every message pointing at the system-to-be → one system use case**.

---

## 3. B — Requirements

### System use-case diagram (PlantUML `usecase`)
- **Actor** = the objects with a **solid line to the system under study** in the business sequence diagram (no separate brainstorm needed). Actor ≠ "user" ≠ importance; someone who only receives information and need not consciously respond is a **stakeholder**, not an actor.
- Use-case names are **verb-object**, drop the subject, avoid weak verbs ("perform invoice voiding" → "void invoice").
- Primary actor → use case (initiates); secondary actor ← use case (passive, must "consciously participate in the response").
- **include** = factor a "**step set**" shared by multiple use cases and self-contained as a small goal into an included use case (many→one, called in the body with 【bold brackets】, like a private operation). Use **extend** sparingly (it is not "A then maybe B/C"). Multiple actors at one use case → **split into separate use cases**; don't reuse via a generalized "user".
- Don't draw use-case diagrams for subsystems/components/modules.
- **Anti-patterns**: the CRUD quartet, "manage XX" use cases (both reverse requirements from DB tables/design); treating a step as a use case ("log in" is not a use case).

### Use-case spec (hybrid: structured text as source + generated activity-diagram view)
`specs/<uc>.md` holds **all fields**:
- **Actors** (mark primary/secondary).
- **Pre / post-conditions** = **system-detectable states** (not actions); "already logged in" is not a precondition (see include).
- **Stakeholder interests**: use the "drunk" test to find stakeholders; four sources = human actors / upstream / downstream / the owner of the information (most easily missed). Write each interest **differently, with concrete pain**.
- **Basic path** = **four steps**: request (always) / validate / change / respond. One sentence per step; write only what the system can sense and promise; **the subject can only be the primary actor or the system** (no "frontend requests backend" — even a system spanning a hundred countries is just the word "system" in requirements); use core-domain terms; no UI/interaction detail.
- **Extension paths**: numbered `Na` / `Na1` (step number + letter); collect only "**exceptions the system can sense and must handle**".
- **Supplementary constraints**, four kinds:
  - field list (data-dictionary notation `+ () {} [|]`, write until stakeholders agree; **do not paste a data-model diagram**)
  - business rules (computational rules stakeholders "can't do without", not implementation algorithms)
  - quality requirements (usability/performance/reliability/supportability, **must be measurable**)
  - design constraints (also written from the stakeholder view)
- **Ultimate test**: **"can't do without it" = a requirement**; "this also works" is not.

**Generated view**: mechanically convert the basic + extension paths into a PlantUML activity diagram (each step → action node, each `Na` → decision branch, swimlanes `actor|system`). Text is the single source; the activity diagram is a rendered view, not maintained by hand.

### Contracts (for parallel implementation, optional)

The use-case spec **is** the contract (pre/post + paths + supplementary constraints). When several people / agents implement parts **in parallel**, extract a focused **contract** per use case or service boundary so the independent pieces still fit — it is a *synthesis* of existing artifacts, not new invention:
- **Interface**: the boundary messages / signatures (pull from the system & design sequences).
- **Pre/post-conditions** (from the spec) + **invariants / business rules** (from supplementary constraints).
- **State-transition contract**: which actor may move the entity to which state (from the `state` machine).
- **Acceptance** as Given/When/Then (from `ai_spec.acceptance` + the basic/extension paths).

→ `B-requirements/contracts/<uc>.md`, `type=contract`. **Skip it for solo, sequential implementation** — the spec + analysis model + sequences already suffice (`ai_spec.is_implementation_input=true`). Add it only when parallel/independent implementation makes the inter-part interface the bottleneck.

---

## 4. C — Analysis

### Analysis / domain class diagram (Mermaid `classDiagram`)
- Centered on **entity classes** (boundary/control classes map mechanically by formula, can be deferred).
- **Analysis = zero time, infinite resources.** The test for "analysis vs design" is **performance/time**: for each element ask "what if I remove it? — if the answer is 'there'd be a performance problem', delete it from the analysis model."

**Reverse downgrade (design-level → analysis-level) stripping list**: remove ① object ID / identity attributes ② foreign keys ③ attributes literally named "status" ④ List/array multi-value implementations ⑤ classes copied straight from forms/cards ⑥ redundancy added for performance. Then re-run the "performance" test above.

### Class-diagram linter (hard semantics, fix on sight)
- **Only three relations: generalization / association / dependency.**
- Aggregation (hollow diamond) / composition (filled diamond) are **subtypes of association**, diamond end = the whole. Composition's two constraints: a part belongs to only one whole at a time; destroying the whole destroys the parts.
- **Default to plain association; no composition/aggregation without sufficient evidence**; **do not mark an aggregate root, do not circle aggregate boundaries** (the book deems these redundant/wrong concepts).
- **Multiplicity only on associations**, default to just `1` and `*`; **generalization has no multiplicity**.
- Generalization = set-inclusion semantics; subclasses are **disjoint by default**, completeness not required; no (indirect) reflexive generalization.
- **Dependency** appears only in sequence diagrams (which scenario/step/call); a pure domain class diagram **draws no dependency**.
- Naming: **singular noun**; no redundant suffix like "class/info/record/table", no ID/status attribute, attribute names don't repeat the class name; use core-domain terms ("plain language").
- Associations: **prefer a role name (noun)**; direction follows "whose state the system is more responsible for / interested in" (note an RDB foreign key may point the opposite way, and the association-name reading arrow ≠ navigation direction); an association is a relation the system **must remember** — if it can be computed by a rule (e.g. string containment), don't model it.
- **Low-value signals**: a class diagram that looks like a use-case diagram ("customer—query—product"); pseudo-OO classes full of `-er/Strategy/Rule/Algorithm` with operations but no attributes.

### Distilling class diagrams from code (three reverse views + Information Expert)

When reversing "structure", produce three views by code style and **label them honestly, never conflate**:
1. **Distilled OO class diagram** (`type=class`, provenance=**hybrid**, level=design) — **producible from any code**, the default "design class diagram". Attributes ← data structures; **operations ← free functions/handlers reassigned by «Information Expert (GRASP) / responsibility assignment»** (whoever owns the data owns the operation, `recordSentEmail()` → `EmailMessage.record()`); associations ← foreign keys + entities co-occurring in function signatures; dependencies ← the call graph. Honesty rules: reassignment involves modeling judgment → mark `hybrid`; mark distilled operations with `✦` (they are free functions in the code); every operation traces to a real function `file:line`. **OO is an analysis lens, not a code-syntax property — functional / data-oriented code still has a latent object model; distill it.**
2. **Data model** (`type=data-model`/`er`, reverse, design) — schema/ORM → entities + fields + foreign keys, the persistence truth. **Do not treat it as an OO class diagram** (no operations; FK direction ≠ association direction).
3. **Analysis domain model** (hybrid, analysis) — downgrade from ① by applying the class-diagram linter + stripping list: remove id/FK/status-string/**implementation operations**, name conceptually (= pure domain concepts).

---

## 5. D — Design

**Forward**: at the design level "**code is the representation**", **draw no UML by default** — build a good analysis model → customize a regular "analysis→design" mapping → tool/AI/human map by the rules; draw only a few **representative classes/use cases** to demonstrate the pattern, not everything.

**Reverse / navigation** (high value in the AI era): reliably recover three **design-level** diagrams from code to help humans and AI navigate the implementation —
- **Class diagram (structure)**: as-built entities + fields (incl. id/FK/status/JSON), i.e. the design level before the §4 stripping.
- **System sequence diagram (coarse interaction)**: lifelines = this system + external systems/services (DB / third parties / other services), messages = service calls / endpoints. Answers "which systems does this flow touch".
- **Design sequence diagram (object/method level)**: lifelines = **internal** code modules/classes, messages = **real method calls** (`mod.method(args)` + returns). Answers "how this flow advances step by step in the code". It is essentially a **call graph**, the **most faithful reverse artifact** (method names come straight from code, nothing invented), and the best map for AI to modify code along the functions.
  - The system sequence treats the system as one box; the design sequence **opens the box** into internal object collaboration — the two complement each other for the same flow.
  - Hang `file:line` in `Note`; branch with `opt`/`alt`/`loop`; mark idempotency/guard/exception branches with `Note`. `type=design-sequence`, file `recovered/sequences/<flow>.design.mmd`.

---

## 6. Forward vs reverse boundary (hard discipline)

**Mindset (as-is vs to-be)**: reversing code ≈ getting the **as-is** — but complete only at the **system/design level** (class / system-sequence / design-sequence / architecture = "what the code looks like now"); the **business-level as-is** can only be reversed as a "skeleton touching the system", while the manual / offline / verbal parts are not in the code and must be filled by dialogue. **The to-be (improvement) at any level is not in the code** — it can only be obtained by **forward dialogue**, like `plan-ceo-review` / `plan-eng-review` repeatedly probing from the "business-owner / engineering" lenses. In one line: **system as-is = reverse; improvement + business intent = forward dialogue.**

| Artifact | Forward (dialogue / human-provided) | Reverse (read code) |
|---|---|---|
| Vision / boss / quantified goal | ✓ sole source | ✗ |
| Business use-case diagram | ✓ | ✗ |
| Business sequence diagram | ✓ complete | **hybrid**: reverse a skeleton (system↔external interactions, entry as a generalized actor) → the agent actively asks / suggests to complete the manual / as-is / to-be parts |
| System use-case diagram / use-case spec | ✓ | ✗ |
| Analysis class diagram | ✓ clean analysis-level | ⚠ comes out design-level, needs stripping (§4) |
| Architecture / system-sequence / design-sequence (object·method level) / class diagram | — (D draws no UML by default; forward goes straight to code) | ✓ design-level as-built reliably recoverable; design-sequence = call graph, most faithful |

Mark reverse artifacts `provenance: reverse` / `level: design` / `gaps`, place them in `recovered/`. **The requirements layer is never reversed.** Reverse **must not invent**: extract only from real artifacts (schema→ER/class diagram, routes→system sequence, integration points→business-sequence skeleton); fabricate nothing without evidence.

---

## 7. Tooling and "modeling vs drawing"

- Backbone **Mermaid** (class/sequence/state/ER); **use-case diagram = PlantUML** (Mermaid has no native usecase; PlantUML is the default representation AI generates UML in). The use-case-spec activity-diagram view = PlantUML.
- **`manifest.json` is the metamodel layer**: it strings every diagram/use-case/class/code together by id into one consistent, navigable model, avoiding the "each diagram independent and inconsistent" — **drawing instead of modeling** — failure mode. For every diagram you write, ask "did it add value?" — especially in the AI era.
