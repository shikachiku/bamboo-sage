from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TARGET_DIRS = [
    ROOT / "indicators",
]

HEADER = "from settings import DATA_PATH\n"

OLD = 'BASE = "data"'
NEW = "BASE = DATA_PATH"

count = 0

for folder in TARGET_DIRS:

    for py in folder.glob("*.py"):

        text = py.read_text(encoding="utf-8")

        changed = False

        if HEADER.strip() not in text:

            lines = text.splitlines()

            insert_at = 0

            for i, line in enumerate(lines):

                if line.startswith("import ") or line.startswith("from "):
                    insert_at = i + 1

            lines.insert(insert_at, HEADER.rstrip())

            text = "\n".join(lines)

            changed = True

        if OLD in text:

            text = text.replace(OLD, NEW)

            changed = True

        if changed:

            py.write_text(text, encoding="utf-8")

            print(f"Updated -> {py.name}")

            count += 1

print()
print("===========================")
print(f"Updated Files : {count}")
print("===========================")