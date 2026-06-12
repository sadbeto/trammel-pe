#!/usr/bin/env python3
"""Parity check: chain artifact structure must match between index.html (JS)
and trammel-py (Python). Runs both with identical inputs and diffs the
structural lines (headers, gates, piping contract)."""
import json, re, subprocess, sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
HTML = (REPO / "index.html").read_text()

# Extract the two JS chain builders + escapeHtml helper
def extract(fn_name):
    m = re.search(rf"function {fn_name}\(.*?\n\}}", HTML, re.S)
    if not m:
        print(f"FAIL: could not extract {fn_name} from index.html"); sys.exit(1)
    return m.group(0)

js = "\n".join([extract("buildChainMarkdown"), extract("buildChainJSON")])
js += """
const steps = [
  {name: 'Research competitors', data: {objective: 'Research top 5 competitors'}, prompt: 'PROMPT_ONE'},
  {name: 'Exec summary', data: {objective: 'Summarize {{prev_output}}'}, prompt: 'PROMPT_TWO'},
];
const md = buildChainMarkdown('Parity Chain', steps);
const j = buildChainJSON('Parity Chain', steps);
console.log(JSON.stringify({md, json: j}));
"""
node = subprocess.run(["node", "-e", js], capture_output=True, text=True)
if node.returncode != 0:
    print("FAIL: node error:", node.stderr); sys.exit(1)
js_out = json.loads(node.stdout)

# Python side: same step names/prompts via a stub that bypasses generation
sys.path.insert(0, str(REPO / "trammel-py"))
from trammel_pe.core import PromptChain, PromptData

chain = PromptChain("Parity Chain", [
    PromptData(objective="Research top 5 competitors"),
    PromptData(objective="Summarize {{prev_output}}"),
])
# Force identical step names and prompt bodies so we diff STRUCTURE only
chain._step_name = lambda d, i: ["Research competitors", "Exec summary"][i]
chain._engine.generate_markdown = lambda d: ["PROMPT_ONE", "PROMPT_TWO"][
    0 if d.objective.startswith("Research") else 1]
py_md = chain.to_markdown()
py_json = chain.to_json()

fail = 0
if js_out["md"] != py_md:
    fail = 1
    print("FAIL: markdown drift JS vs Python")
    import difflib
    for line in difflib.unified_diff(js_out["md"].splitlines(), py_md.splitlines(),
                                     "js", "py", lineterm=""):
        print(" ", line)
else:
    print("OK: chain markdown identical JS == Python (%d chars)" % len(py_md))

# JSON: compare structural keys (data payloads legitimately differ:
# JS stores raw form data, Python stores generated JSON spec)
def shape(o):
    return {
        "version": o.get("trammel_pe_chain"),
        "execution": o.get("execution"),
        "piping": o.get("piping"),
        "steps": [{"step": s["step"], "name": s["name"],
                   "receives_prev_output": s["receives_prev_output"],
                   "prompt": s["prompt"]} for s in o.get("steps", [])],
    }

if shape(js_out["json"]) != shape(py_json):
    fail = 1
    print("FAIL: JSON chain spec structural drift")
    print(" js:", json.dumps(shape(js_out["json"]), indent=1)[:500])
    print(" py:", json.dumps(shape(py_json), indent=1)[:500])
else:
    print("OK: chain JSON spec structure identical JS == Python")

print("RESULT:", "PARITY FAIL" if fail else "PARITY OK")
sys.exit(fail)
