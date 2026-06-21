#!/usr/bin/env python3
"""abcd: build a self-contained design/index.html viewer from manifest.json.

- Mermaid diagrams (.mmd) render client-side via CDN — the source never leaves the
  browser, so internal designs stay private.
- PlantUML diagrams (.puml) inline a pre-rendered rendered/<id>.svg if present,
  otherwise the source is shown in a collapsible block (install plantuml to pre-render).

No third-party pip deps. Usage:
    python3 build_index_html.py [design_dir]   # default: ./design, else .
"""
import json
import sys
import html
import pathlib
import re

WF = {
    "A": "A · Business modeling",
    "B": "B · Requirements",
    "C": "C · Analysis",
    "D": "D · Design / Reverse",
}

WF_GLOSS = {
    "A": "model the business value &amp; flow first — where AI shifts the value.",
    "B": "system use cases &amp; specs, derived from the business.",
    "C": "the conceptual object / domain model.",
    "D": "design-level structure &amp; sequences, including what is recovered from code.",
}

# One-line meaning per diagram type — shown in the legend only for the types present.
TYPE_GLOSS = {
    "business-usecase": "Business use case — the value the organization delivers to its actors (outcomes, not system features).",
    "business-sequence": "Business sequence — who does what, in what order, to deliver that value. as-is = how it works today; to-be = the improved flow the system enables.",
    "usecase": "System use case — a goal a user achieves with the system; the contract for what to build.",
    "activity": "Activity diagram — the basic + alternate paths of one use case (the spec's path view).",
    "domain-model": "Domain model — the conceptual vocabulary of the problem (analysis-level, implementation stripped out).",
    "class": "Class diagram — the object model: classes with attributes, operations &amp; relationships. Analysis = conceptual; design = distilled from code (operations included).",
    "data-model": "Data model — entities, fields &amp; foreign keys from the schema. Structure only, no behaviour — not an OO class diagram.",
    "system-sequence": "System sequence — one flow with each service as a black box (service ↔ service).",
    "design-sequence": "Design sequence — the same flow drilled into code: lifelines are modules/classes, messages are real method calls (the call graph).",
    "state": "State machine — an entity's lifecycle: states + allowed transitions (and who may trigger each). A status field belongs here, not as a class attribute.",
    "contract": "Contract — interface + pre/post-conditions + Given/When/Then acceptance at a use-case / service boundary, synthesized from spec + sequences. Lets people / agents implement parts in parallel and still fit together.",
}


def read(p: pathlib.Path):
    try:
        return p.read_text(encoding="utf-8")
    except Exception:
        return None


def badge(text, kind=""):
    if text is None or text == "":
        return ""
    return f'<span class="badge {kind}">{html.escape(str(text))}</span>'


def legend_html(diagrams, m):
    """Self-teaching legend: the ABCD method + what each diagram type / badge means."""
    types_here = {d.get("type") for d in diagrams if d.get("type")}
    order = [
        "business-usecase", "business-sequence", "usecase", "activity",
        "domain-model", "class", "data-model", "state", "system-sequence", "design-sequence", "contract",
    ]
    present = [t for t in order if t in types_here]
    present += [t for t in sorted(types_here) if t not in present and t in TYPE_GLOSS]

    abcd = "".join(
        f"<li><b>{html.escape(WF.get(k, k))}</b> — {WF_GLOSS[k]}</li>" for k in ["A", "B", "C", "D"]
    )
    types = "".join(
        f"<li><code>{html.escape(t)}</code> — {TYPE_GLOSS[t]}</li>" for t in present if t in TYPE_GLOSS
    )
    core = (
        "<li><b>Profit = Requirements − Design.</b> AI makes design/coding cheap, so value moves "
        "upstream to business modeling (A).</li>"
        "<li><b>You cannot reverse-engineer requirements from code.</b> Reverse recovers the design-level "
        "as-is only; business &amp; requirements are modeled forward, with you in the loop.</li>"
        "<li><b>OO is an analysis lens, not a code-syntax property.</b> Even functional code has a latent "
        "object model worth drawing.</li>"
    )
    badges = (
        '<span class="badge prov-forward">forward</span> modeled with you (top-down) &middot; '
        '<span class="badge prov-reverse">reverse</span> recovered from code (the as-is) &middot; '
        '<span class="badge prov-hybrid">hybrid</span> recovered skeleton + modeling judgment'
    )
    uf = m.get("uncovered_flows") or []
    uf_html = ""
    if uf:
        items = "".join(
            "<li>" + html.escape(u.get("node", ""))
            + (f' — <span class="muted">{html.escape(u.get("reason", ""))}</span>' if u.get("reason") else "")
            + (f' <code>{html.escape(u.get("code_hint", ""))}</code>' if u.get("code_hint") else "")
            + "</li>"
            for u in uf
        )
        uf_html = (
            '<div class="uncovered"><b>Not covered yet</b> — reverse only maps the flows it traced; '
            f"these exist in the code but were not recovered:<ul>{items}</ul></div>"
        )
    return (
        '<details class="legend" open><summary>What am I looking at? · 软件方法 (ABCD)</summary>'
        '<p class="muted">A standardized <b>diagram-as-code</b> design package. A manifest keeps every diagram '
        "in one navigable model (business ↔ code), so humans read the pictures and AI reads the source.</p>"
        f'<div class="lg"><b>The four workflows</b><ul>{abcd}</ul></div>'
        f'<div class="lg"><b>Core method</b><ul>{core}</ul></div>'
        f'<div class="lg"><b>Diagram types in this package</b><ul>{types}</ul></div>'
        f'<div class="lg"><b>Provenance</b> <span class="muted">{badges}</span></div>'
        f"{uf_html}</details>"
    )


def render_card(d, design: pathlib.Path):
    title = html.escape(d.get("title", d.get("id", "")))
    prov = d.get("provenance", "")
    badges = (
        badge(prov, "prov-" + prov)
        + badge(d.get("level", ""), "lvl")
        + badge(d.get("phase", ""), "phase")
        + badge(d.get("type", ""), "type")
        + badge(d.get("tool", ""), "tool")
    )
    gaps = d.get("gaps") or []
    gaps_html = ""
    if gaps:
        items = "".join(f"<li>{html.escape(g)}</li>" for g in gaps)
        gaps_html = f'<div class="gaps"><b>gaps</b><ul>{items}</ul></div>'
    refs = d.get("code_refs") or []
    refs_html = ""
    if refs:
        chips = " · ".join(
            f'<code>{html.escape(r.get("path", ""))}:{html.escape(str(r.get("lines", "")))}</code>'
            for r in refs
        )
        refs_html = f'<div class="refs">{chips}</div>'

    src = read(design / d.get("file", ""))
    if src is None:
        view = f'<div class="missing">missing file: {html.escape(d.get("file", ""))}</div>'
    elif d.get("tool") == "mermaid":
        view = f'<pre class="mermaid">{html.escape(src)}</pre>'
    elif d.get("tool") == "markdown":
        view = f'<details open><summary>contract (markdown source)</summary><pre class="src">{html.escape(src)}</pre></details>'
    else:  # plantuml (or anything non-mermaid)
        svgp = design / "rendered" / (str(d.get("id", "")) + ".svg")
        if svgp.exists():
            svg = read(svgp) or ""
            svg = re.sub(r"^\s*<\?xml[^>]*\?>\s*", "", svg)
            svg = re.sub(r"<!DOCTYPE[^>]*>\s*", "", svg, flags=re.I)
            view = f'<div class="svgwrap">{svg}</div>'
        else:
            view = (
                "<details><summary>PlantUML source (install plantuml so the render step "
                f'pre-renders it to SVG)</summary><pre class="src">{html.escape(src)}</pre></details>'
            )
    return (
        f'<article class="card"><div class="chead"><h3>{title}</h3>'
        f'<div class="badges">{badges}</div></div>{refs_html}{gaps_html}'
        f'<div class="view">{view}</div></article>'
    )


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    if arg:
        design = pathlib.Path(arg)
    elif pathlib.Path("design/manifest.json").exists():
        design = pathlib.Path("design")
    else:
        design = pathlib.Path(".")

    mpath = design / "manifest.json"
    if not mpath.exists():
        print(f"ERROR: {mpath} not found", file=sys.stderr)
        sys.exit(1)
    m = json.loads(mpath.read_text(encoding="utf-8"))
    diagrams = m.get("diagrams", [])

    groups = {}
    for d in diagrams:
        groups.setdefault(d.get("workflow", "?"), []).append(d)

    parts = []
    sysname = html.escape(m.get("system", "(unnamed system)"))
    parts.append(f"<header><h1>{sysname}</h1>")
    if m.get("purpose"):
        parts.append(f'<p class="purpose">{html.escape(m["purpose"])}</p>')
    v = m.get("vision") or {}
    if v:
        goals = "".join(
            f'<li>{html.escape(g.get("metric", ""))} '
            f'<span class="muted">{html.escape(str(g.get("baseline", "")))} → '
            f'{html.escape(str(g.get("target", "")))}</span></li>'
            for g in v.get("goals", [])
        )
        parts.append(
            '<div class="vision"><b>Vision</b> · boss: '
            f'{html.escape(str(v.get("boss", "")))} · org: '
            f'{html.escape(str(v.get("organization", "")))}<ul>{goals}</ul></div>'
        )
    parts.append(
        f'<p class="muted">generated {html.escape(str(m.get("generated", "")))} · '
        f"{len(diagrams)} diagrams · source is the single source of truth; "
        "Mermaid renders locally in the browser</p></header>"
    )

    parts.append(legend_html(diagrams, m))

    for wf in ["A", "B", "C", "D"]:
        ds = groups.get(wf)
        if not ds:
            continue
        cards = "".join(render_card(d, design) for d in ds)
        parts.append(f"<section><h2>{html.escape(WF.get(wf, wf))}</h2>{cards}</section>")

    tr = m.get("traceability") or []
    if tr:
        rows = "".join(
            f'<tr><td>{html.escape(t.get("use_case", ""))}</td>'
            f'<td>{html.escape(", ".join(t.get("analysis_classes", [])))}</td>'
            f'<td>{html.escape(", ".join(t.get("code", [])))}</td></tr>'
            for t in tr
        )
        parts.append(
            '<section><h2>Traceability</h2><table><thead><tr><th>Use case</th>'
            f"<th>Analysis classes</th><th>Code</th></tr></thead><tbody>{rows}</tbody></table></section>"
        )

    out = TEMPLATE.replace("{{TITLE}}", sysname).replace("{{BODY}}", "\n".join(parts))
    (design / "index.html").write_text(out, encoding="utf-8")
    print(f'wrote {design / "index.html"} ({len(diagrams)} diagrams)')


TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{{TITLE}} · abcd design</title>
<style>
  :root{
    --bg:#fbfbfa; --fg:#1f1f1d; --fg2:#6b6b66; --card:#fff; --bd:#e6e4df;
    --accent:#7F77DD; --blue:#3b6fd4; --coral:#d4663b; --teal:#2f9a8f; --amber:#b5862a;
  }
  @media (prefers-color-scheme: dark){
    :root{ --bg:#1a1a18; --fg:#ececea; --fg2:#9a9a95; --card:#232320; --bd:#36352f;
      --blue:#7aa2f0; --coral:#e89a78; --teal:#5fc7bb; --amber:#d9b65f; }
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--fg);
    font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;
    line-height:1.6;padding:32px 20px}
  .wrap{max-width:1000px;margin:0 auto}
  header{border-bottom:1px solid var(--bd);padding-bottom:16px;margin-bottom:8px}
  h1{font-size:24px;font-weight:600;margin:0 0 4px}
  h2{font-size:18px;font-weight:600;margin:32px 0 12px;color:var(--fg)}
  h3{font-size:15px;font-weight:600;margin:0}
  .purpose{color:var(--fg2);margin:4px 0}
  .muted{color:var(--fg2);font-size:13px}
  .vision{background:var(--card);border:1px solid var(--bd);border-radius:10px;padding:10px 14px;margin:10px 0;font-size:14px}
  .vision ul{margin:6px 0 0;padding-left:18px}
  .legend{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px 16px;margin:14px 0}
  .legend>summary{cursor:pointer;font-weight:600;font-size:15px}
  .legend .lg{margin:12px 0 0}
  .legend ul{margin:4px 0 0;padding-left:18px;font-size:13.5px}
  .legend li{margin:3px 0}
  .legend code{background:var(--bg);padding:1px 5px;border-radius:4px;
    font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
  .uncovered{margin:12px 0 0;font-size:13.5px;color:var(--coral)}
  .uncovered ul{margin:4px 0 0;padding-left:18px}
  .uncovered code{color:var(--fg2)}
  .card{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:16px;margin:14px 0}
  .chead{display:flex;justify-content:space-between;align-items:flex-start;gap:12px;flex-wrap:wrap}
  .badges{display:flex;gap:6px;flex-wrap:wrap}
  .badge{font-size:11px;padding:2px 8px;border-radius:20px;border:1px solid var(--bd);color:var(--fg2);white-space:nowrap}
  .prov-forward{color:var(--blue);border-color:var(--blue)}
  .prov-reverse{color:var(--coral);border-color:var(--coral)}
  .prov-hybrid{color:var(--teal);border-color:var(--teal)}
  .refs{margin:8px 0 0;font-size:12px;color:var(--fg2)}
  .refs code,.src{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
  .refs code{background:var(--bg);padding:1px 5px;border-radius:4px}
  .gaps{margin:8px 0 0;font-size:13px;color:var(--amber)}
  .gaps ul{margin:4px 0 0;padding-left:18px}
  .view{margin-top:12px;overflow-x:auto}
  .mermaid{background:transparent;border:0;text-align:center}
  .svgwrap svg{max-width:100%;height:auto}
  details{margin-top:8px}
  summary{cursor:pointer;color:var(--fg2);font-size:13px}
  pre.src{background:var(--bg);border:1px solid var(--bd);border-radius:8px;padding:12px;
    font-size:12px;overflow-x:auto;white-space:pre}
  .missing{color:var(--coral);font-size:13px}
  table{border-collapse:collapse;width:100%;font-size:13px}
  th,td{border:1px solid var(--bd);padding:6px 10px;text-align:left;vertical-align:top}
  th{color:var(--fg2);font-weight:600}
</style>
</head>
<body>
<div class="wrap">
{{BODY}}
</div>
<script type="module">
  import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
  const dark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
  mermaid.initialize({ startOnLoad: true, theme: dark ? 'dark' : 'default',
    securityLevel: 'loose', sequence: { useMaxWidth: true } });
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
