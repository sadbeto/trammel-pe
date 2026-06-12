"""
Trammel PE — CLI interface.

Usage:
    trammel-pe generate --config config.json --format markdown --output prompt.md
    trammel-pe quick "Analyze competitive landscape" --domain Marketing --depth deep
    trammel-pe template api-design --output api-prompt.md
    trammel-pe templates  # list available templates
"""

import argparse
import json
import sys
from pathlib import Path

from .core import TrammelPE, PromptData, TEMPLATES


def cmd_generate(args):
    """Generate a prompt from a JSON config file."""
    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Error: Config file not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)

    data = PromptData(**{k: v for k, v in config.items() if k in PromptData.__dataclass_fields__})
    trammel = TrammelPE(lang=data.lang or "en")

    fmt = args.format or "markdown"
    output = args.output

    content = trammel.save(data, format=fmt, path=output)
    if not output:
        print(content)
    else:
        print(f"✅ Prompt saved to {output}")


def cmd_quick(args):
    """Quick-generate a prompt from a single objective string."""
    tools = []
    if args.tools:
        tools = [t.strip() for t in args.tools.split(",")]

    data = PromptData(
        objective=args.objective,
        domain=args.domain or "",
        success_criteria=args.success_criteria or "",
        in_scope=args.in_scope or "",
        out_scope=args.out_scope or "",
        depth=args.depth or "standard",
        role=args.role or "",
        tone=args.tone or "professional",
        tools=tools,
        format_type=args.format or "markdown",
        length_target=args.length or "moderate",
        must_do=args.must_do or "",
        background=args.background or "",
        audience=args.audience or "",
        lang=args.lang or "en",
    )

    trammel = TrammelPE(lang=data.lang)
    fmt = args.format or "markdown"
    output = args.output

    content = trammel.save(data, format=fmt, path=output)
    if not output:
        print(content)
    else:
        print(f"✅ Prompt saved to {output}")


def cmd_template(args):
    """Generate a prompt from a built-in template."""
    template_id = args.template
    if template_id not in TEMPLATES:
        print(f"Error: Unknown template '{template_id}'", file=sys.stderr)
        print(f"Available templates: {', '.join(TEMPLATES.keys())}", file=sys.stderr)
        sys.exit(1)

    # Build overrides from CLI args
    overrides = {}
    if args.objective:
        overrides["objective"] = args.objective
    if args.domain:
        overrides["domain"] = args.domain
    if args.lang:
        overrides["lang"] = args.lang

    trammel = TrammelPE(lang=args.lang or "en")
    data = trammel.from_template(template_id, overrides=overrides or None)

    fmt = args.format or "markdown"
    output = args.output

    content = trammel.save(data, format=fmt, path=output)
    if not output:
        print(content)
    else:
        print(f"✅ Prompt saved to {output}")


def cmd_templates(args):
    """List available templates."""
    print("Available templates:")
    for tid, tpl in TEMPLATES.items():
        print(f"  {tid:20s} — {tpl['objective'][:60]}...")


def main():
    parser = argparse.ArgumentParser(
        prog="trammel-pe",
        description="Trammel PE — Generate structured, tool-aware prompts for any LLM agent",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # generate
    gen_parser = subparsers.add_parser("generate", help="Generate a prompt from a JSON config file")
    gen_parser.add_argument("--config", "-c", required=True, help="Path to JSON config file")
    gen_parser.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format")
    gen_parser.add_argument("--output", "-o", help="Output file path (stdout if omitted)")

    # quick
    quick_parser = subparsers.add_parser("quick", help="Quick-generate a prompt from an objective string")
    quick_parser.add_argument("objective", help="The objective/task description")
    quick_parser.add_argument("--domain", "-d", help="Domain of expertise")
    quick_parser.add_argument("--depth", choices=["quick", "standard", "deep", "expert"], help="Analysis depth")
    quick_parser.add_argument("--role", "-r", help="Role/persona for the agent")
    quick_parser.add_argument("--tone", "-t", choices=["professional", "concise", "academic", "creative", "conversational", "technical", "executive"], help="Output tone")
    quick_parser.add_argument("--tools", help="Comma-separated list of tool IDs")
    quick_parser.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format")
    quick_parser.add_argument("--length", "-l", choices=["brief", "moderate", "comprehensive", "unlimited"], help="Output length")
    quick_parser.add_argument("--success-criteria", "-s", help="What success looks like")
    quick_parser.add_argument("--in-scope", help="What's in scope")
    quick_parser.add_argument("--out-scope", help="What's out of scope")
    quick_parser.add_argument("--must-do", help="MUST DO rules")
    quick_parser.add_argument("--background", help="Background context")
    quick_parser.add_argument("--audience", help="Target audience")
    quick_parser.add_argument("--lang", choices=["en", "es", "pt"], default="en", help="Output language")
    quick_parser.add_argument("--output", "-o", help="Output file path (stdout if omitted)")

    # template
    tpl_parser = subparsers.add_parser("template", help="Generate a prompt from a built-in template")
    tpl_parser.add_argument("template", help="Template ID (use 'templates' command to list)")
    tpl_parser.add_argument("--objective", help="Override template objective")
    tpl_parser.add_argument("--domain", help="Override template domain")
    tpl_parser.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown", help="Output format")
    tpl_parser.add_argument("--lang", choices=["en", "es", "pt"], default="en", help="Output language")
    tpl_parser.add_argument("--output", "-o", help="Output file path (stdout if omitted)")

    # templates (list)
    subparsers.add_parser("templates", help="List available built-in templates")

    args = parser.parse_args()

    if args.command == "generate":
        cmd_generate(args)
    elif args.command == "quick":
        cmd_quick(args)
    elif args.command == "template":
        cmd_template(args)
    elif args.command == "templates":
        cmd_templates(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()