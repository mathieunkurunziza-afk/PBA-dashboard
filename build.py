"""Builds the two versions of the dashboard from src/dashboard.html.
   index.html            -> GitHub Pages version (reads data/active_schools.csv)
   dist/claude.html      -> Claude version (reads its own database)"""
import pathlib
root = pathlib.Path(__file__).parent
src = (root / "src/dashboard.html").read_text()
head = ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
        '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n')
gh = src.replace('MODE: "__MODE__"', 'MODE: "csv"')
i = gh.index("<header")
(root / "index.html").write_text(head + gh[:i] + "</head>\n<body>\n" + gh[i:] + "</body>\n</html>\n")
(root / "dist").mkdir(exist_ok=True)
(root / "dist/claude.html").write_text(src.replace('MODE: "__MODE__"', 'MODE: "claude"'))
print("built index.html and dist/claude.html")
