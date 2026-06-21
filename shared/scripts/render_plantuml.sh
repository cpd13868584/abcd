#!/usr/bin/env bash
# abcd: pre-render PlantUML diagrams in a design package to rendered/<id>.svg.
# Fully offline (plantuml + graphviz) — no diagram data leaves the machine.
# build_index_html.py then inlines rendered/<id>.svg instead of folding the source.
#
# Usage: render_plantuml.sh [design_dir]   # default ./design, else .
set -uo pipefail

DESIGN="${1:-design}"
[ -f "$DESIGN/manifest.json" ] || DESIGN="."
MANIFEST="$DESIGN/manifest.json"
[ -f "$MANIFEST" ] || { echo "ERROR: manifest.json not found (pass the design dir)" >&2; exit 1; }
ABS="$(cd "$DESIGN" && pwd)"

# Resolve a PlantUML runner: prefer `plantuml`, else `java -jar $PLANTUML_JAR`.
PUML=""
if command -v plantuml >/dev/null 2>&1; then
  PUML="plantuml"
elif [ -n "${PLANTUML_JAR:-}" ] && command -v java >/dev/null 2>&1; then
  PUML="java -jar ${PLANTUML_JAR}"
fi

if [ -z "$PUML" ]; then
  echo "plantuml not found — skipping PlantUML pre-render (HTML viewer will fold source)."
  echo "  install for offline rendering:"
  echo "    macOS : brew install plantuml"
  echo "    Debian: sudo apt-get install -y plantuml"
  echo "    or    : set PLANTUML_JAR=/path/to/plantuml.jar (needs java) + graphviz for usecase"
  exit 0   # non-fatal
fi

if ! command -v dot >/dev/null 2>&1; then
  echo "note: graphviz (dot) not found — usecase diagrams may not lay out. install: brew install graphviz" >&2
fi

mkdir -p "$ABS/rendered"
n=0
# manifest → "<id>\t<file>" for every tool=plantuml diagram
python3 - "$MANIFEST" <<'PY' | while IFS=$'\t' read -r id file; do
import json, sys
m = json.load(open(sys.argv[1]))
for d in m.get("diagrams", []):
    if d.get("tool") == "plantuml" and d.get("file"):
        print(f"{d['id']}\t{d['file']}")
PY
  src="$ABS/$file"
  [ -f "$src" ] || { echo "skip (missing): $file"; continue; }
  base="$(basename "${file%.*}")"
  if $PUML -tsvg -o "$ABS/rendered" "$src" >/dev/null 2>&1; then
    [ "$base.svg" != "$id.svg" ] && mv -f "$ABS/rendered/$base.svg" "$ABS/rendered/$id.svg"
    echo "rendered: rendered/$id.svg"
    n=$((n + 1))
  else
    echo "render failed: $file"
  fi
done
echo "done."
