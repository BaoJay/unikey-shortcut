from pathlib import Path
import unicodedata
import sys

# ============================================================
# Configuration
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

SOURCE_FILE = ROOT_DIR / "unikey-shortcut.txt"
OUTPUT_FILE = ROOT_DIR / "evkey-shortcut.txt"

UNIKEY_HEADER_PREFIX = ";DO NOT DELETE"
EVKEY_HEADER = "Không được xoá dòng này<<<version=3>>>"


# ============================================================
# Build
# ============================================================


def parse_line(raw_line):
    """Convert one UniKey line to EVKey format.

    Returns None for lines to ignore, raises ValueError for invalid lines.
    """
    line = unicodedata.normalize("NFC", raw_line.strip())

    # Ignore empty lines, UniKey header and comments
    if not line or line.startswith((UNIKEY_HEADER_PREFIX, "#")):
        return None

    # Invalid shortcut line
    if ":" not in line:
        raise ValueError(f"missing ':' separator → {line}")

    shortcut, replacement = line.split(":", 1)

    shortcut = shortcut.strip()
    replacement = replacement.strip()

    if not shortcut:
        raise ValueError("shortcut is empty")

    if not replacement:
        raise ValueError(f"replacement is empty → {shortcut}")

    return f"{shortcut}||{replacement}"


def build_evkey():
    if not SOURCE_FILE.exists():
        print(f"❌ Source file not found: {SOURCE_FILE}")
        sys.exit(1)

    try:
        text = SOURCE_FILE.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        print("❌ Source file is not valid UTF-8.")
        sys.exit(1)

    output_lines = [EVKEY_HEADER]

    shortcut_count = 0
    skipped_count = 0

    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        try:
            entry = parse_line(raw_line)
        except ValueError as error:
            print(f"⚠️  Skipped line {line_number}: {error}")
            skipped_count += 1
            continue

        if entry is None:
            continue

        output_lines.append(entry)
        shortcut_count += 1

    output_text = "\n".join(output_lines) + "\n"

    OUTPUT_FILE.write_text(
        output_text,
        encoding="utf-8",
        newline="\n",
    )

    print()
    print("✅ EVKey shortcut file generated successfully")
    print(f"📄 Source : {SOURCE_FILE.name}")
    print(f"📄 Output : {OUTPUT_FILE.name}")
    print(f"🔤 Shortcuts: {shortcut_count}")

    if skipped_count:
        print(f"⚠️  Skipped: {skipped_count}")

    print()


if __name__ == "__main__":
    build_evkey()
