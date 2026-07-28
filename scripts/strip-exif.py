#!/usr/bin/env python3
"""Entfernt EXIF/XMP-Metadaten (u.a. GPS-Standort) verlustfrei aus JPEGs.

Arbeitet direkt auf den Marker-Segmenten der JPEG-Datei und lässt die
komprimierten Bilddaten unverändert -- im Gegensatz zu prepare-images.py
wird hier nichts neu kodiert. Gedacht fuer die Originale in hero-pics/ und
pics/, bevor sie ins Repository eingecheckt werden.

Siehe docs/adr/0007-exif-entfernung-aus-originalen.md
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE_DIRS = [ROOT / "hero-pics", ROOT / "pics"]

# Marker, die komplett entfernt werden: APP1 (EXIF und/oder XMP), APP13 (Photoshop IRB/IPTC)
STRIP_MARKERS = {0xE1, 0xED}
# Marker ohne eigenes Längenfeld / mit Sonderbehandlung
SOI, EOI, SOS = 0xD8, 0xD9, 0xDA


def strip(path: Path) -> tuple[int, int]:
    with open(path, "rb") as f:
        data = f.read()

    assert data[0] == 0xFF and data[1] == SOI, f"{path}: kein gültiges JPEG"

    out = bytearray(data[:2])  # SOI
    i = 2
    removed = 0
    while i < len(data):
        assert data[i] == 0xFF, f"{path}: Marker erwartet bei Offset {i}"
        marker = data[i + 1]

        if marker == SOS:
            # Ab hier folgen die komprimierten Scan-Daten bis EOI -- unverändert übernehmen
            out += data[i:]
            break

        if marker in (0x01,) or 0xD0 <= marker <= 0xD7:
            # Marker ohne Länge (TEM, RST0-7) -- kommt vor SOS praktisch nicht vor, sicherheitshalber behandeln
            out += data[i:i + 2]
            i += 2
            continue

        length = (data[i + 2] << 8) + data[i + 3]
        segment = data[i:i + 2 + length]

        if marker in STRIP_MARKERS:
            removed += len(segment)
        else:
            out += segment

        i += 2 + length

    with open(path, "wb") as f:
        f.write(out)

    return len(data), removed


def main() -> None:
    targets = sorted(
        p for d in SOURCE_DIRS for p in d.glob("*.[Jj][Pp][Gg]")
    )
    if not targets:
        print("Keine Bilder in hero-pics/ oder pics/ gefunden.")
        sys.exit(1)

    for path in targets:
        before, removed = strip(path)
        rel = path.relative_to(ROOT)
        print(f"{str(rel):45s} {before / 1024:>7.0f} KB, {removed} Bytes Metadaten entfernt")


if __name__ == "__main__":
    main()
