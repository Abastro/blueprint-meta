# Blueprint Skeleton

This is a skeleton project for research blueprints.

## Structure
- `docs/common/`: Shared preamble, macros, bibliography and latexmk configuration.
- `docs/main/`: The main document.

Each document lives in its own folder `docs/<name>/`, with root file `<name>.tex` and sections under `sections/`.
To add a document, copy `docs/main/` (including its `.latexmkrc`) to `docs/<name>/` and rename `main.tex` to `<name>.tex`.
A document can override shared macros in its own `commands.tex`, input after `../common/commands`.

## Building
Each folder builds `<name>.tex` into `<name>/build/<name>.pdf`.

```sh
cd docs/main && latexmk      # build
latexmk -pvc                 # rebuild on save
latexmk -c                   # remove build files except the PDF
```

### VS Code (LaTeX Workshop)
The project uses `.latexmkrc` to configure build, and outputs to the build folder.
Add to the VS Code settings:

```jsonc
"latex-workshop.latex.recipe.default": "latexmk (latexmkrc)",
"latex-workshop.latex.outDir": "%DIR%/build"
```
