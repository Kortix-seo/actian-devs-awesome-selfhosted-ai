"""Shared loaders for the list data in data/."""
import datetime
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
ENTRIES = DATA / "entries"
GITHUB_REPO = re.compile(r"^https://github\.com/([^/]+)/([^/#?]+)/?$")


def _load(path):
    """Load YAML, turning dates into ISO strings so they validate as strings."""
    def fix(value):
        if isinstance(value, (datetime.date, datetime.datetime)):
            return value.isoformat()
        if isinstance(value, dict):
            return {k: fix(v) for k, v in value.items()}
        if isinstance(value, list):
            return [fix(v) for v in value]
        return value
    return fix(yaml.safe_load(path.read_text()))


def load_categories():
    return _load(DATA / "categories.yml")


def entry_paths():
    """Entry files, skipping templates such as _template.yml."""
    return sorted(p for p in ENTRIES.glob("*.yml") if not p.name.startswith("_"))


def load_entries():
    entries = []
    for path in entry_paths():
        entry = _load(path)
        entry["_path"] = path
        entries.append(entry)
    return entries


def sort_key(entry):
    return entry["name"].lower()


def github_repo(url):
    """Return (owner, repo) for a GitHub repository URL, else None."""
    m = GITHUB_REPO.match(url)
    return (m.group(1), m.group(2)) if m else None


def dump_yaml(obj):
    return yaml.safe_dump(obj, sort_keys=False, allow_unicode=True, width=1000)
