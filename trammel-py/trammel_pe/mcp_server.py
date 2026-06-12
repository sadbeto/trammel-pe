"""
Trammel PE MCP Server — Model Context Protocol integration.

Allows any MCP-compatible agent (OpenClaw, Claude Desktop, Cursor, etc.)
to generate structured prompts via Trammel PE without knowing the SDK.

Transport: stdio (for local agent integration)
"""

import json
import sys
import argparse
import dataclasses
from pathlib import Path

# Add parent to path so we can import trammel_pe
sys.path.insert(0, str(Path(__file__).parent))

from trammel_pe.core import TrammelPE, PromptData, PromptChain, TEMPLATES


# ── MCP Protocol Implementation ────────────────────────────────────────────

def handle_initialize(params: dict) -> dict:
    return {
        "capabilities": {
            "tools": {"listChanged": False},
        },
        "serverInfo": {
            "name": "trammel-pe",
            "version": "0.1.0",
        },
    }


def handle_tools_list() -> list:
    return [
        {
            "name": "generate_prompt",
            "description": "Generate a structured, tool-aware prompt for any LLM agent using the Trammel PE framework. Returns a complete prompt with 9 sections: Objective, Role & Tone, Success Criteria, Scope, Tools, Task Decomposition, Context & Data, Output Format, Constraints, and optional Self-Learning Loop.",
            "inputSchema": {
                "type": "object",
                "required": ["objective"],
                "properties": {
                    "objective": {
                        "type": "string",
                        "description": "What you want the agent to do (verb-first, specific)",
                    },
                    "domain": {
                        "type": "string",
                        "description": "Domain of expertise (e.g., 'Construction', 'Software Engineering', 'Cybersecurity')",
                    },
                    "success_criteria": {
                        "type": "string",
                        "description": "What 'done' looks like — measurable success criteria",
                    },
                    "in_scope": {
                        "type": "string",
                        "description": "What's included in the task scope",
                    },
                    "out_scope": {
                        "type": "string",
                        "description": "What's excluded from the task scope",
                    },
                    "depth": {
                        "type": "string",
                        "enum": ["quick", "standard", "deep", "expert"],
                        "description": "Analysis depth level",
                    },
                    "role": {
                        "type": "string",
                        "description": "Who the AI should be (persona/expertise)",
                    },
                    "tone": {
                        "type": "string",
                        "enum": ["professional", "concise", "academic", "creative", "conversational", "technical", "executive"],
                        "description": "Output tone",
                    },
                    "tools": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "enum": ["web_search", "code_execution", "file_read_write", "api_calls", "data_analysis", "browser_automation", "database", "shell_terminal", "image_generation", "document_processing", "scheduling_cron", "memory_vector_db"],
                        },
                        "description": "Tools the agent should use",
                    },
                    "subtasks": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "name": {"type": "string", "description": "Sub-task name"},
                                "desc": {"type": "string", "description": "Sub-task description"},
                                "data": {"type": "string", "description": "Data focus for this sub-task"},
                            },
                        },
                        "description": "Task decomposition — break the objective into focused sub-tasks",
                    },
                    "format_type": {
                        "type": "string",
                        "enum": ["markdown", "json", "table", "bulletlist", "narrative", "code", "mixed"],
                        "description": "Output format",
                    },
                    "length_target": {
                        "type": "string",
                        "enum": ["brief", "moderate", "comprehensive", "unlimited"],
                        "description": "Target output length",
                    },
                    "background": {
                        "type": "string",
                        "description": "Background context for the agent",
                    },
                    "input_data": {
                        "type": "string",
                        "description": "Input data the agent should work with",
                    },
                    "audience": {
                        "type": "string",
                        "description": "Target audience for the output",
                    },
                    "must_do": {
                        "type": "string",
                        "description": "MUST DO rules — things the agent must include or do",
                    },
                    "constraints": {
                        "type": "string",
                        "description": "MUST NOT rules — things the agent must avoid",
                    },
                    "edge_cases": {
                        "type": "string",
                        "description": "Edge cases the agent should handle",
                    },
                    "self_learn": {
                        "type": "boolean",
                        "description": "Enable self-learning loop (agent iterates on its own output)",
                    },
                    "iteration_strategy": {
                        "type": "string",
                        "enum": ["reflect", "validate", "research_more", "all"],
                        "description": "Self-learning strategy",
                    },
                    "max_iterations": {
                        "type": "integer",
                        "description": "Max self-learning iterations (default: 3)",
                    },
                    "improvement_focus": {
                        "type": "string",
                        "description": "What the agent should improve each iteration",
                    },
                    "lang": {
                        "type": "string",
                        "enum": ["en", "es", "pt"],
                        "description": "Output language (default: en)",
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["markdown", "json"],
                        "description": "Return format: 'markdown' for .md content, 'json' for structured JSON (default: markdown)",
                    },
                },
            },
        },
        {
            "name": "generate_from_template",
            "description": "Generate a prompt from a built-in Trammel PE template. Templates: competitive, data-analysis, content-writing, api-design, code-review, security-audit. Optionally override objective and domain.",
            "inputSchema": {
                "type": "object",
                "required": ["template_id"],
                "properties": {
                    "template_id": {
                        "type": "string",
                        "enum": list(TEMPLATES.keys()),
                        "description": "Template to use",
                    },
                    "objective": {
                        "type": "string",
                        "description": "Override template objective",
                    },
                    "domain": {
                        "type": "string",
                        "description": "Override template domain",
                    },
                    "lang": {
                        "type": "string",
                        "enum": ["en", "es", "pt"],
                        "description": "Output language (default: en)",
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["markdown", "json"],
                        "description": "Return format (default: markdown)",
                    },
                },
            },
        },
        {
            "name": "list_templates",
            "description": "List available Trammel PE prompt templates with descriptions.",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "lang": {
                        "type": "string",
                        "enum": ["en", "es", "pt"],
                        "description": "Language for descriptions (default: en)",
                    },
                },
            },
        },
        {
            "name": "generate_chain",
            "description": "Generate a sequential prompt chain from a list of prompt configs. Each step's output feeds the next step via the {{prev_output}} placeholder. Returns a Markdown mega-prompt with stage gates, or a JSON chain spec. Trammel generates the artifact; the consuming agent executes the chain.",
            "inputSchema": {
                "type": "object",
                "required": ["name", "steps"],
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "Chain name",
                    },
                    "steps": {
                        "type": "array",
                        "minItems": 2,
                        "description": "Ordered list of prompt configs (same fields as generate_prompt: objective, role, success_criteria, in_scope, out_scope, etc.). Use {{prev_output}} in any field of steps 2+ to reference the previous step's output.",
                        "items": {"type": "object"},
                    },
                    "lang": {
                        "type": "string",
                        "enum": ["en", "es", "pt"],
                        "description": "Output language (default: en)",
                    },
                    "output_format": {
                        "type": "string",
                        "enum": ["markdown", "json"],
                        "description": "Return format (default: markdown)",
                    },
                },
            },
        },
    ]


def handle_tool_call(name: str, arguments: dict) -> list:
    """Execute a tool call and return MCP content items."""
    try:
        if name == "generate_prompt":
            # Build PromptData from arguments
            data = PromptData(
                objective=arguments.get("objective", ""),
                domain=arguments.get("domain", ""),
                success_criteria=arguments.get("success_criteria", ""),
                in_scope=arguments.get("in_scope", ""),
                out_scope=arguments.get("out_scope", ""),
                depth=arguments.get("depth", "standard"),
                role=arguments.get("role", ""),
                tone=arguments.get("tone", "professional"),
                tools=arguments.get("tools", []),
                subtasks=arguments.get("subtasks", []),
                format_type=arguments.get("format_type", "markdown"),
                length_target=arguments.get("length_target", "moderate"),
                background=arguments.get("background", ""),
                input_data=arguments.get("input_data", ""),
                audience=arguments.get("audience", ""),
                must_do=arguments.get("must_do", ""),
                constraints=arguments.get("constraints", ""),
                edge_cases=arguments.get("edge_cases", ""),
                self_learn=arguments.get("self_learn", False),
                iteration_strategy=arguments.get("iteration_strategy", "reflect"),
                max_iterations=arguments.get("max_iterations", 3),
                improvement_focus=arguments.get("improvement_focus", ""),
                lang=arguments.get("lang", "en"),
            )
            trammel = TrammelPE(lang=data.lang)
            output_fmt = arguments.get("output_format", "markdown")
            if output_fmt == "json":
                result = json.dumps(trammel.generate_json(data), indent=2, ensure_ascii=False)
            else:
                result = trammel.generate_markdown(data)
            return [{"type": "text", "text": result}]

        elif name == "generate_from_template":
            template_id = arguments.get("template_id", "")
            if template_id not in TEMPLATES:
                return [{"type": "text", "text": f"Error: Unknown template '{template_id}'. Available: {', '.join(TEMPLATES.keys())}"}]
            trammel = TrammelPE(lang=arguments.get("lang", "en"))
            overrides = {}
            if arguments.get("objective"):
                overrides["objective"] = arguments["objective"]
            if arguments.get("domain"):
                overrides["domain"] = arguments["domain"]
            data = trammel.from_template(template_id, overrides=overrides or None)
            output_fmt = arguments.get("output_format", "markdown")
            if output_fmt == "json":
                result = json.dumps(trammel.generate_json(data), indent=2, ensure_ascii=False)
            else:
                result = trammel.generate_markdown(data)
            return [{"type": "text", "text": result}]

        elif name == "list_templates":
            lang = arguments.get("lang", "en")
            lines = ["Available Trammel PE Templates:\n"]
            for tid, tpl in TEMPLATES.items():
                obj = tpl.get("objective", "")
                if isinstance(obj, dict):
                    obj = obj.get(lang, obj.get("en", ""))
                lines.append(f"• {tid}: {obj}")
            return [{"type": "text", "text": "\n".join(lines)}]

        elif name == "generate_chain":
            chain_name = arguments.get("name", "")
            raw_steps = arguments.get("steps", [])
            lang = arguments.get("lang", "en")
            if not chain_name:
                return [{"type": "text", "text": "Error: 'name' is required"}]
            if not isinstance(raw_steps, list) or len(raw_steps) < 2:
                return [{"type": "text", "text": "Error: 'steps' must be a list with at least 2 prompt configs"}]
            step_data = []
            allowed = {f.name for f in dataclasses.fields(PromptData)}
            for i, cfg in enumerate(raw_steps):
                if not isinstance(cfg, dict) or not cfg.get("objective"):
                    return [{"type": "text", "text": f"Error: steps[{i}] must be an object with at least an 'objective'"}]
                cfg = dict(cfg)
                cfg.setdefault("lang", lang)
                step_data.append(PromptData(**{k: v for k, v in cfg.items() if k in allowed}))
            chain = PromptChain(chain_name, step_data, lang=lang)
            output_fmt = arguments.get("output_format", "markdown")
            if output_fmt == "json":
                result = json.dumps(chain.to_json(), indent=2, ensure_ascii=False)
            else:
                result = chain.to_markdown()
            return [{"type": "text", "text": result}]

        else:
            return [{"type": "text", "text": f"Error: Unknown tool '{name}'"}]

    except Exception as e:
        return [{"type": "text", "text": f"Error generating prompt: {str(e)}"}]


# ── MCP stdio transport ─────────────────────────────────────────────────────

def run_stdio():
    """Run MCP server on stdio (for OpenClaw/Claude Desktop integration)."""
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue

        method = msg.get("method", "")
        msg_id = msg.get("id")
        params = msg.get("params", {})

        if method == "initialize":
            result = handle_initialize(params)
        elif method == "tools/list":
            result = handle_tools_list()
        elif method == "tools/call":
            tool_name = params.get("name", "")
            tool_args = params.get("arguments", {})
            result = handle_tool_call(tool_name, tool_args)
        elif method == "notifications/initialized" or method == "cancelled":
            continue  # no response needed
        else:
            result = {"error": f"Unknown method: {method}"}

        if msg_id is not None:
            response = {"jsonrpc": "2.0", "id": msg_id, "result": result}
            sys.stdout.write(json.dumps(response) + "\n")
            sys.stdout.flush()


def run_http(host: str = "127.0.0.1", port: int = 8100):
    """Run MCP server on streamable-http (for remote agent integration)."""
    try:
        from http.server import HTTPServer, BaseHTTPRequestHandler
    except ImportError:
        print("HTTP server requires Python standard library", file=sys.stderr)
        sys.exit(1)

    class MCPHandler(BaseHTTPRequestHandler):
        def do_POST(self):
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length).decode("utf-8")
            try:
                msg = json.loads(body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "Invalid JSON"}).encode())
                return

            method = msg.get("method", "")
            msg_id = msg.get("id")
            params = msg.get("params", {})

            if method == "initialize":
                result = handle_initialize(params)
            elif method == "tools/list":
                result = handle_tools_list()
            elif method == "tools/call":
                tool_name = params.get("name", "")
                tool_args = params.get("arguments", {})
                result = handle_tool_call(tool_name, tool_args)
            else:
                result = {"error": f"Unknown method: {method}"}

            if msg_id is not None:
                response = {"jsonrpc": "2.0", "id": msg_id, "result": result}
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())

        def log_message(self, format, *args):
            pass  # Suppress default logging

    server = HTTPServer((host, port), MCPHandler)
    print(f"Trammel PE MCP Server running on http://{host}:{port}/mcp", file=sys.stderr)
    server.serve_forever()


def main():
    parser = argparse.ArgumentParser(description="Trammel PE MCP Server")
    parser.add_argument("--transport", choices=["stdio", "http"], default="stdio", help="Transport mode")
    parser.add_argument("--host", default="127.0.0.1", help="HTTP host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8100, help="HTTP port (default: 8100)")
    args = parser.parse_args()

    if args.transport == "stdio":
        run_stdio()
    else:
        run_http(args.host, args.port)


if __name__ == "__main__":
    main()