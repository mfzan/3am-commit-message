"""Write the 3AM commit message entry to /output/entry.txt.

The entry is one line: a git commit message typed by an AI coding
agent at 3am after a long night of fixing its own bugs. The joke is
the revert spiral -- the agent's "fix" is reverting its previous
3am fix, then it catches itself editing the revert, so it ends up
reverting its own revert. The fixer becomes the thing being undone.

Gate (from the kit's RULES.txt): the file must hold UTF-8 text of
1 to 139 characters, one line, and nothing else. This program fails
loudly instead of writing an out-of-gate entry.
"""

import os
import sys

# The single entry line. Kept ASCII so it reads like a real commit.
ENTRY = (
    "revert 'fix: stop the agent editing its own code at 3am' "
    "- it edited the revert, so I am reverting my own revert"
)

MIN_CHARS = 1
MAX_CHARS = 139


def fail(message):
    print("entry rejected: " + message, file=sys.stderr)
    sys.exit(1)


def main():
    # Files this program creates must be world-readable (0644).
    os.umask(0o022)

    line = ENTRY

    if "\n" in line or "\r" in line:
        fail("entry must be a single line")
    if not line.strip():
        fail("entry must not be only whitespace")
    # The scorer measures the file, which also carries the trailing
    # newline, so the line plus that newline must fit the gate.
    if not (MIN_CHARS <= len(line) + 1 <= MAX_CHARS):
        fail(
            "entry file would be %d characters, outside the gate of "
            "%d to %d" % (len(line) + 1, MIN_CHARS, MAX_CHARS)
        )

    out_dir = os.environ.get("OUTPUT_DIR") or "/output"
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir, mode=0o755, exist_ok=True)

    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(line + "\n")

    # The grader collects the output as another user: the file itself
    # must be world-readable. Never chmod the /output directory itself
    # -- it is root-owned and merely writable, so chmod on it fails.
    os.chmod(path, 0o644)

    print("wrote %s (%d characters)" % (path, len(line)))


if __name__ == "__main__":
    main()
