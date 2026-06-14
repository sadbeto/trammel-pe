"""
Trammel PE MCP Server — Model Context Protocol integration via FastMCP.

Allows any MCP-compatible agent (OpenClaw, Claude Desktop, Cursor, etc.)
to generate structured prompts via Trammel PE without knowing the SDK.

Transport: stdio only (local access, no network exposure)
Methodology: Supports Karpathy 4 Principles as built-in option
"""

import json
import dataclasses
from pathlib import Path
from typing import Optional

from mcp.server.fastmcp import FastMCP

# Add parent to path so we can import trammel_pe
import sys
sys.path.insert(0, str(Path(__file__).parent))

from trammel_pe.core import TrammelPE, PromptData, PromptChain, TEMPLATES


# ── FastMCP Server ──────────────────────────────────────────────────────────

mcp = FastMCP(
    "trammel-pe",
    instructions="Trammel PE — Trace the arc from idea to execution. Generate structured, tool-aware prompts for any LLM agent.",
)


# ── Tool 1: generate_prompt ─────────────────────────────────────────────────

@mcp.tool()
def generate_prompt(
    objective: str,
    domain: Optional[str] = None,
    success_criteria: Optional[str] = None,
    in_scope: Optional[str] = None,
    out_scope: Optional[str] = None,
    depth: Optional[str] = None,
    role: Optional[str] = None,
    tone: Optional[str] = None,
    tools: Optional[list] = None,
    subtasks: Optional[list] = None,
    format_type: Optional[str] = None,
    length_target: Optional[str] = None,
    background: Optional[str] = None,
    audience: Optional[str] = None,
    must_do: Optional[str] = None,
    constraints: Optional[str] = None,
    edge_cases: Optional[str] = None,
    self_learn: Optional[bool] = None,
    methodology: Optional[str] = None,
    lang: Optional[str] = None,
) -> str:
    """Generate a structured, tool-aware prompt for any LLM agent using the Trammel PE framework.
    Returns a complete prompt with 9 sections: Objective, Role & Tone, Success Criteria, Scope,
    Tools, Task Decomposition, Context & Data, Output Format, Constraints, and optional Self-Learning Loop.

    Args:
        objective: What you want the agent to do (verb-first, specific). REQUIRED.
        domain: Domain of expertise (e.g., 'Construction', 'Software Engineering', 'Cybersecurity').
        success_criteria: How you know the task is done. Be measurable.
        in_scope: What the agent SHOULD handle.
        out_scope: What the agent should NOT touch.
        depth: Analysis depth: quick, standard, expert.
        role: Who the agent should be (e.g., 'Senior Dev Agent Principal').
        tone: Communication style: technical, casual, academic, formal.
        tools: Comma-separated list of tools the agent can use.
        subtasks: JS-composable task decomposition (JSON list of dicts with objective, data_focus).
        format_type: Output format: markdown, json, table, bulletlist, narrative, code, mixed.
        length_target: Target length: brief, moderate, comprehensive, unlimited.
        background: Background context or reference material.
        audience: Target audience for the output.
        must_do: MUST DO rules — non-negotiable requirements.
        constraints: MUST NOT rules — hard boundaries.
        edge_cases: Edge cases the agent should anticipate.
        self_learn: Enable self-learning loop (reflect, validate, improve).
        methodology: Methodology preset: 'karpathy' for 4 Principles.
        lang: Output language: en, es, pt.
    """
    trammel = TrammelPE(lang=lang or "en")

    allowed = {f.name for f in dataclasses.fields(PromptData)}
    params = {k: v for k, v in {
        "objective": objective,
        "domain": domain,
        "success_criteria": success_criteria,
        "in_scope": in_scope,
        "out_scope": out_scope,
        "depth": depth,
        "role": role,
        "tone": tone,
        "tools": tools,
        "subtasks": subtasks,
        "format_type": format_type,
        "length_target": length_target,
        "background": background,
        "audience": audience,
        "must_do": must_do,
        "constraints": constraints,
        "edge_cases": edge_cases,
        "self_learn": self_learn,
        "methodology": methodology,
        "lang": lang,
    }.items() if v is not None and k in allowed}

    data = PromptData(**params)
    return trammel.generate_markdown(data)


# ── Tool 2: generate_from_template ───────────────────────────────────────────

@mcp.tool()
def generate_from_template(
    template_id: str,
    objective: Optional[str] = None,
    domain: Optional[str] = None,
    lang: Optional[str] = None,
    methodology: Optional[str] = None,
) -> str:
    """Generate a prompt using a built-in Trammel PE template.

    Available templates: competitive, data-analysis, content-writing, api-design, code-review, security-audit

    Args:
        template_id: Template to use (competitive, data-analysis, content-writing, api-design, code-review, security-audit).
        objective: What you want the agent to do. REQUIRED.
        domain: Domain of expertise (e.g., 'Construction', 'Software Engineering', 'Cybersecurity').
        lang: Output language: en, es, pt.
        methodology: Methodology preset: 'karpathy' for 4 Principles.
    """
    if template_id not in TEMPLATES:
        available = ", ".join(TEMPLATES.keys())
        return f"Error: Unknown template '{template_id}'. Available: {available}"

    trammel = TrammelPE(lang=lang or "en")
    overrides = {}
    if objective:
        overrides["objective"] = objective
    if domain:
        overrides["domain"] = domain
    if methodology:
        overrides["methodology"] = methodology

    data = trammel.from_template(template_id, overrides=overrides or None)
    return trammel.generate_markdown(data)


# ── Tool 3: list_templates ───────────────────────────────────────────────────

@mcp.tool()
def list_templates(lang: Optional[str] = None) -> str:
    """List all available Trammel PE templates with descriptions.

    Args:
        lang: Language for descriptions (default: en).
    """
    lang = lang or "en"
    lines = ["Available Trammel PE Templates:\n"]
    for tid, tpl in TEMPLATES.items():
        obj = tpl.get("objective", "")
        if isinstance(obj, dict):
            obj = obj.get(lang, obj.get("en", ""))
        lines.append(f"• {tid}: {obj}")
    return "\n".join(lines)


# ── Tool 4: generate_chain ───────────────────────────────────────────────────

@mcp.tool()
def generate_chain(
    name: str,
    steps: list,
    lang: Optional[str] = None,
    output_format: Optional[str] = None,
) -> str:
    """Generate a sequential prompt chain from a list of prompt configs.
    Each step's output feeds the next step via the {{prev_output}} placeholder.
    Returns a Markdown mega-prompt with stage gates, or a JSON chain spec.
    Trammel generates the artifact; the consuming agent executes the chain.

    Args:
        name: Chain name.
        steps: Ordered list of prompt configs (same fields as generate_prompt: objective, role, success_criteria, etc.). Use {{prev_output}} in any field of steps 2+ to reference the previous step's output.
        lang: Output language (default: en).
        output_format: Return format: markdown or json (default: markdown).
    """
    if not name:
        return "Error: 'name' is required"
    if not isinstance(steps, list) or len(steps) < 2:
        return "Error: 'steps' must be a list with at least 2 prompt configs"

    lang = lang or "en"
    trammel = TrammelPE(lang=lang)
    allowed = {f.name for f in dataclasses.fields(PromptData)}
    step_data = []

    for i, cfg in enumerate(steps):
        if not isinstance(cfg, dict) or not cfg.get("objective"):
            return f"Error: steps[{i}] must be an object with at least an 'objective'"
        cfg = dict(cfg)
        cfg.setdefault("lang", lang)
        step_data.append(PromptData(**{k: v for k, v in cfg.items() if k in allowed}))

    chain = PromptChain(name, step_data, lang=lang)

    if output_format == "json":
        return json.dumps(chain.to_json(), indent=2, ensure_ascii=False)
    else:
        return chain.to_markdown()


# ── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    mcp.run(transport="stdio")