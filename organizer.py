"""Sort the files of a folder into sub-folders by type.

By default it only shows what it would do (dry run). Use --apply to move the files.

    python organizer.py ~/Downloads
    python organizer.py ~/Downloads --apply
"""
import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".odt", ".rtf"},
    "spreadsheets": {".xls", ".xlsx", ".csv", ".ods"},
    "presentations": {".ppt", ".pptx", ".odp"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "installers": {".exe", ".msi", ".dmg", ".deb", ".iso"},
    "code": {".py", ".js", ".html", ".css", ".java", ".json", ".sql"},
}


def category_for(path: Path) -> str:
    suffix = path.suffix.lower()
    for name, extensions in CATEGORIES.items():
        if suffix in extensions:
            return name
    return "other"


def free_name(target: Path) -> Path:
    """Return a path that does not exist yet: report.pdf -> report (1).pdf."""
    if not target.exists():
        return target
    counter = 1
    while True:
        candidate = target.with_name(f"{target.stem} ({counter}){target.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def plan(folder: Path):
    """List (source, destination) pairs for the files directly inside `folder`."""
    moves = []
    for item in sorted(folder.iterdir()):
        if not item.is_file() or item.name.startswith("."):
            continue
        destination = folder / category_for(item) / item.name
        moves.append((item, destination))
    return moves


def organize(folder: Path, apply: bool = False):
    moves = plan(folder)
    done = []
    for source, destination in moves:
        final = free_name(destination)
        if apply:
            final.parent.mkdir(exist_ok=True)
            shutil.move(str(source), str(final))
        done.append((source, final))
    return done


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("folder", type=Path)
    parser.add_argument("--apply", action="store_true", help="really move the files")
    args = parser.parse_args()

    if not args.folder.is_dir():
        parser.error(f"{args.folder} is not a folder")

    results = organize(args.folder, apply=args.apply)
    verb = "Moved" if args.apply else "Would move"
    for source, final in results:
        print(f"{verb}: {source.name} -> {final.relative_to(args.folder)}")
    print(f"{len(results)} file(s) {'moved' if args.apply else 'found (dry run, nothing was changed)'}")


if __name__ == "__main__":
    main()
