# Sphinx configuration for the Loci Framework Specification wiki.
# This file is processed from wiki/_build/src/ after wikilink preprocessing.

project   = "Loci Framework Specification"
copyright = "Mississippi State University"
author    = "Edward A. Luke et al."
release   = "0.6.0"

extensions = [
    "myst_parser",
    "sphinx.ext.mathjax",
]

myst_enable_extensions = [
    "colon_fence",   # :::directive syntax as alternative to ```{directive}
    "deflist",       # definition lists
    "tasklist",      # - [ ] task items
    "dollarmath",    # $...$ inline and $$...$$ display math
]

# Treat all .md files as MyST Markdown.
source_suffix = {
    ".md":  "markdown",
    ".rst": "restructuredtext",
}

root_doc = "index"

html_theme = "furo"

html_theme_options = {
    "sidebar_hide_name": False,
    "navigation_with_keys": True,
}

html_title = "Loci Specification"

# Pages not in any toctree (stubs) are intentional — suppress the warning.
# Also suppress unknown lexer warnings (Loci source uses ```cpp as the fence
# language since Pygments has no native Loci lexer).
suppress_warnings = ["toc.excluded", "misc.highlighting_failure"]

exclude_patterns = ["_build", "_tools", "Thumbs.db", ".DS_Store"]
