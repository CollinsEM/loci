#!/usr/bin/env python3
"""
Preprocess Loci wiki Markdown for Sphinx.

Steps performed for each .md file:
  1. Resolve [[target/path|Display Text]] wikilinks to correct relative
     Markdown links, e.g. [Display Text](../target/path.md).
     If the display text is omitted the last path component is used.
  2. For index.md only: append a single hidden {toctree} listing each
     section's index page, giving Furo a two-level hierarchy for
     collapsible sidebar navigation.
  3. For existing section index pages (fvm/index, runtime/index): append a
     hidden {toctree} listing the section's sub-pages (for navigation;
     the inline wikilinks on the page already serve as visible links).
  4. For sections without a source index page: generate a minimal index
     page in the output directory with a visible {toctree} of the
     section's pages.

Usage:
    python3 resolve_wikilinks.py <wiki_src_dir> <output_dir>

The output directory is created fresh on each run (previous contents
are removed). conf.py and any _static/ directory are copied verbatim.
"""

import os
import re
import shutil
import sys
from pathlib import Path

WIKILINK_RE = re.compile(r'\[\[([^\]|]+?)(?:\|([^\]]+?))?\]\]')

# Section config: (directory, display title, existing-index-stem or None)
# Sections with an existing index use it as the collapsible section node.
# Sections without one get an auto-generated index in the build output.
SECTIONS = [
    ("principles",            "Foundational Principles",   None),
    ("core-data-model",       "Core Data Model",           None),
    ("rule-system",           "Rule System",               None),
    ("scheduling",            "Scheduling and Execution",  None),
    ("distributed-execution", "Distributed Execution",     None),
    ("program-lifecycle",     "Program Lifecycle",         None),
    ("fvm",                   "Standard Modules",          "fvm/index"),
    ("source-language",       "Loci Source Language",      None),
    ("runtime",               "Runtime Specification",     "runtime/index"),
]


def collect_pages(src_dir: Path) -> dict[str, Path]:
    """Return {stem: rel_path} for every .md file under src_dir.

    stem example: 'principles/static-schedule'
    rel_path example: PosixPath('principles/static-schedule.md')
    """
    pages = {}
    for p in sorted(src_dir.rglob("*.md")):
        rel = p.relative_to(src_dir)
        pages[str(rel.with_suffix(""))] = rel
    return pages


def resolve_wikilinks(content: str, source_rel: Path, pages: dict) -> str:
    """Replace [[target|text]] with [text](relative/path.md)."""
    source_dir = source_rel.parent

    def replace(m: re.Match) -> str:
        target = m.group(1).strip()
        text = (m.group(2) or target.split("/")[-1]).strip()
        target_path = Path(target + ".md")
        rel = Path(os.path.relpath(target_path, source_dir))
        rel_str = rel.as_posix()
        if not rel_str.startswith("."):
            rel_str = "./" + rel_str
        return f"[{text}]({rel_str})"

    return WIKILINK_RE.sub(replace, content)


def group_pages(pages: dict) -> dict[str, list[str]]:
    """Return {section_dir: [stem, ...]} — section index pages excluded."""
    section_dirs = {s[0] for s in SECTIONS}
    groups: dict[str, list[str]] = {s[0]: [] for s in SECTIONS}

    for stem in sorted(pages):
        parts = stem.split("/")
        if len(parts) < 2:
            continue
        section = parts[0]
        if section in section_dirs:
            # Exclude the section's own index
            if not (len(parts) == 2 and parts[1] == "index"):
                groups[section].append(stem)

    return groups


def build_root_toctree(groups: dict) -> str:
    """Return a single hidden toctree for index.md listing one entry per section."""
    entries = []
    for section_dir, _caption, existing_index in SECTIONS:
        if not groups[section_dir] and existing_index is None:
            continue  # skip empty sections with no index
        index_stem = existing_index if existing_index else f"{section_dir}/index"
        entries.append(index_stem)

    if not entries:
        return ""

    return (
        "\n\n<!-- Sphinx navigation — hidden from page display -->\n"
        "\n```{toctree}\n"
        ":hidden:\n"
        ":maxdepth: 2\n\n"
        + "\n".join(entries)
        + "\n```\n"
    )


def build_section_toctree(section_dir: str, page_stems: list[str],
                           hidden: bool = True) -> str:
    """Return a toctree block for a section index page.

    Entries are relative to the section directory (e.g. 'entity', not
    'core-data-model/entity') so that Sphinx resolves them correctly from
    within the section subdirectory.
    """
    rel_entries = []
    for stem in page_stems:
        parts = stem.split("/", 1)
        if len(parts) == 2 and parts[0] == section_dir:
            rel_entries.append(parts[1])

    if not rel_entries:
        return ""

    hidden_line = ":hidden:\n" if hidden else ""
    return (
        "\n\n```{toctree}\n"
        + hidden_line
        + ":maxdepth: 1\n\n"
        + "\n".join(rel_entries)
        + "\n```\n"
    )


def build_generated_index(caption: str, section_dir: str,
                           page_stems: list[str]) -> str:
    """Build a minimal section index page for sections without a source index."""
    return (
        f"---\ntitle: {caption}\n---\n\n"
        f"# {caption}\n"
        + build_section_toctree(section_dir, page_stems, hidden=False)
    )


def process(src_dir_arg: str, dst_dir_arg: str) -> None:
    src_dir = Path(src_dir_arg).resolve()
    dst_dir = Path(dst_dir_arg).resolve()

    if dst_dir.exists():
        shutil.rmtree(dst_dir)
    dst_dir.mkdir(parents=True)

    # Copy Sphinx config, extension modules, and any static assets verbatim.
    for name in ("conf.py", "_static", "_ext"):
        src = src_dir / name
        if not src.exists():
            continue
        dst = dst_dir / name
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    pages = collect_pages(src_dir)
    groups = group_pages(pages)
    root_toc = build_root_toctree(groups)

    # Map existing-index-stem → section_dir for quick lookup during processing.
    existing_index_map = {
        existing: section_dir
        for section_dir, _caption, existing in SECTIONS
        if existing is not None
    }

    for stem, rel in pages.items():
        src_file = src_dir / rel
        dst_file = dst_dir / rel
        dst_file.parent.mkdir(parents=True, exist_ok=True)

        content = src_file.read_text(encoding="utf-8")
        content = resolve_wikilinks(content, rel, pages)

        # Append root toctree to the top-level index.
        if str(rel) == "index.md":
            content += root_toc

        # Append hidden sub-toctree to existing section index pages.
        if stem in existing_index_map:
            section_dir = existing_index_map[stem]
            content += build_section_toctree(
                section_dir, groups[section_dir], hidden=True
            )

        dst_file.write_text(content, encoding="utf-8")
        print(f"  {rel}")

    # Generate section index pages for sections that don't have a source index.
    for section_dir, caption, existing_index in SECTIONS:
        if existing_index is None and groups[section_dir]:
            idx_file = dst_dir / section_dir / "index.md"
            idx_file.parent.mkdir(parents=True, exist_ok=True)
            idx_file.write_text(
                build_generated_index(caption, section_dir, groups[section_dir]),
                encoding="utf-8",
            )
            print(f"  [generated] {section_dir}/index.md")

    print(f"\nPreprocessed {len(pages)} pages → {dst_dir}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <wiki_src_dir> <output_dir>")
        sys.exit(1)
    process(sys.argv[1], sys.argv[2])
