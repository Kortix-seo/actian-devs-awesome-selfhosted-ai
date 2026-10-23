"""Add a monthly section to CHANGELOG.md from data/history snapshots.

Compares the latest snapshot with the one closest to four weeks earlier and
lists entries added, removed, and moved, plus the biggest star gains.

Usage: python3 scripts/changelog.py [--top N]
"""
import argparse
import datetime
import json
import sys

from listdata import DATA, ROOT

MIN_GAP_DAYS = 21  # need roughly a month between snapshots to compare


def load_snapshots():
    snaps = []
    for path in sorted((DATA / "history").glob("*.json")):
        snap = json.loads(path.read_text())
        snap["_taken"] = datetime.datetime.fromisoformat(snap["taken_at"])
        snaps.append(snap)
    return snaps


def pick_pair(snaps):
    """Latest snapshot and the one closest to 28 days before it."""
    if len(snaps) < 2:
        return None
    latest = snaps[-1]
    older = [s for s in snaps[:-1] if (latest["_taken"] - s["_taken"]).days >= MIN_GAP_DAYS]
    if not older:
        return None
    target = latest["_taken"] - datetime.timedelta(days=28)
    return min(older, key=lambda s: abs((s["_taken"] - target).days)), latest


def stars(entry):
    return (entry.get("github") or {}).get("stars")


def section(old, new, top):
    a, b = old["entries"], new["entries"]
    month = new["_taken"].strftime("%B %Y")
    lines = [f"## {month}", "", f"Compared with the snapshot from {old['_taken'].date()}.", ""]

    added = sorted(set(b) - set(a))
    removed = sorted(set(a) - set(b))
    moved = sorted(s for s in set(a) & set(b) if a[s]["url"] != b[s]["url"])
    if added:
        lines += ["### Added", ""] + [f"- [{b[s]['name']}]({b[s]['url']})" for s in added] + [""]
    if removed:
        lines += ["### Removed", ""] + [f"- {a[s]['name']}" for s in removed] + [""]
    if moved:
        lines += ["### Moved", ""] + [f"- {b[s]['name']}: {a[s]['url']} → {b[s]['url']}" for s in moved] + [""]

    gains = [
        (stars(b[s]) - stars(a[s]), s)
        for s in set(a) & set(b)
        if stars(a[s]) is not None and stars(b[s]) is not None
    ]
    gains = [g for g in sorted(gains, reverse=True) if g[0] > 0][:top]
    if gains:
        lines += ["### Most new GitHub stars", ""]
        lines += [f"- [{b[s]['name']}]({b[s]['url']}) +{gain:,}" for gain, s in gains] + [""]
    if not (added or removed or moved or gains):
        lines += ["No changes.", ""]
    return month, "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--top", type=int, default=10)
    args = parser.parse_args()

    pair = pick_pair(load_snapshots())
    if pair is None:
        print(f"Not enough history yet (need two snapshots {MIN_GAP_DAYS}+ days apart).")
        return 0
    month, body = section(*pair, args.top)

    path = ROOT / "CHANGELOG.md"
    intro = "# Changelog\n\nMonthly changes to the list, generated from `data/history/` by `scripts/changelog.py`.\n"
    text = path.read_text() if path.exists() else intro
    if f"\n## {month}\n" in text:
        print(f"CHANGELOG.md already has {month}.")
        return 0
    head, sep, rest = text.partition("\n## ")
    path.write_text(head.rstrip("\n") + "\n\n" + body + ("\n## " + rest if sep else ""))
    print(f"Added {month} to CHANGELOG.md.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
