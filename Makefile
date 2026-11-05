# Builds the documents listed in docs/documents.json.
#
#   make          build every document
#   make <dir>    build one: docs/<dir>/<name>.tex -> docs/<dir>/build/<name>.pdf
#   make dist     build every document and collect the PDFs in dist/<name>.pdf
#   make check    check docs/documents.json against the docs/ folders
#   make json     print the documents as a JSON array (used by CI)
#   make clean    remove every document's build folder, and dist/
#
# How each document compiles is up to latexmk and docs/common/latexmkrc.pl.

PYTHON  ?= python3
LATEXMK ?= latexmk
DIST    ?= dist

# "<dir>/<name>" per document. The script checks the manifest first, so a
# broken manifest stops every target here, with the problems printed above.
DOCUMENTS := $(shell $(PYTHON) scripts/documents.py list)
ifneq ($(.SHELLSTATUS),0)
  $(error Fix docs/documents.json or the docs/ folders first)
endif

DIRS    := $(foreach d,$(DOCUMENTS),$(firstword $(subst /, ,$(d))))
name_of  = $(notdir $(filter $(1)/%,$(DOCUMENTS)))

.PHONY: all dist check json clean $(DIRS)

all: $(DIRS)

# latexmk tracks each document's dependencies itself, so always run it.
$(DIRS):
	cd docs/$@ && $(LATEXMK) $(call name_of,$@).tex

# Rebuilt from scratch, so it holds exactly the current documents.
dist: all
	rm -rf $(DIST)
	mkdir -p $(DIST)
	$(foreach d,$(DOCUMENTS),cp docs/$(dir $(d))build/$(notdir $(d)).pdf $(DIST)/ &&) true

check:
	@$(PYTHON) scripts/documents.py check

json:
	@$(PYTHON) scripts/documents.py json

clean:
	rm -rf $(foreach d,$(DIRS),docs/$(d)/build) $(DIST)
