"""Adds the release notes pages to the menu, newest first.

The release notes tool writes one page per version in docs/notas-de-version (version-<major>-<minor>.md),
and the nav of mkdocs.yml is written by hand, so without this every new version would need a line there.
"""
import re
from pathlib import Path

FOLDER = "notas-de-version"
SECTION = "Notas de versión"
PAGE = re.compile(r"^version-(\d+)-(\d+)(?:\.[a-z]{2})?\.md$")


def on_config(config):
    folder = Path(config["docs_dir"]) / FOLDER
    if not folder.is_dir() or config["nav"] is None:
        return config
    versions = {}
    for file in folder.iterdir():
        match = PAGE.match(file.name)
        if match:
            # page.md and page.es.md are the same page for the i18n plugin: list it once, by its name without language
            versions[(int(match[1]), int(match[2]))] = f"{FOLDER}/version-{match[1]}-{match[2]}.md"
    if not versions:
        return config
    pages = [versions[key] for key in sorted(versions, reverse=True)]
    nav = [entry for entry in config["nav"] if not (isinstance(entry, dict) and SECTION in entry)]
    nav.append({SECTION: pages})
    config["nav"] = nav
    return config
