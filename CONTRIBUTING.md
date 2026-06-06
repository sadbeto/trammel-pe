# Contributing to Trammel PE

Thank you for your interest in contributing! Trammel PE is built to be a community tool — simple, local, and useful for anyone working with LLMs and AI agents.

## 🌎 Idiomas / Languages

- [English](CONTRIBUTING.md) (you are here)
- [Español](CONTRIBUYENDO.md)

---

## Contributor Tiers

We value quality contributions from professionals with diverse backgrounds — engineering, physics, biology, mathematics, linguistics, and more. To maintain code quality, we use a tiered contributor system:

### 🌱 Proposed (New Contributors)

All new contributors start here. Your first contributions will be reviewed manually.

- **How to join:** Open an issue introducing yourself, or submit your first PR
- **PRs:** Require manual approval from a Maintainer before merge
- **Background:** We encourage you to share your professional background (engineering, science, etc.) in your first issue — this helps us match you with tasks that fit your expertise
- **Scope:** Bug fixes, translations, documentation improvements, template additions

### 🌿 Contributor

After 2+ merged PRs and consistent quality, you advance to Contributor.

- **PRs:** Require 1 Maintainer approval
- **Scope:** Feature additions, new language support, UI improvements
- **How to advance:** Consistent quality, good communication, understanding of project architecture

### 🌳 Maintainer

Trusted contributors with deep project knowledge. Currently JJ Solutions team members.

- **PRs:** Can approve other contributors' PRs
- **Scope:** Architecture decisions, breaking changes, release management
- **How to advance:** Nominated by existing Maintainers after sustained contribution

## How to Contribute

### Quick Start

1. **Fork** this repository
2. **Create** a feature branch: `git checkout -b my-feature`
3. **Make** your changes
4. **Test** by opening `index.html` in a browser
5. **Commit** with a clear message (see Commit Style below)
6. **Push** and open a Pull Request

### Commit Style

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `i18n:` Translations/internationalization
- `style:` UI/visual changes
- `refactor:` Code refactoring
- `test:` Testing additions

### Adding a Language

The i18n system uses a key-value object in `index.html` (the `I18N` object). To add a new language:

1. Copy the `en` object inside `I18N`
2. Change the key to your language code (e.g., `fr`, `de`, `ja`, `zh`)
3. Translate all values
4. Add a `<option>` to the `#langSelect` dropdown in the HTML
5. Test thoroughly — all sections, placeholders, and generated prompts must work
6. Update `README.md` and `CONTRIBUYENDO.md` with the new language info

### Adding a Template

Templates are defined in the `loadTemplate()` function. To add one:

1. Add a new entry to the `templates` object
2. Provide translations for `en`, `es`, and any other available languages (minimum `en` and `es`)
3. Make sure all fields are populated (objective, scope, tools, subtasks, etc.)
4. Test in all available languages

### Reporting Issues

- Open an issue on [Codeberg](https://codeberg.org/JJSOLUTIONS/trammel-pe/issues)
- Include browser version, OS, and steps to reproduce
- Screenshots help!
- Issues can be in **English or Español**

### Code Style

- **HTML/CSS/JS only** — no build tools, no frameworks, no Node.js
- **Keep it single-file** — the entire app lives in `index.html`
- **No external dependencies** — everything must work offline from a single file
- **Test across browsers** — Chrome, Firefox, Edge, Safari
- **All UI text must go through the i18n system** — no hardcoded strings in HTML

## What We Need

- 🌐 **More languages** — French, German, Japanese, Mandarin, Arabic, etc.
- 🎨 **UI/UX improvements** — Better mobile responsiveness, dark/light theme toggle, customizable layouts
- 📝 **More templates** — Data analysis, content writing, API design, security audit, project planning
- 🧪 **Testing** — Browser compatibility, accessibility testing
- 📖 **Documentation** — Tutorials, video walkthroughs, blog posts
- 🔧 **Features** — Prompt versioning, export to file, prompt chaining, MCP server integration

## Code of Conduct

- Be respectful and constructive
- Focus on making Trammel PE better for everyone
- No discrimination, harassment, or toxicity
- Contributions in any language are welcome, but code comments should be in English

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).