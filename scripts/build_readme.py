"""Generate README.md from data/.

Usage:
  python3 scripts/build_readme.py          # write README.md
  python3 scripts/build_readme.py --check  # exit 1 if README.md is out of date
"""
import re
import sys

from listdata import DATA, ROOT, load_categories, load_entries, sort_key


def anchor(title):
    """GitHub heading anchor: lowercase, drop punctuation, spaces to hyphens."""
    return re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


def render_entry(entry):
    desc = entry["description"]
    if entry.get("proprietary"):
        desc = desc[:-1] + " (`⊘ Proprietary`)."
    return f"- [{entry['name']}]({entry['url']}) - {desc}"


def render():
    categories = load_categories()
    entries = load_entries()
    header = (DATA / "readme" / "header.md").read_text()
    footer = (DATA / "readme" / "footer.md").read_text()

    parts = [header, "## Contents\n"]
    parts.append("\n".join(f"- [{c['title']}](#{anchor(c['title'])})" for c in categories) + "\n")
    for cat in categories:
        items = sorted((e for e in entries if e["category"] == cat["id"]), key=sort_key)
        section = f"## {cat['title']}\n"
        if cat.get("intro"):
            section += f"\n{cat['intro']}\n"
        section += "\n" + "\n".join(render_entry(e) for e in items) + "\n"
        parts.append(section)
    parts.append(footer)
    return "\n".join(parts)


def main():
    readme = ROOT / "README.md"
    output = render()
    if "--check" in sys.argv:
        if readme.read_text() != output:
            print("README.md is out of date. Run: python3 scripts/build_readme.py", file=sys.stderr)
            return 1
        print("README.md is up to date.")
        return 0
    readme.write_text(output)
    print("Wrote README.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
