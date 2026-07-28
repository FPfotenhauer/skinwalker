#!/usr/bin/env python3
"""Bereitet site/ vollständig für den Upload auf den Webspace vor.

Führt der Reihe nach aus:
  1. strip-exif.py    -- GPS/EXIF aus den Originalen in hero-pics/ und pics/ entfernen
  2. prepare-images.py -- Web-Kopien nach site/img/hero/ bzw. site/img/pics/ erzeugen
  3. impressum.md (falls vorhanden) nach site/impressum.html übertragen

Danach kann der komplette Inhalt von site/ 1:1 auf den Webspace kopiert werden.

Siehe docs/adr/0009-release-skript.md
"""
import re
import subprocess
import sys
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
IMPRESSUM_SRC = ROOT / "impressum.md"
IMPRESSUM_DST = ROOT / "site" / "impressum.html"

PAGE_TEMPLATE = """<!doctype html>
<html lang="de">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Impressum &mdash; skinwalker.de</title>
  <link rel="stylesheet" href="css/style.css" />
</head>
<body>
  <main class="legal">
    <p><a href="index.html">&larr; zurück</a></p>
{content}
  </main>

  <footer>
    <p>&copy; 2026 skinwalker.de &middot; <a href="impressum.html">Impressum</a></p>
  </footer>
</body>
</html>
"""


def run_step(script_name: str) -> None:
    print(f"--- {script_name} ---", flush=True)
    result = subprocess.run([sys.executable, str(SCRIPTS_DIR / script_name)], cwd=ROOT)
    if result.returncode != 0:
        print(f"Abgebrochen: {script_name} ist fehlgeschlagen.")
        sys.exit(result.returncode)


def markdown_to_html(text: str) -> str:
    """Minimaler Markdown->HTML-Konverter fuer die einfache Impressum-Struktur
    (Ueberschriften, durch Leerzeilen getrennte Absaetze, **fett**). Kein
    Ersatz fuer einen vollstaendigen Markdown-Parser, reicht aber fuer diesen
    einen, selbst geschriebenen Anwendungsfall."""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL).strip()
    blocks = [b for b in re.split(r"\n\s*\n", text) if b.strip()]

    html_blocks = []
    for block in blocks:
        lines = block.strip("\n").split("\n")
        first = lines[0]
        if first.startswith("## "):
            html_blocks.append(f"    <h2>{escape(first[3:])}</h2>")
        elif first.startswith("# "):
            html_blocks.append(f"    <h1>{escape(first[2:])}</h1>")
        else:
            joined = "<br>\n      ".join(escape(l) for l in lines)
            joined = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", joined)
            html_blocks.append(f"    <p>\n      {joined}\n    </p>")

    return "\n".join(html_blocks)


def build_impressum() -> None:
    print("--- impressum.html ---")
    if not IMPRESSUM_SRC.exists():
        print(
            "Keine impressum.md gefunden -- übersprungen. "
            "Siehe impressum.example.md, um eine anzulegen."
        )
        return

    content = markdown_to_html(IMPRESSUM_SRC.read_text(encoding="utf-8"))
    IMPRESSUM_DST.write_text(
        PAGE_TEMPLATE.format(content=content), encoding="utf-8"
    )
    print(f"{IMPRESSUM_DST.relative_to(ROOT)} geschrieben.")


def main() -> None:
    run_step("strip-exif.py")
    run_step("prepare-images.py")
    build_impressum()
    print("\nFertig. Inhalt von site/ kann jetzt auf den Webspace hochgeladen werden.")


if __name__ == "__main__":
    main()
