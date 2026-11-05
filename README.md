# Blueprint Skeleton

This is a skeleton project for research blueprints.

## Structure
- `docs/common/` contains the shared contents like preamble.
- `docs/main/` contains skeleton of a document. The format supports multiple documents.

### VS Code (LaTeX Workshop)
The project uses `.latexmkrc` to configure build, and outputs to the build folder.
Add to the VS Code settings:

```jsonc
"latex-workshop.latex.recipe.default": "latexmk (latexmkrc)",
"latex-workshop.latex.outDir": "%DIR%/build"
```
