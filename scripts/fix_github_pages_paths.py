from pathlib import Path
import re
from collections import Counter

root = Path("public")
prefix = "/client-seabreeze"

if not root.is_dir():
    raise SystemExit("ERROR: public/ missing")

# Match root-relative URLs for known site paths.
# Exclude external URLs and already-prefixed paths.
pattern = re.compile(
    r'(?<![A-Za-z0-9_./-])/'
    r'(img|icons|css|en|ru|ar|hi|'
    r'projects|search)(?=/)'
)

counts = Counter()

for path in root.rglob("*"):
    if not path.is_file():
        continue

    if path.suffix.lower() not in {
        ".html", ".css", ".js", ".json", ".xml"
    }:
        continue

    text = path.read_text(
        encoding="utf-8", errors="replace"
    )

    def fix(match):
        counts[match.group(1)] += 1
        return prefix + match.group(0)

    updated = pattern.sub(fix, text)

    # Fix explicit links to the site root.
    updated = re.sub(
        r'(href=["\'])/(\1)',
        lambda m: m.group(1) + prefix + "/" + m.group(2),
        updated
    )

    if updated != text:
        path.write_text(updated, encoding="utf-8")

print("=== GITHUB PAGES PATH REWRITE ===")
for key, value in sorted(counts.items()):
    print(f"{key}: {value}")

print("TOTAL:", sum(counts.values()))

if sum(counts.values()) == 0:
    print("WARNING: No paths rewritten; inspect generated URLs")
