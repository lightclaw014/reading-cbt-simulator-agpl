#!/usr/bin/env python3
"""Build simulator.html — index.html with every test in library/tests baked in.

The app is one offline file, so a page opened from disk cannot read a folder
by itself. This script writes the tests INTO a copy of the app instead: each
test's raw Markdown goes into the existing <script id="baked-config"> block
(as its "library" field), and the app parses it with its own parser when the
teacher opens it. Nothing here needs to understand the test format.

    python tools/build_library.py            # library/tests -> simulator.html
    python tools/build_library.py --out X    # write somewhere else

Chrome and Edge can read the library folder live (the app's "Connect your
library folder" button), which needs no build step. This is for the browsers
that cannot: Firefox, Safari and phones.

index.html is never modified. Exporting a test for students rewrites that same
block, so a student's file never carries the library.
"""

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BLOCK_RE = re.compile(
    r'<script type="application/json" id="baked-config">[\s\S]*?</script>'
)
BIG_FILE_MB = 3.0  # warn past this: usually a test with an embedded image


def collect(tests_dir):
    """Every .md under tests/, sorted, as {file, md} entries."""
    entries, problems = [], []
    for path in sorted(tests_dir.rglob("*.md"), key=lambda p: str(p).lower()):
        rel = path.relative_to(tests_dir).as_posix()
        # utf-8-sig: Windows editors (Notepad, PowerShell) start a file with a
        # byte-order mark, which would otherwise sit before "# Test:" and make
        # a good test look like a stray file.
        text = path.read_text(encoding="utf-8-sig")
        if not re.search(r"^#\s*Test:", text, re.MULTILINE):
            problems.append(rel)
            continue
        entries.append({"file": rel, "md": text})
    return entries, problems


def build(entries, src_html):
    payload = {"standalone": False, "test": None, "attempt": None, "library": entries}
    # "</script" inside a test would end the block early; "<\/script" is a legal
    # JSON escape for the same text, so the app reads it back unchanged.
    block = json.dumps(payload, ensure_ascii=False).replace("</script", "<\\/script")
    if not BLOCK_RE.search(src_html):
        sys.exit("Could not find the baked-config block in index.html — has it been edited by hand?")
    return BLOCK_RE.sub(
        lambda m: '<script type="application/json" id="baked-config">' + block + "</script>",
        src_html,
        count=1,
    )


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tests", default=str(ROOT / "library" / "tests"), help="folder of .md tests (default: library/tests)")
    ap.add_argument("--out", default=str(ROOT / "simulator.html"), help="file to write (default: simulator.html)")
    args = ap.parse_args()

    tests_dir = pathlib.Path(args.tests)
    if not tests_dir.is_dir():
        sys.exit("No folder at " + str(tests_dir) + " — create library/tests and put your .md tests inside.")

    entries, problems = collect(tests_dir)
    out_html = build(entries, (ROOT / "index.html").read_text(encoding="utf-8"))
    out_path = pathlib.Path(args.out)
    out_path.write_text(out_html, encoding="utf-8")

    for rel in problems:
        print("  skipped " + rel + " — no '# Test:' line, so it isn't a test file")
    for e in entries:
        print("  added   " + e["file"] + " (" + f"{len(e['md']) / 1024:.1f}" + " KB)")
    size_mb = out_path.stat().st_size / 1024 / 1024
    print(
        "\n" + str(len(entries)) + " test(s) -> " + out_path.name +
        " (" + f"{size_mb:.1f}" + " MB). Open that file to use your library."
    )
    if size_mb > BIG_FILE_MB:
        print("Note: that is large for one file. A test with an embedded image is the usual cause.")


if __name__ == "__main__":
    main()
