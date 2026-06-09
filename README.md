<div align="center">

# 🛠️ Trammel PE

### Trace the arc from idea to execution

**Build structured, tool-aware prompts for any LLM agent — in 3 languages**

[🇺🇸 English](#features) · [🇵🇷 Español](#características) · [🇧🇷 Português](#funcionalidades)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![No Dependencies](https://img.shields.io/badge/dependencies-zero-orange.svg)]()
[![Languages](https://img.shields.io/badge/languages-3-yellow.svg)](#multi-language)

*A trammel is the precision tool that traces the perfect arc — the carpenter's large compass that maintains the exact distance while drawing curves. Trammel PE does the same for prompts: traces the arc between your objective and the agent's perfect execution.*

</div>

---

## What is Trammel PE?

Trammel PE (Prompt Engineering) is a **local, zero-dependency HTML tool** that transforms vague task ideas into **structured, tool-aware, self-improving prompts** for any LLM or AI agent.

Unlike simple "prompt templates," Trammel PE forces you to think through:

- **What tools** the agent should use
- **How to decompose** a complex task into focused sub-tasks with concentrated data
- **What success looks like** before you start
- **Whether the agent should self-iterate** and improve its own output

**The result:** Prompts that produce better, more specific, more actionable outputs from any LLM.

## Features

| Step | Section | What It Does |
|------|---------|-------------|
| 1 | 🎯 **Objective** | Define what you want done (verb-first), domain, and success criteria |
| 2 | 🔭 **Scope** | Set IN/OUT boundaries and depth level |
| 3 | 🛠️ **Tools** | Select which tools the agent should leverage |
| 4 | 🧩 **Task Decomposition** | Break into sub-tasks with focused data per task |
| 5 | 🎭 **Role & Persona** | Define who the AI should be and its tone |
| 6 | 📋 **Output Format** | Choose format, length, custom instructions |
| 7 | 📚 **Context & Data** | Provide background, input data, target audience |
| 8 | 🚧 **Constraints** | Set MUST/MUST NOT rules and edge cases |
| 9 | 🔄 **Self-Learning Loop** | Configure iteration strategy and improvement focus |

### Key Capabilities

- **⚡ Quick Builder Mode** — Default workflow: describe the task once, tap use-case cards and chips, get a complete structured prompt
- **❓ Smart Questions** — Optional 3-question helper that improves the prompt without forcing a long form
- **🛠️ Advanced Builder** — Full 9-section framework remains available for precision prompting
- **🛠️ Tool Selection** — Explicitly tell the agent which tools to use (web search, code, APIs, databases, etc.)
- **🧩 Task Decomposition** — Break complex objectives into sub-tasks with concentrated data focus per task
- **🔄 Self-Learning Loop** — Agent iterates on its own output: reflect, validate, research gaps
- **📋 3 Output Formats** — Formatted (visual), Markdown (copy-paste), JSON (for APIs and multi-agent systems)
- **📊 Quality Scoring** — Live completeness, specificity, and token count as you fill in fields
- **🌐 Multi-Language** — Full interface + generated prompts in English, Español, and Português
- **🔒 100% Local** — Zero servers, zero tracking, zero dependencies. Open the HTML file and go.
- **📋 Built-in Templates** — 6 templates: Competitive Analysis, Data Analysis, Content Writing, API Design, Code Review, Security Audit
- **📚 Prompt Library** — Save prompts to `localStorage`, keep multiple versions per prompt, reload any version
- **⬇️ Export / Import** — Download as `.md` / `.json` / `.txt`, or paste JSON to import back into the form (round-trip)
- **🌗 Theme Toggle** — Switch dark/light, preference persists across sessions

## Multi-Language

The entire interface — labels, placeholders, section headers, generated prompts, and template content — switches instantly when you select a language:

| 🇺🇸 English | 🇵🇷 Español | 🇧🇷 Português |
|---|---|---|
| Objective | Objetivo | Objetivo |
| Scope | Alcance | Escopo |
| Tools | Herramientas | Ferramentas |
| Task Decomposition | Descomposición de Tareas | Decomposição de Tarefas |
| Constraints | Restricciones | Restrições |
| Self-Learning Loop | Bucle de Auto-Aprendizaje | Loop de Auto-Aprendizado |

**Generated prompts are also fully translated** — section headers, instructions, and loop steps all output in the selected language.

## Características

Trammel PE es una **herramienta HTML local sin dependencias** que transforma ideas vagas en **prompts estructurados, con herramientas y auto-mejorables** para cualquier LLM o agente de IA.

- **🛠️ Selección de Herramientas** — Indica explícitamente qué herramientas debe usar el agente
- **🧩 Descomposición de Tareas** — Divide objetivos complejos en subtareas con datos concentrados
- **🔄 Bucle de Auto-Aprendizaje** — El agente itera sobre su propia salida
- **📋 3 Formatos de Salida** — Formateado (visual), Markdown, JSON (para APIs y multi-agente)
- **🌐 3 Idiomas** — Interfaz completa y prompts generados en Inglés, Español y Portugués
- **🔒 100% Local** — Cero servidores, cero tracking, cero dependencias

## Funcionalidades

O Trammel PE é uma **ferramenta HTML local sem dependências** que transforma ideias vagas em **prompts estruturados, com ferramentas e auto-melhoráveis** para qualquer LLM ou agente de IA.

- **🛠️ Seleção de Ferramentas** — Indique explicitamente quais ferramentas o agente deve usar
- **🧩 Decomposição de Tarefas** — Divida objetivos complexos em subtarefas com dados concentrados
- **🔄 Loop de Auto-Aprendizado** — O agente itera sobre sua própria saída
- **📋 3 Formatos de Saída** — Formatado (visual), Markdown, JSON (para APIs e multi-agente)
- **🌐 3 Idiomas** — Interface completa e prompts gerados em Inglês, Espanhol e Português
- **🔒 100% Local** — Zero servidores, zero tracking, zero dependências

## Why Trammel PE?

Most prompt generators stop at "Role + Task + Context." That's not enough for real agent work.

| Other Prompt Builders | Trammel PE |
|---|---|
| Role/Task/Context only | 9-section structured framework |
| No tool selection | Explicit tool specification |
| No task decomposition | Sub-tasks with data focus |
| No self-improvement loop | Configurable iteration strategy |
| English only | 3 languages (EN/ES/PT) |
| Server-dependent or SaaS | 100% local, zero dependencies |
| Single output format | Formatted + Markdown + JSON |
| No quality feedback | Live completeness & specificity scoring |

### Research Behind It

Trammel PE synthesizes best practices from:

- **RCTFCE Framework** (Role-Context-Task-Format-Constraints-Examples)
- **6-Band sinc** (PERSONA-CONTEXT-DATA-CONSTRAINTS-FORMAT-TASK)
- **2026 Prompt Format Patterns** — FutureAGI
- **7-Phase Reverse Engineering Protocol**
- **DSPy** — Declarative Self-improving Python
- **Anthropic/OpenAI/Google prompt engineering guides**

## Getting Started

### Quick Start

1. **Download** `index.html` from this repo
2. **Open** it in any modern browser
3. **Fill in** the form — start with Objective
4. **Copy** the generated prompt and paste into any LLM

That's it. No install. No server. No API key.

### From Source

```bash
git clone https://codeberg.org/JJSolutions/trammel-pe.git
cd trammel-pe
# Open index.html in your browser
open index.html       # macOS
xdg-open index.html   # Linux
start index.html      # Windows
```

## How to Use

### Quick Builder (default)

1. **Describe the task** — one or two sentences is enough
2. **Pick the job** — Email, Summary, Data, PRD, Code Review, Research, Agent Workflow, etc.
3. **Tune with chips** — tone, depth, output format, target AI
4. **Generate** — Trammel builds the structured prompt for you
5. **Optional:** click **Ask me 3 questions** to sharpen the prompt without filling a long form

### Advanced Builder

Use **Advanced Builder** when you need precise control over the full framework:

1. **Define your Objective** — Start with a verb, be specific
2. **Set Scope** — What's IN, what's OUT, how deep
3. **Select Tools** — Pick the tools the agent should use
4. **Decompose Tasks** — Break it into sub-tasks with data focus
5. **Set Role & Tone** — Who should the AI be?
6. **Choose Format** — Markdown, JSON, tables, or mixed
7. **Add Context** — Background, data, audience
8. **Set Constraints** — MUST and MUST NOT rules
9. **Enable Self-Learning** — Let the agent iterate and improve

Switch between **Formatted**, **Markdown**, and **JSON** tabs for different output formats.

## Output Formats

### Formatted
Visual preview with syntax-highlighted sections. Good for reviewing.

### Markdown
Raw copy-paste text. Paste directly into ChatGPT, Claude, Gemini, or any LLM.

### JSON
Machine-readable structured object. Use with APIs, multi-agent systems (OpenClaw, AutoGPT, CrewAI, Linear agents).

## Contributing

Contributions are welcome! We value contributors from **diverse professional backgrounds** — engineering, physics, biology, mathematics, linguistics, and more.

📄 **Guidelines:** [CONTRIBUTING.md](CONTRIBUTING.md) (English) · [CONTRIBUYENDO.md](CONTRIBUYENDO.md) (Español)

### Contributor Tiers

| Tier | PRs | Description |
|------|-----|-------------|
| 🌱 **Proposed** | Require manual Maintainer approval | New contributors — share your professional background! |
| 🌿 **Contributor** | Require 1 Maintainer approval | After 2+ merged PRs with consistent quality |
| 🌳 **Maintainer** | Can approve PRs | Trusted contributors with deep project knowledge |

All PRs require Maintainer approval before merge. No direct pushes to `main`.

### 🌎 Comunidad Latina

¡Hablamos español! La comunidad latina es bienvenida. Issues y PRs pueden ser en **inglés o español**. Los templates de issues incluyen un formulario de introducción donde puedes compartir tu formación profesional.

### Areas We Need Help With

- 🌐 **More languages** — French, German, Japanese, Mandarin, Arabic, etc.
- 🎨 **UI/UX improvements** — Better mobile responsiveness, dark/light theme toggle, customizable layouts
- 📝 **More templates** — Data analysis, content writing, API design, security audit, project planning
- 🧪 **Testing** — Browser compatibility, accessibility testing
- 📖 **Documentation** — Tutorials, video walkthroughs, blog posts
- 🔧 **Features** — Prompt versioning, export to file, prompt chaining, MCP server integration

## Roadmap

- [ ] More languages (FR, DE, JA, ZH, AR)
- [ ] MCP server for agent integration
- [x] Prompt versioning & history (localStorage)
- [x] Export to file (.md, .json)
- [ ] Prompt chaining (link multiple prompts)
- [x] Dark/light theme toggle
- [ ] Customizable UI layouts
- [ ] Mobile-responsive improvements
- [x] More built-in templates
- [ ] Quality scoring algorithm improvements
- [ ] Integration guides for OpenClaw, AutoGPT, CrewAI
- [ ] Contributor evaluation system (professional background review)

## License

[MIT License](LICENSE) — Free for personal and commercial use.

---

<div align="center">

**Built by [JJ Solutions](https://codeberg.org/JJSolutions)** 🇵🇷

*Trammel PE — Trace the arc from idea to execution*

If Trammel PE helps you build better prompts, ⭐ star this repo and share it!

</div>