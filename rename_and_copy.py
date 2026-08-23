#!/usr/bin/env python3
"""
Auto-renamer for the Rakshabandhan site assets.

What it does:
  1. Walks through a folder you point it at (can have messy subfolders,
     doesn't matter).
  2. For every file in there, checks if its filename matches one of the
     original Discord filenames listed in manifest.json.
  3. If it matches, copies it into assets/ under the correct new name
     that index.html expects.
  4. Prints a report of what it found and what's still missing.

Usage:
  python3 rename_and_copy.py /path/to/folder/with/your/recovered/files

If you don't pass a folder, it'll look in the current directory.
"""

import json
import os
import shutil
import sys

def main():
    source_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    source_dir = os.path.abspath(source_dir)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    manifest_path = os.path.join(script_dir, "manifest.json")
    assets_dir = os.path.join(script_dir, "assets")

    if not os.path.exists(manifest_path):
        print(f"Could not find manifest.json next to this script ({manifest_path}).")
        sys.exit(1)

    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    os.makedirs(assets_dir, exist_ok=True)

    # Build a lookup: lowercase original filename -> manifest entry
    lookup = {item["orig"].lower(): item for item in manifest}
    matched_origs = set()

    print(f"Scanning {source_dir} ...\n")

    found_count = 0
    for root, dirs, files in os.walk(source_dir):
        # don't descend into the assets folder itself or hidden folders
        dirs[:] = [d for d in dirs if not d.startswith(".") and os.path.join(root, d) != assets_dir]
        for fname in files:
            key = fname.lower()
            if key in lookup and key not in matched_origs:
                item = lookup[key]
                src_path = os.path.join(root, fname)
                dst_path = os.path.join(assets_dir, item["local"])
                shutil.copy2(src_path, dst_path)
                matched_origs.add(key)
                found_count += 1
                print(f"  ✓ found '{fname}' -> saved as assets/{item['local']}")

    missing = [item for item in manifest if item["orig"].lower() not in matched_origs]

    print(f"\n{found_count} / {len(manifest)} files matched and copied into assets/.")

    if missing:
        print(f"\n{len(missing)} still missing (script didn't find these anywhere in {source_dir}):\n")
        for item in missing:
            uses = ", ".join(item.get("used_in", []))
            reuse_note = f"  [used in {len(item['used_in'])} places]" if len(item.get("used_in", [])) > 1 else ""
            print(f"  - {item['orig']}  (needed as assets/{item['local']}{reuse_note})")
            print(f"      used in: {uses}")
        print("\nFor these, you'll need to re-take/re-save them manually, rename to the filename shown, and drop into assets/.")
        print("Note: a file only needs to be saved once even if it's used in multiple spots on the site.")
    else:
        print("\nEverything matched. Your assets/ folder is complete!")

if __name__ == "__main__":
    main()
