# Rakshabandhan Site — Recovery Kit

**60 unique files** are needed (not 74). 13 of your original files were used in more than one place on the site (e.g. the hero banner photo is also in Behind the Scenes), those only need to be saved **once**, `index.html` already points every usage to the same filename.

## Fastest option: auto-rename script
If you still have the original photos/videos saved anywhere on your computer or phone
(even in a messy folder, subfolders are fine), do this:

1. Put/copy all your recovered files into one folder (any name, anywhere).
2. Open a terminal in this folder (the one with `rename_and_copy.py` in it).
3. Run:
   ```
   python3 rename_and_copy.py /path/to/that/folder
   ```
4. It'll scan the folder, match filenames against what's needed, copy and
   rename matches straight into `assets/`, and print a report of what it
   found and what's still missing.

You can run it multiple times as you recover more files, it'll only ever
add what's missing.

## Manual option
Open `rename-guide.html` in your browser for a checklist version with
progress tracking, or `manifest.md` for a plain text version. Both list
every original filename next to the new filename it needs.

## Once assets/ is filled
Push `index.html` + `assets/` to your GitHub repo (overwriting the old
`index.html`), Vercel will redeploy automatically.
