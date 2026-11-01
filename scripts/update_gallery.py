"""Generate the profile gallery using only the Python standard library."""

import argparse
from html import escape
from pathlib import Path
import re
import sys
from urllib.parse import quote

START = b"<!-- GALLERY:START -->"
END = b"<!-- GALLERY:END -->"
EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
FEATURED = 2


def image_paths(root):
    assets = root / "assets"
    paths = []
    if assets.exists():
        for path in assets.rglob("*"):
            relative = path.relative_to(assets)
            if relative.parts[0].casefold() == "branding":
                continue
            if path.is_file() and not path.is_symlink() and path.suffix.lower() in EXTENSIONS:
                if any(parent.is_symlink() for parent in path.parents if parent != root):
                    continue
                paths.append(path.relative_to(root).as_posix())

    def natural_key(value):
        return tuple((0, int(p)) if p.isdigit() else (1, p.casefold())
                     for p in re.split(r"(\d+)", value))

    return sorted(paths, key=lambda value: (natural_key(value), value))


def caption(path):
    stem = Path(path).stem
    cleaned = re.sub(r"^\d+[-_\s]+", "", stem)
    cleaned = " ".join(re.sub(r"[-_]+", " ", cleaned).split())
    return cleaned or stem


def render_gallery(paths):
    if not paths:
        return ""

    def card(path):
        url = quote(path, safe="/")
        label = escape(caption(path), quote=True)
        return (f'<p align="center">\n'
                f'  <a href="{url}"><img src="{url}" alt="{label}" width="640"></a>\n'
                f'  <br>{label}\n</p>')

    parts = ["## Achievements & Moments", "A few moments from my learning journey."]
    parts.extend(card(path) for path in paths[:FEATURED])
    if len(paths) > FEATURED:
        parts.append(f"<details>\n<summary>More moments ({len(paths) - FEATURED})</summary>")
        parts.extend(card(path) for path in paths[FEATURED:])
        parts.append("</details>")
    return "\n\n".join(parts)


def update(root):
    readme = root / "README.md"
    original = readme.read_bytes()
    if original.count(START) != 1 or original.count(END) != 1:
        raise ValueError("README.md must contain exactly one GALLERY:START and one GALLERY:END marker.")
    start = original.index(START) + len(START)
    end = original.index(END)
    if start > end:
        raise ValueError("GALLERY:START must appear before GALLERY:END.")
    newline = b"\r\n" if b"\r\n" in original else b"\n"
    gallery = render_gallery(image_paths(root)).encode("utf-8").replace(b"\n", newline)
    inside = newline + (newline + gallery + newline + newline if gallery else b"")
    updated = original[:start] + inside + original[end:]
    if updated == original:
        return False
    readme.write_bytes(updated)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        changed = update(args.root.resolve())
    except (OSError, ValueError) as error:
        print(f"Gallery error: {error}", file=sys.stderr)
        return 1
    print("Gallery updated." if changed else "Gallery already up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
