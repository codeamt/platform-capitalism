# Documentation

This directory contains the MkDocs documentation for the Platform Capitalism Simulation.

## Local Development

### Serve Docs Locally

```bash
make docs-serve
```

Or directly:

```bash
mkdocs serve
```

Open `http://localhost:8000` to view the documentation.

### Build Docs

```bash
make docs-build
```

Output will be in `site/` directory.

## Deployment

Documentation is automatically deployed to GitHub Pages when changes are pushed to the `main` branch.

**Live Docs:** https://codeamt.github.io/platform-capitalism

### Manual Deployment

```bash
make docs-deploy
```

Or directly:

```bash
mkdocs gh-deploy --force
```

## Structure

```
docs/
├── index.md                    # Home page
├── architecture/               # System architecture
│   ├── overview.md
│   ├── agents.md
│   ├── policy-engine.md
│   ├── environment.md
│   └── ui.md
├── research/                   # Research documentation
│   ├── framework.md
│   ├── cpm-economics.md
│   ├── state-machine.md
│   └── capital-conversion.md
├── development/                # Development guides
│   ├── getting-started.md
│   ├── testing.md
│   ├── deployment.md
│   └── contributing.md
└── api/                        # API reference
    ├── agents.md
    ├── policy-engine.md
    └── scenarios.md
```

## Writing Documentation

### Markdown Features

MkDocs supports:

- **Mermaid diagrams** - For flowcharts and architecture
- **Code highlighting** - Syntax highlighting for Python, bash, etc.
- **Admonitions** - Info, warning, danger boxes
- **Tabs** - Tabbed content sections
- **Tables** - Markdown tables

### Example: Mermaid Diagram

\`\`\`mermaid
graph LR
    A[Start] --> B[Process]
    B --> C[End]
\`\`\`

### Example: Admonition

\`\`\`markdown
!!! note "Important"
    This is an important note.
\`\`\`

### Example: Code Block

\`\`\`python
def example():
    return "Hello, world!"
\`\`\`

## Configuration

Documentation is configured in `mkdocs.yml` at the project root.

### Theme

Using Material for MkDocs with:
- Dark/light mode toggle
- Navigation tabs
- Search
- Code copy buttons

### Plugins

- **search** - Full-text search
- **mermaid2** - Mermaid diagram support

## Contributing

When adding new documentation:

1. Create markdown files in appropriate directory
2. Add to navigation in `mkdocs.yml`
3. Test locally with `make docs-serve`
4. Push to GitHub - docs auto-deploy

## Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Mermaid Diagrams](https://mermaid.js.org/)
