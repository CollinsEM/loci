# Loci Specification Wiki — HTML build via Sphinx + MyST-Parser
#
# Quick start:
#   make install-deps   # install Python packages (once)
#   make html           # build → _build/html/index.html
#   make serve          # build and serve on http://localhost:8000

PYTHON      := python3
SPHINXBUILD := sphinx-build
SPHINXOPTS  :=
WIKIDIR     := .
SRCDIR      := _build/src
HTMLDIR     := _build/html
TOOLSDIR    := _tools

# All wiki Markdown sources (excluding the build tree).
MD_SOURCES := $(shell find $(WIKIDIR) -name '*.md' -not -path './_build/*' \
                                                    -not -path './_tools/*')

.PHONY: all html preprocess clean serve install-deps help

all: html

## help         Show this help message
help:
	@grep -E '^## ' $(MAKEFILE_LIST) | sed 's/^## /  /'

## install-deps Install required Python packages
install-deps:
	pip3 install -r requirements.txt

## preprocess   Resolve wikilinks and stage sources for Sphinx
preprocess: $(MD_SOURCES) conf.py
	@echo "==> Preprocessing wiki sources..."
	$(PYTHON) $(TOOLSDIR)/resolve_wikilinks.py $(WIKIDIR) $(SRCDIR)

## html         Build HTML documentation
html: preprocess
	@echo "==> Running Sphinx..."
	$(SPHINXBUILD) -b html $(SPHINXOPTS) $(SRCDIR) $(HTMLDIR)
	@echo ""
	@echo "Done. Open: $(HTMLDIR)/index.html"

## clean        Remove all build artifacts
clean:
	rm -rf _build

## serve        Build HTML and serve locally on port 8000
serve: html
	@echo "Serving at http://localhost:8000  (Ctrl-C to stop)"
	cd $(HTMLDIR) && $(PYTHON) -m http.server 8000
