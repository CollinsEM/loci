"""
attribution.py — Sphinx extension that renders attribution and review badges.

Reads two frontmatter fields on each page:
  attribution: human | llm | mixed   (default: human)
  reviewed:    true  | false         (default: false)

A small colored badge is injected immediately after the page title. Hovering
over it shows a CSS tooltip; clicking it jumps to a compact attribution notice
anchored at the bottom of the page.

Badge variants:
  llm   + unreviewed → warning  (amber)
  llm   + reviewed   → info     (blue)
  mixed + unreviewed → warning  (amber)
  mixed + reviewed   → info     (blue)
  human + unreviewed → caution  (yellow)
  human + reviewed   → success  (green)
"""

from docutils import nodes
from sphinx.application import Sphinx

# (attribution, reviewed) → (css_modifier, icon, short_label, full_message)
_BADGE = {
    ("llm",   False): ("warning", "🤖", "AI-generated · Unreviewed",
        "This page was generated with the assistance of an AI language model "
        "and has not yet been reviewed by a subject matter expert. "
        "Content may be inaccurate or incomplete."),
    ("llm",   True):  ("info",    "🤖", "AI-generated · SME-reviewed",
        "This page was generated with the assistance of an AI language model "
        "and has been reviewed by a subject matter expert."),
    ("mixed", False): ("warning", "🤖", "Partially AI-generated · Unreviewed",
        "This page contains a mix of human-written and AI-generated content "
        "and has not yet been reviewed by a subject matter expert."),
    ("mixed", True):  ("info",    "🤖", "Partially AI-generated · SME-reviewed",
        "This page contains a mix of human-written and AI-generated content "
        "and has been reviewed by a subject matter expert."),
    ("human", False): ("caution", "⚠", "Unreviewed",
        "This page has not yet been reviewed by a subject matter expert."),
    ("human", True):  ("success", "✓", "SME-reviewed",
        "This page was written and reviewed by a subject matter expert."),
}

_ANCHOR = "doc-attribution"


def _parse_reviewed(value):
    if isinstance(value, bool):
        return value
    return str(value).lower() not in ("false", "no", "0")


def inject_badge(app, doctree, docname):
    meta = app.env.metadata.get(docname, {})
    attribution = str(meta.get("attribution", "human")).lower()
    reviewed = _parse_reviewed(meta.get("reviewed", False))

    key = (attribution, reviewed)
    if key not in _BADGE:
        return

    css_mod, icon, label, full_msg = _BADGE[key]
    tooltip = full_msg.replace('"', "&quot;")

    badge_html = (
        f'<div class="attr-badge-wrap">'
        f'<a class="attr-badge attr-badge--{css_mod}" '
        f'href="#{_ANCHOR}" '
        f'data-tooltip="{tooltip}" '
        f'aria-label="{tooltip}">'
        f'{icon}&nbsp;{label}'
        f'</a>'
        f'</div>\n'
    )

    notice_html = (
        f'<hr class="attr-separator">'
        f'<div id="{_ANCHOR}" class="attr-notice attr-notice--{css_mod}">'
        f'<strong>Attribution:</strong> {full_msg}'
        f'</div>\n'
    )

    badge_node = nodes.raw("", badge_html, format="html")
    notice_node = nodes.raw("", notice_html, format="html")

    # Insert badge right after the outermost section title.
    for section in doctree.traverse(nodes.section):
        for i, child in enumerate(section.children):
            if isinstance(child, nodes.title):
                section.insert(i + 1, badge_node)
                break
        break

    # Append notice at the end of the document body.
    doctree += notice_node


def setup(app: Sphinx):
    app.connect("doctree-resolved", inject_badge)
    app.add_css_file("attribution.css")
    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
