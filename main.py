"""Two Days of Quiet Dread — a one-line code review comment.

The program writes a single approving review comment, carrying quiet
existential dread, to /output/entry.txt, then reads the file back and
checks that what landed is exactly the line it meant to write, byte
for byte.
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
    bad = sorted({ord(ch) for ch in text if ord(ch) < 0x20 or ord(ch) == 0x7F})
    if bad:
        faults.append(
            "control characters: " + ", ".join(f"U+{code:04X}" for code in bad)
        )
    return faults


def fail_if_bad(text, where):
    """Abort with a readable message when `text` breaks the gate."""
    faults = check(text)
    if faults:
        raise SystemExit(f"{where} fails the gate: " + "; ".join(faults))


def main():
    fail_if_bad(COMMENT, "comment")

    payload = COMMENT + "\n"
    encoded = payload.encode("utf-8")
    if encoded.decode("utf-8") != payload:
        raise SystemExit("comment does not survive a UTF-8 round-trip")

    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_bytes(encoded)

    raw = DESTINATION.read_bytes()
    if raw != encoded:
        raise SystemExit("round-trip mismatch: file bytes differ from the comment")
    stored = raw.decode("utf-8")
    if not stored.endswith("\n"):
        raise SystemExit("written file lost its trailing newline")
    fail_if_bad(stored[:-1], "written file")

    print(
        f"wrote {len(COMMENT)} characters "
        f"({len(encoded) - 1} bytes of text) to {DESTINATION}"
    )


if __name__ == "__main__":
    main()
