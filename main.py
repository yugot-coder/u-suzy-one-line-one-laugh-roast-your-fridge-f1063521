"""One-line fridge roast entry for make.fun.

Writes the chosen roast to entry.txt (next to this script) and, when the
grader's /output directory exists, to /output/entry.txt as well.

Standard library only. Deterministic: the same bytes every run.
"""

import hashlib
import os
import sys

ENTRY = (
    "The magnets on my fridge hold up takeaway menus for restaurants "
    "that closed years ago \u2014 it's a museum with a light inside."
)

MAX_CHARS = 200


def validate_entry(text):
    """Check the entry against the competition gate.

    Returns a list of problems; an empty list means the entry is valid.
    """
    problems = []
    if not isinstance(text, str):
        problems.append("entry is not a string")
        return problems
    if not (1 <= len(text) <= MAX_CHARS):
        problems.append(
            "entry is %d characters, must be 1-%d" % (len(text), MAX_CHARS)
        )
    if not text.strip():
        problems.append("entry is only white space")
    if "\n" in text or "\r" in text:
        problems.append("entry must be a single line")
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("entry is not valid UTF-8 text")
    return problems


def write_entry(path):
    """Write ENTRY to path, read it back, and verify it is byte-identical."""
    data = ENTRY.encode("utf-8")
    with open(path, "wb") as f:
        f.write(data)
    with open(path, "rb") as f:
        back = f.read()
    if back != data:
        raise RuntimeError("read-back mismatch for %s" % path)
    return path


def main():
    problems = validate_entry(ENTRY)
    if problems:
        for problem in problems:
            print("INVALID: %s" % problem, file=sys.stderr)
        return 1
    here = os.path.dirname(os.path.abspath(__file__))
    write_entry(os.path.join(here, "entry.txt"))
    if os.path.isdir("/output"):
        write_entry("/output/entry.txt")
    digest = hashlib.sha256(ENTRY.encode("utf-8")).hexdigest()
    print("entry (%d chars): %s" % (len(ENTRY), ENTRY))
    print("sha256: %s" % digest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
