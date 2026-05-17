# Sphinx configuration for the Loci Framework Developer Reference.
# This file is processed from wiki/_build/src/ after wikilink preprocessing.

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "_ext"))

project   = "Loci Framework Developer Reference"
copyright = "Mississippi State University"
author    = "Edward A. Luke et al."
release   = "0.7.0"

extensions = [
    "myst_parser",
    "sphinx.ext.mathjax",
    "attribution",
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

html_title = "Loci Developer Reference"

# Pages not in any toctree (stubs) are intentional — suppress the warning.
# Also suppress unknown lexer warnings (Loci source uses ```cpp as the fence
# language since Pygments has no native Loci lexer).
suppress_warnings = ["toc.excluded", "misc.highlighting_failure"]

exclude_patterns = ["_build", "_tools", "_ext", "Thumbs.db", ".DS_Store"]
