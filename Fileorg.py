import os
import shutil
import sys
from pathlib import Path
CATEGORIES = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".ico", ".tiff"],
    "Videos":     [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".m4v"],
    "Audio":      [".mp3", ".wav", ".aac", ".flac", ".ogg", ".m4a", ".wma"],
    "Documents":  [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md", ".csv", ".odt"],
    "Archives":   [".zip", ".tar", ".gz", ".rar", ".7z", ".bz2"],
    "Code":       [".py", ".js", ".ts", ".html", ".css", ".java", ".cpp", ".c", ".h", ".json", ".xml", ".yaml", ".yml", ".sh", ".sql"],
    "Executables":[".exe", ".msi", ".dmg", ".pkg", ".deb", ".rpm", ".app"],
    "Fonts":      [".ttf", ".otf", ".woff", ".woff2"],
}
def get_category(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Misc"
def organize(target_dir: str, dry_run: bool = False) -> dict:
    target = Path(target_dir).resolve()
    if not target.is_dir():
        print(f" Error: '{target}' is not a valid directory.")
        sys.exit(1)
    summary = {}
    skipped = []
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Organizing: {target}\n")
    for item in sorted(target.iterdir()):
        if item.is_dir():
            continue
        if item.name == Path(__file__).name:
            continue
        category = get_category(item.suffix)
        dest_folder = target / category
        dest_file = dest_folder / item.name
        counter = 1
        while dest_file.exists():
            stem = item.stem
            dest_file = dest_folder / f"{stem}_{counter}{item.suffix}"
            counter += 1
        action = f"{'[MOVE]' if not dry_run else '[WOULD MOVE]'} {item.name}  →  {category}/"
        if dest_file.name != item.name:
            action += f"(renamed to {dest_file.name})"
        print(action)
        if not dry_run:
            dest_folder.mkdir(exist_ok=True)
            shutil.move(str(item), str(dest_file))
        summary.setdefault(category, []).append(item.name)
    return summary
def print_summary(summary: dict) -> None:
    total = sum(len(v) for v in summary.values())
    print(f"\n{'─'*40}")
    print(f"Summary: {total} file(s) organized\n")
    for category, files in sorted(summary.items()):
        print(f" {category:<14} {len(files):>3} file(s)")
    print(f"{'─'*40}\n")
def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    dirs = [a for a in args if not a.startswith("--")]
    target_dir = dirs[0] if dirs else "."
    summary = organize(target_dir, dry_run=dry_run)
    if summary:
        print_summary(summary)
        if dry_run:
            print("Dry run complete. No files were moved.\n")
        else:
            print("Done!\n")
    else:
        print("\n  Nothing to organize — no files found.\n")
if __name__ == "__main__":
    main()