from pathlib import Path
import unicodedata
import sys

# ============================================================
# Configuration
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

SOURCE_FILE = ROOT_DIR / "shortcuts.txt"
UNIKEY_FILE = ROOT_DIR / "unikey-shortcut.txt"
EVKEY_FILE = ROOT_DIR / "evkey-shortcut.txt"

UNIKEY_HEADER = ";DO NOT DELETE THIS LINE*** version=1 ***"
EVKEY_HEADER = "Không được xoá dòng này<<<version=3>>>"


# ============================================================
# Parse
# ============================================================


def parse_line(raw_line):
    """Parse one `shortcut:replacement` line.

    Returns None for lines to ignore, raises ValueError for invalid lines.
    """
    line = unicodedata.normalize("NFC", raw_line.strip().lstrip("﻿"))

    # Ignore empty lines and comments
    if not line or line.startswith("#"):
        return None

    if ":" not in line:
        raise ValueError(f"missing ':' separator → {line}")

    shortcut, replacement = line.split(":", 1)

    shortcut = shortcut.strip()
    replacement = replacement.strip()

    if not shortcut:
        raise ValueError("shortcut is empty")

    if not replacement:
        raise ValueError(f"replacement is empty → {shortcut}")

    return shortcut, replacement


def load_entries():
    if not SOURCE_FILE.exists():
        print(f"❌ Source file not found: {SOURCE_FILE}")
        sys.exit(1)

    try:
        text = SOURCE_FILE.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("❌ Source file is not valid UTF-8.")
        sys.exit(1)

    entries = []
    seen = {}
    errors = []

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        try:
            entry = parse_line(raw_line)
        except ValueError as error:
            errors.append(f"line {line_number}: {error}")
            continue

        if entry is None:
            continue

        shortcut = entry[0]
        if shortcut in seen:
            errors.append(
                f"line {line_number}: duplicate shortcut '{shortcut}'"
                f" (first defined on line {seen[shortcut]})"
            )
            continue

        seen[shortcut] = line_number
        entries.append(entry)

    if errors:
        for error in errors:
            print(f"❌ {error}")
        sys.exit(1)

    return entries


# ============================================================
# Build
# ============================================================


def build():
    entries = load_entries()

    # UniKey (Windows): UTF-8 with BOM, CRLF line endings
    unikey_lines = [UNIKEY_HEADER] + [f"{s}:{r}" for s, r in entries]
    UNIKEY_FILE.write_text(
        "\r\n".join(unikey_lines),
        encoding="utf-8-sig",
        newline="",
    )

    # EVKey (macOS): UTF-8, LF line endings
    evkey_lines = [EVKEY_HEADER] + [f"{s}||{r}" for s, r in entries]
    EVKEY_FILE.write_text(
        "\n".join(evkey_lines) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    print()
    print("✅ Shortcut files generated successfully")
    print(f"📄 Source : {SOURCE_FILE.name}")
    print(f"📄 Output : {UNIKEY_FILE.name}, {EVKEY_FILE.name}")
    print(f"🔤 Shortcuts: {len(entries)}")
    print()


if __name__ == "__main__":
    build()
