#!/usr/bin/env python3
"""Parity test: quality() in SDK must match computeQuality() in index.html."""
import json
import re
import subprocess
import sys
import os

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "trammel-py"))
from trammel_pe import PromptData  # noqa: E402

CASES = [
    # (name, fields)
    ("vague", {
        "objective": "do some stuff with my data please and things",
        "success_criteria": "it works good",
    }),
    ("strong", {
        "objective": "Analyze the competitive landscape for a SaaS startup",
        "success_criteria": "A prioritized list of 5-7 competitors with revenue estimates",
        "in_scope": "LATAM market, companies with >$1M ARR",
        "out_scope": "Companies with no AI component, markets outside LATAM",
        "constraints": "No speculation without sourcing. Every point actionable.",
        "must_do": "Must include revenue estimates with confidence levels and citations.",
        "subtasks": [{"name": "Research", "desc": "Find competitors", "data": "G2, pricing pages"}],
    }),
    ("empty", {}),
    ("spanish", {
        "objective": "Construye un dashboard de ventas con filtros por region",
        "success_criteria": "Dashboard con 5 KPIs y carga en menos de 2 segundos",
        "in_scope": "Ventas de Puerto Rico y LATAM",
    }),
]

# --- JS side: extract script, run computeQuality via node ---
html = open(os.path.join(REPO, "index.html")).read()
script = re.findall(r"<script[^>]*>(.*?)</script>", html, re.S)[0]

# Extract only what we need: the QS_ constants and computeQuality (buildPrompt
# is DOM-heavy, so stub it — tokens aren't part of this parity check)
harness = """
const QS_ACTION_VERBS = %s;
const QS_VAGUE_WORDS = %s;
const QS_MEASURABLE = %s;
function buildPrompt() { return ''; }
%s
const cases = %s;
const out = {};
for (const [name, d] of Object.entries(cases)) {
  const full = Object.assign({objective:'',successCriteria:'',inScope:'',outScope:'',role:'',
    background:'',constraints:'',mustDo:'',edgeCases:'',subtasks:[]}, d);
  const q = computeQuality(full);
  out[name] = {completeness: q.completeness, specificity: q.specificity, tips: q.tips};
}
console.log(JSON.stringify(out));
"""

def grab(name):
    m = re.search(rf"const {name} = (/.+?/i);", script)
    if not m:
        print(f"FAIL: could not extract {name} from index.html")
        sys.exit(1)
    return m.group(1)

m = re.search(r"(function computeQuality\(d\) \{.*?\n\})", script, re.S)
if not m:
    print("FAIL: could not extract computeQuality from index.html")
    sys.exit(1)

js_cases = {name: {
    "objective": c.get("objective", ""),
    "successCriteria": c.get("success_criteria", ""),
    "inScope": c.get("in_scope", ""),
    "outScope": c.get("out_scope", ""),
    "constraints": c.get("constraints", ""),
    "mustDo": c.get("must_do", ""),
    "subtasks": c.get("subtasks", []),
} for name, c in CASES}

code = harness % (grab("QS_ACTION_VERBS"), grab("QS_VAGUE_WORDS"),
                  grab("QS_MEASURABLE"), m.group(1), json.dumps(js_cases))
js_out = json.loads(subprocess.run(["node", "-e", code], capture_output=True,
                                   text=True, check=True).stdout)

# --- Python side ---
fails = 0
for name, c in CASES:
    py = PromptData(**c).quality()
    js = js_out[name]
    match = (py["completeness"] == js["completeness"]
             and py["specificity"] == js["specificity"]
             and py["tips"] == js["tips"])
    status = "OK " if match else "FAIL"
    if not match:
        fails += 1
    print(f"  {status} {name}: py={py} js={js}")

if fails:
    print(f"PARITY: {fails} case(s) diverged")
    sys.exit(1)
print("PARITY: SDK and HTML quality scoring match")
