# Research Template
This is a template project for research.

## Structure
- `docs/documents.json` is the metadata file for documents.
- `docs/common/` contains the shared contents for documents.
- `docs/main/` contains skeleton of a document.

### Metadata
Each entry has a `dir`, a `name` and a `title`:
its root file is `docs/<dir>/<name>.tex`, which builds to `docs/<dir>/build/<name>.pdf`.
The title is shown on the release page.

## Adding a Document
To add a document, copy `docs/main/` to `docs/<dir>/`, rename its root file to `<name>.tex`,
and add it to `docs/documents.json`.

`make check` reports any mismatch between the two.

## Build
- `make` builds every document.
- `make <dir>` builds a document for the directory.
- `make dist` builds every document and collects the PDFs in `dist/`.
- `make check` checks the `docs/documents.json` against the folders.
- `make clean` removes the build folders.

## IDE Setup
The project uses `.latexmkrc` to configure build, and outputs to the build folder.

### VS Code (LaTeX Workshop)
Add to the VS Code settings:

```jsonc
"latex-workshop.latex.recipe.default": "latexmk (latexmkrc)",
"latex-workshop.latex.outDir": "%DIR%/build"
```
