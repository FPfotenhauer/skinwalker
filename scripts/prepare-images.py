#!/usr/bin/env python3
"""Verkleinert und komprimiert Originalfotos nach site/img/.

hero-pics/ (Kopfbild-Pool) und pics/ (kuenftige Beitraege unterhalb des
Headers) werden getrennt gehalten und landen entsprechend in
site/img/hero/ bzw. site/img/pics/.

Siehe docs/adr/0004-bildaufbereitung.md und
docs/adr/0008-trennung-hero-und-body-bilder.md
"""
import sys
from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SOURCES = {
    "hero": ROOT / "hero-pics",
    "pics": ROOT / "pics",
}
DST_ROOT = ROOT / "site" / "img"
MAX_WIDTH = 1920
JPEG_QUALITY = 82


def prepare_image(src: Path, dst: Path) -> None:
    with Image.open(src) as img:
        img = ImageOps.exif_transpose(img)  # korrekte Ausrichtung anwenden
        img = img.convert("RGB")
        if img.width > MAX_WIDTH:
            new_height = round(img.height * MAX_WIDTH / img.width)
            img = img.resize((MAX_WIDTH, new_height), Image.LANCZOS)
        # exif bewusst nicht mitgespeichert: entfernt u.a. GPS-Standortdaten
        img.save(dst, "JPEG", quality=JPEG_QUALITY, optimize=True)


def main() -> None:
    found_any = False
    for label, src_dir in SOURCES.items():
        dst_dir = DST_ROOT / label
        sources = sorted(src_dir.glob("*.[Jj][Pp][Gg]"))
        if not sources:
            print(f"Keine Bilder in {src_dir} gefunden, überspringe.")
            continue

        found_any = True
        dst_dir.mkdir(parents=True, exist_ok=True)
        for src in sources:
            dst = dst_dir / f"{src.stem.lower()}.jpg"
            prepare_image(src, dst)
            before = src.stat().st_size // 1024
            after = dst.stat().st_size // 1024
            print(f"{src.name:35s} {before:>5d} KB -> {label}/{dst.name:25s} {after:>5d} KB")

    if not found_any:
        print("Keine Bilder gefunden.")
        sys.exit(1)


if __name__ == "__main__":
    main()
