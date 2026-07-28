# ADR 0008: Getrennte Ordner für Hero- und Body-Bilder

## Status
Angenommen

## Kontext
Bisher lagen alle Originalfotos in einem einzigen Ordner (`Pictures/`) und
wurden komplett als Hero-Pool behandelt (siehe
[ADR 0006](0006-zufaelliges-hero-bild.md)). Laut
[ADR 0003](0003-eine-scrollseite.md) soll die Seite später zusätzlich kurze
Beiträge unterhalb des Headers bekommen. Diese Body-Bilder sind inhaltlich
etwas anderes als der rotierende Balkonblick im Header und sollen nicht
automatisch im Hero-Pool landen, nur weil sie im selben Ordner liegen.

## Entscheidung
Die Originalfotos werden ab sofort in zwei getrennten Ordnern gepflegt:

- `hero-pics/` — der bisherige `Pictures/`-Ordner, umbenannt. Enthält
  ausschließlich Aufnahmen für den zufälligen Hero-Header.
- `pics/` — neu angelegt, zunächst leer. Für zukünftige Fotos, die als
  einzelne Beiträge mit Text unterhalb des Headers erscheinen sollen.

Beide Ordner werden von den bestehenden Hilfsskripten
([ADR 0004](0004-bildaufbereitung.md), [ADR 0007](0007-exif-entfernung-aus-originalen.md))
gleich behandelt, aber getrennt verarbeitet: `prepare-images.py` erzeugt aus
`hero-pics/` die Web-Kopien in `site/img/hero/`, aus `pics/` entsprechend in
`site/img/pics/`. `strip-exif.py` entfernt Metadaten aus beiden Ordnern.

## Konsequenzen
- Ein neues Foto landet automatisch nur dann im Hero-Pool, wenn es bewusst
  in `hero-pics/` abgelegt wird — kein versehentliches Vermischen mit
  künftigen Body-Bildern.
- `hero.js` referenziert Hero-Bilder jetzt unter `img/hero/…` statt `img/…`.
- `pics/` und `site/img/pics/` bleiben vorerst ungenutzt, bis die Galerie
  unterhalb des Headers tatsächlich gebaut wird; das Verzeichnis existiert
  bereits, damit die Struktur von Anfang an klar ist.
