"""
attribution.py — Sphinx extension that renders attribution and review banners.

Reads two frontmatter fields on each page:
  attribution: human | llm | mixed   (default: human — no banner)
  reviewed:    true  | false         (default: false — banner shown)

A single combined banner is injected immediately after the page title:

  attribution=llm,   reviewed=false  → warning  (AI-generated, unreviewed)
  attribution=llm,   reviewed=true   → note     (AI-generated, reviewed)
  attribution=mixed, reviewed=false  → warning  (mixed content, unreviewed)
  attribution=mixed, reviewed=true   → note     (mixed content, reviewed)
  attribution=human, reviewed=false  → note     (human-written, unreviewed)
  attribution=human, reviewed=true   → (no banner)
"""

from docutils import nodes
from sphinx.application import Sphinx


def _note(text: str) -> nodes.note:
    node = nodes.note()
    node += nodes.paragraph(text=text)
    return node


def _warning(text: str) -> nodes.warning:
    node = nodes.warning()
    node += nodes.paragraph(text=text)
    return node


def _build_banner(attribution: str, reviewed: bool):
    if attribution == "llm" and not reviewed:
        return _warning(
            "This page was generated with the assistance of an AI language model "
            "and has not yet been reviewed by a subject matter expert. "
            "Content may be inaccurate or incomplete."
        )
    if attribution == "llm" and reviewed:
        return _note(
            "This page was generated with the assistance of an AI language model "
            "and has been reviewed by a subject matter expert."
        )
    if attribution == "mixed" and not reviewed:
        return _warning(
            "This page contains a mix of human-written and AI-generated content "
            "and has not yet been reviewed by a subject matter expert."
        )
    if attribution == "mixed" and reviewed:
        return _note(
            "This page contains a mix of human-written and AI-generated content "
            "and has been reviewed by a subject matter expert."
        )
    if attribution == "human" and not reviewed:
        return _note(
            "This page has not yet been reviewed by a subject matter expert."
        )
    # attribution == "human" and reviewed
    return _note(
        "This page was written by a subject matter expert."
    )


def inject_banner(app, doctree, docname):
    meta = app.env.metadata.get(docname, {})
    attribution = str(meta.get("attribution", "human")).lower()
    reviewed_raw = meta.get("reviewed", False)
    if isinstance(reviewed_raw, bool):
        reviewed = reviewed_raw
    else:
        reviewed = str(reviewed_raw).lower() not in ("false", "no", "0")

    banner = _build_banner(attribution, reviewed)
    if banner is None:
        return

    for section in doctree.traverse(nodes.section):
        for i, child in enumerate(section.children):
            if isinstance(child, nodes.title):
                section.insert(i + 1, banner)
                return  # insert once, in the outermost section only


def setup(app: Sphinx):
    app.connect("doctree-resolved", inject_banner)
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
