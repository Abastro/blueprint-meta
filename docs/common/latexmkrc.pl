# Shared latexmk configuration, loaded by each document folder's .latexmkrc.
# Each folder docs/<name>/ builds <name>.tex into docs/<name>/build/<name>.pdf.
use strict;
use warnings;
use File::Basename qw(basename);
use Cwd qw(getcwd);

our ($pdf_mode, $out_dir, @default_files, $bibtex_use, $bibtex_fudge, $clean_ext);

$pdf_mode = 1;   # pdflatex
# Applies the same flags to every engine (-pdf, -lualatex, -xelatex).
set_tex_cmds('-synctex=1 -interaction=nonstopmode -file-line-error %O %S');

$out_dir       = getcwd() . '/build';
@default_files = (basename(getcwd()) . '.tex');

$bibtex_use = 2;               # `latexmk -c` also removes the .bbl
# Run bibtex from the document folder, so \bibliography paths resolve
# relative to the .tex file (as for \input), not to build/.
$bibtex_fudge = 0;
$clean_ext .= ' synctex.gz';   # ... and the SyncTeX file

1;
