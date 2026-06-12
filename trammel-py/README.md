# Trammel PE — Python SDK & CLI

**Programmatic prompt generation from the Trammel PE framework.**

Generate structured, tool-aware, self-improving prompts for any LLM agent — from Python or the command line. No browser needed.

## Install

```bash
pip install -e .
# or
pip install trammel-pe
```

## Quick Start

### Python Library

```python
from trammel_pe import TrammelPE, PromptData

# Build a prompt programmatically
data = PromptData(
    objective="Design a REST API for a construction project management platform",
    domain="Software Engineering",
    success_criteria="OpenAPI-style endpoint list with auth flows, schemas, and error handling",
    in_scope="CRUD for projects/teams/tasks, JWT auth, RBAC, rate limiting",
    out_scope="Frontend, deployment infra, billing",
    depth="deep",
    role="Senior backend architect specializing in API design and construction tech",
    tone="technical",
    tools=["code_execution", "file_read_write", "web_search"],
    must_do="Use consistent naming. Define error envelope. Specify auth on every endpoint.",
    format_type="mixed",
    length_target="comprehensive",
    subtasks=[
        {"name": "Resource Model", "desc": "Define entities, relationships, and schemas for construction projects", "data": "Project, Team, Task, Milestone, Blueprint entities"},
        {"name": "Endpoints & Auth", "desc": "Map routes, methods, auth scopes, and errors", "data": "Route table, JWT claims, status codes"},
    ],
)

trammel = TrammelPE()
prompt_md = trammel.generate_markdown(data)
prompt_json = trammel.generate_json(data)

# Save to file
trammel.save(data, format="markdown", path="output/prompt.md")
```

### CLI

```bash
# Generate from JSON config
trammel-pe generate --config prompt-config.json --format markdown --output prompt.md

# Quick one-liner
trammel-pe quick "Analyze competitive landscape for a SaaS startup in LATAM" --domain "Marketing" --depth deep --output competitive.md

# Use a built-in template
trammel-pe template api-design --output api-prompt.md

# Pipe to stdout
trammel-pe quick "Review this codebase" --format json
```

### Agent Integration (OpenClaw / LangChain / CrewAI)

```python
from trammel_pe import TrammelPE

trammel = TrammelPE()

# Generate prompt and pass to any agent framework
prompt = trammel.generate_markdown(data)

# For OpenClaw — save as .md and reference in agent config
trammel.save(data, format="markdown", path="agents/prompts/buildera-dap.md")

# For LangChain — use as prompt template
from langchain_core.prompts import ChatPromptTemplate
chain_prompt = ChatPromptTemplate.from_template(prompt)
```

## PromptData Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `objective` | str | ✅ | What you want done (verb-first) |
| `domain` | str | ❌ | Domain of expertise |
| `success_criteria` | str | ❌ | What "done" looks like |
| `in_scope` | str | ❌ | What's included |
| `out_scope` | str | ❌ | What's excluded |
| `depth` | str | ❌ | `quick`/`standard`/`deep`/`expert` |
| `role` | str | ❌ | Who the AI should be |
| `tone` | str | ❌ | `professional`/`concise`/`academic`/`creative`/`conversational`/`technical`/`executive` |
| `tools` | list | ❌ | Tools the agent should use |
| `subtasks` | list | ❌ | Task decomposition with data focus |
| `format_type` | str | ❌ | `markdown`/`json`/`table`/`bulletlist`/`narrative`/`code`/`mixed` |
| `length_target` | str | ❌ | `brief`/`moderate`/`comprehensive`/`unlimited` |
| `background` | str | ❌ | Context / background info |
| `input_data` | str | ❌ | Input data for the agent |
| `audience` | str | ❌ | Target audience |
| `constraints` | str | ❌ | MUST NOT rules |
| `must_do` | str | ❌ | MUST DO rules |
| `edge_cases` | str | ❌ | Edge cases to handle |
| `self_learn` | bool | ❌ | Enable self-learning loop |
| `iteration_strategy` | str | ❌ | `reflect`/`validate`/`research_more`/`all` |
| `max_iterations` | int | ❌ | Max self-learning iterations |
| `improvement_focus` | str | ❌ | What to improve each iteration |
| `lang` | str | ❌ | `en`/`es`/`pt` — output language |

## Built-in Templates

| Template ID | Description |
|-------------|-------------|
| `competitive` | Competitive landscape analysis |
| `data-analysis` | Data exploration and insights |
| `content-writing` | SEO-optimized blog post |
| `api-design` | REST API design |
| `code-review` | PR review with findings |
| `security-audit` | Web app vulnerability audit |

## Output Formats

### Markdown (default)
Structured prompt with emoji headers, ready to paste into any LLM.

### JSON
Machine-readable structured object for APIs and multi-agent systems.

### Formatted
Visual HTML preview (available in browser only).

## License

MIT — Same as Trammel PE parent project.