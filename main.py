"""Two Days of Quiet Dread — a one-line code review comment.

The program writes a single approving review comment, carrying quiet
existential dread, to /output/entry.txt, then reads the file back and
checks that what landed is exactly the line it meant to write.
"""

from pathlib import Path

MAX_CHARS = 140
DESTINATION = Path("/output/entry.txt")

COMMENT = (
    "LGTM. I read every line twice, mostly to delay the rest of my life. "
    "The code is fine."
)


def check(text):
    """Collect every way `text` would fail the competition gate."""
    faults = []
    if len(text) == 0:
        faults.append("empty text")
    if len(text) > MAX_CHARS:
        faults.append(f"{len(text)} characters, over the {MAX_CHARS} limit")
    if text.strip() == "":
        faults.append("nothing but whitespace")
    if text != text.strip():
        faults.append("leading or trailing whitespace")
    if "\n" in text or "\r" in text:
        faults.append("more than one line")
    for ch in text:
        code = ord(ch)
        if code < 0x20 or code == 0x7F:
            faults.append(f"control character U+{code:04X}")
            break
    return faults


def main():
    faults = check(COMMENT)
    if faults:
        raise SystemExit("comment fails the gate: " + "; ".join(faults))

    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(COMMENT + "\n", encoding="utf-8")

    written = DESTINATION.read_text(encoding="utf-8")
    if written != COMMENT + "\n":
        raise SystemExit("round-trip mismatch: file differs from the comment")
    if check(written.rstrip("\n")):
        raise SystemExit("written file fails the gate on re-check")

    print(f"wrote {len(COMMENT)} characters to {DESTINATION}")


if __name__ == "__main__":
    main()
