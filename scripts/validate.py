"""Validate data/entries/*.yml against data/schema.json and the list rules.

Usage: python3 scripts/validate.py
"""
import json
import re
import sys

from jsonschema import Draft202012Validator

from listdata import DATA, load_categories, load_entries

# Open licenses that do not need proprietary: true. Add to this list in the
# same PR as the first entry that uses a new one.
OPEN_LICENSES = {
    "AGPL-3.0", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "CC-BY-4.0",
    "CC-BY-SA-4.0", "CC0-1.0", "GPL-2.0", "GPL-3.0", "ISC", "LGPL-3.0",
    "MIT", "MPL-2.0", "ODC-By-1.0", "Unlicense",
}
# Marketing words that do not belong in a factual description.
HYPE = re.compile(r"\b(best|leading|revolutionary|blazing|world-class|cutting-edge)\b", re.I)


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def check(entries, categories):
    """Return a list of 'file: message' errors."""
    validator = Draft202012Validator(json.loads((DATA / "schema.json").read_text()))
    category_ids = {c["id"] for c in categories}
    errors = []
    seen_names, seen_urls = {}, {}
    for entry in entries:
        path = entry["_path"]
        data = {k: v for k, v in entry.items() if k != "_path"}
        where = path.name
        for err in validator.iter_errors(data):
            field = ".".join(str(p) for p in err.absolute_path) or "entry"
            errors.append(f"{where}: {field}: {err.message}")
        if not isinstance(data.get("name"), str) or not isinstance(data.get("url"), str):
            continue
        if isinstance(data.get("description"), str) and HYPE.search(data["description"]):
            errors.append(f"{where}: description: marketing language ({HYPE.search(data['description']).group(0)!r})")
        if path.stem != slugify(data["name"]):
            errors.append(f"{where}: file name should be {slugify(data['name'])}.yml")
        if data.get("category") not in category_ids:
            errors.append(f"{where}: unknown category {data.get('category')!r}")
        license_id = data.get("license")
        if license_id and license_id not in OPEN_LICENSES and not data.get("proprietary"):
            errors.append(
                f"{where}: license {license_id!r} is not in the open-license list; "
                "set proprietary: true or add it to OPEN_LICENSES in scripts/validate.py"
            )
        if data.get("proprietary") and license_id in OPEN_LICENSES:
            errors.append(f"{where}: proprietary: true conflicts with open license {license_id}")
        key = data["url"].rstrip("/").lower()
        for seen, value, label in ((seen_names, data["name"].lower(), "name"), (seen_urls, key, "URL")):
            if value in seen:
                errors.append(f"{where}: duplicate {label}, also in {seen[value]}")
            seen[value] = where
    return errors


def main():
    entries = load_entries()
    errors = check(entries, load_categories())
    for err in errors:
        print(err, file=sys.stderr)
    if errors:
        print(f"{len(errors)} problem(s) in {len(entries)} entries.", file=sys.stderr)
        return 1
    print(f"{len(entries)} entries valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
