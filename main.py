import json
import time
import os
import shutil
import setup
import argparse
import re


SECONDS_IN_7_DAYS = 7 * 24 * 60 * 60

FILE_TYPES = {
    "Images": {"jpg", "jpeg", "png", "gif", "bmp", "webp", "svg"},
    "Videos": {"mp4", "mkv", "avi", "mov", "wmv", "webm"},
    "Audio": {"mp3", "wav", "flac", "aac", "ogg"},
    "Documents": {"pdf", "doc", "docx", "txt", "ppt", "pptx", "xls", "xlsx", "vtt"},
    "Applications": {"exe", "msi", "dmg", "apk"},
    "Code": {
        "py", "js", "java", "cpp", "c", "cs", "go", "rs",
        "html", "css", "json", "xml", "yaml", "yml", "md"
    },
    "Archives": {"zip", "rar", "7z", "tar", "gz"},
}

MANAGED_DIRS = {"recent"} | set(FILE_TYPES.keys()) | {"Other"}

EXCLUDED_FILES = {
    "details.json",
    os.path.basename(__file__),
}


def get_extension(filename):
    return os.path.splitext(filename)[1][1:].lower()

def get_category(ext):
    for category, extensions in FILE_TYPES.items():
        if ext in extensions:
            return category
    return "Other"

def collect_files(base_dir):
    """Collect files from root and managed folders (non-recursive)."""
    files = []

    # root files
    for name in os.listdir(base_dir):
        path = os.path.join(base_dir, name)
        if os.path.isfile(path):
            files.append(path)

    # managed directories
    for folder in MANAGED_DIRS:
        folder_path = os.path.join(base_dir, folder)
        if os.path.isdir(folder_path):
            for name in os.listdir(folder_path):
                path = os.path.join(folder_path, name)
                if os.path.isfile(path):
                    files.append(path)

    return files


def resolve_collision(target_path):
    """
    Handles collisions smartly:
    - If file exists, increment the number in parentheses.
    - If no number, start with (1).
    - Never stack numbers.
    """
    if not os.path.exists(target_path):
        return target_path

    directory, filename = os.path.split(target_path)
    name, ext = os.path.splitext(filename)

    # Check for existing (number) at the end
    match = re.search(r'\((\d+)\)$', name)
    if match:
        base_name = name[:match.start()].rstrip()  # remove the (n)
        number = int(match.group(1)) + 1
    else:
        base_name = name
        number = 1

    while True:
        new_name = f"{base_name} ({number}){ext}"
        new_path = os.path.join(directory, new_name)
        if not os.path.exists(new_path):
            return new_path
        number += 1

def organize_files(sort_dir, dry_run=False):
    recent_dir = os.path.join(sort_dir, "recent")
    if not dry_run:
        os.makedirs(recent_dir, exist_ok=True)

    files = collect_files(sort_dir)

    for file_path in files:
        filename = os.path.basename(file_path)

        if filename in EXCLUDED_FILES:
            continue

        try:
            mod_time = os.path.getmtime(file_path)
            is_recent = (time.time() - mod_time) < SECONDS_IN_7_DAYS

            if is_recent:
                target_path = os.path.join(recent_dir, filename)
            else:
                ext = get_extension(filename)
                category = get_category(ext)
                target_dir = os.path.join(sort_dir, category)
                if not dry_run:
                    os.makedirs(target_dir, exist_ok=True)
                target_path = os.path.join(target_dir, filename)

            # Determine final target only if a real collision exists
            if os.path.exists(target_path) and os.path.abspath(file_path) != os.path.abspath(target_path):
                final_target = resolve_collision(target_path)
            else:
                final_target = target_path


            if os.path.abspath(file_path) != os.path.abspath(final_target):
                if dry_run:
                    print(
                        f"[DRY-RUN] WOULD MOVE: {filename} → "
                        f"{os.path.relpath(final_target, sort_dir)}"
                    )
                else:
                    shutil.move(file_path, final_target)
                    print(
                        f"MOVED: {filename} → "
                        f"{os.path.relpath(final_target, sort_dir)}"
                    )


        except Exception as e:
            print(f"ERROR: {filename} → {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="File Organizer")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be moved without actually moving files"
    )
    args = parser.parse_args()

    setup.ensure_config()

    with open("details.json", "r") as f:
        config = json.load(f)

    print(f"\nOrganizing files in: {config['path']}")
    if args.dry_run:
        print("DRY RUN MODE — no files will be moved\n")
    else:
        print("LIVE MODE — files will be moved\n")

    organize_files(config["path"], dry_run=args.dry_run)

    print("\nOrganization Complete!\n")
