# Contributing to Trammel PE

Thank you for your interest in contributing! Trammel PE is built to be a community tool — simple, local, and useful for anyone working with LLMs and AI agents.

## How to Contribute

### Quick Contributions

1. **Fork** this repository
2. **Create** a feature branch: `git checkout -b my-feature`
3. **Make** your changes
4. **Test** by opening `index.html` in a browser
5. **Commit** with a clear message
6. **Push** and open a Pull Request

### Reporting Issues

- Open an issue on [Codeberg](https://codeberg.org/JJSolutions/trammel-pe/issues)
- Include browser version, OS, and steps to reproduce
- Screenshots help!

### Adding a Language

The i18n system uses a simple key-value object in `index.html` (the `I18N` object). To add a new language:

1. Copy the `en` object inside `I18N`
2. Change the key to your language code (e.g., `fr`, `de`, `ja`)
3. Translate all values
4. Add a `<option>` to the `#langSelect` dropdown in the HTML
5. Test thoroughly — make sure all sections, placeholders, and generated prompts work

### Adding a Template

Templates are defined in the `loadTemplate()` function. To add one:

1. Add a new entry to the `templates` object
2. Provide translations for `en`, `es`, and `pt` (minimum)
3. Make sure all fields are populated
4. Test in all 3 languages

### Code Style

- **HTML/CSS/JS only** — no build tools, no frameworks, no Node.js
- **Keep it single-file** — the entire app lives in `index.html`
- **No external dependencies** — everything must work offline from a single file
- **Test across browsers** — Chrome, Firefox, Edge, Safari

### What We Need

- 🌐 More language translations (French, German, Japanese, Mandarin, etc.)
- 🎨 UI/UX improvements (mobile responsiveness, accessibility)
- 📝 More built-in templates (data analysis, content writing, API design)
- 🧪 Cross-browser testing and bug reports
- 📖 Documentation (tutorials, walkthroughs, blog posts)
- 🔧 New features (prompt versioning, export, chaining)

## Code of Conduct

- Be respectful and constructive
- Focus on making Trammel PE better for everyone
- No discrimination, harassment, or toxicity

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).