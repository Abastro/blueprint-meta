# Shared latexmk configuration, loaded by each document folder's .latexmkrc.
# It only says how to compile; which documents exist is up to
# docs/documents.json and the Makefile, which pass the root file explicitly.
# Output goes to the folder's build/ subfolder.
use strict;
use warnings;
use Cwd qw(getcwd);

our ($pdf_mode, $out_dir, $bibtex_use, $bibtex_fudge, $clean_ext);

$pdf_mode = 1;   # pdflatex
# Applies the same flags to every engine (-pdf, -lualatex, -xelatex).
set_tex_cmds('-synctex=1 -interaction=nonstopmode -file-line-error %O %S');

$out_dir = getcwd() . '/build';

$bibtex_use = 2;               # `latexmk -c` also removes the .bbl
# Run bibtex from the document folder, so \bibliography paths resolve
# relative to the .tex file (as for \input), not to build/.
$bibtex_fudge = 0;
$clean_ext .= ' synctex.gz';   # ... and the SyncTeX file

1;
