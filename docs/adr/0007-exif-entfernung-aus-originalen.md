# ADR 0007: Verlustfreie Entfernung von EXIF/GPS-Daten aus den Originalbildern

## Status
Angenommen

## Kontext
[ADR 0004](0004-bildaufbereitung.md) entfernt EXIF-Daten bereits aus den für
die Website erzeugten Kopien in `site/img/`. Die Originaldateien in
`hero-pics/` bzw. `pics/` sollen nun aber ebenfalls ins Git-Repository eingecheckt werden
(Versionierung der Rohdaten). Kamerafotos enthalten standardmäßig GPS-Daten;
bei Aufnahmen des eigenen Balkonblicks verraten diese Koordinaten praktisch
die private Wohnadresse. Sobald das Repository committet (und ggf. später
veröffentlicht) wird, wären diese Koordinaten damit dauerhaft in der
Git-Historie enthalten.

Ein einfaches Neukodieren der Bilder (wie in ADR 0004 für die Web-Kopien)
würde die Originalqualität verschlechtern und ist für Archivmaterial nicht
gewünscht. Externe Werkzeuge wie `exiftool` oder `jpegtran`, die Metadaten
verlustfrei entfernen können, sind auf dem Entwicklungsrechner nicht
installiert.

## Entscheidung
Ein eigenständiges Skript (`scripts/strip-exif.py`, reine Python-Standard-
bibliothek) entfernt die EXIF- und XMP/IPTC-Marker-Segmente (JPEG-Marker
APP1 und APP13) direkt auf Byte-Ebene aus den Originaldateien in
`hero-pics/` bzw. `pics/`. Die komprimierten Bilddaten (alles ab dem SOS-Marker) werden
unverändert kopiert — es findet keine Neukodierung statt. Das Skript wird
einmalig auf den bestehenden Bestand angewendet und danach bei Bedarf für
neu hinzukommende Originale erneut ausgeführt, bevor sie committet werden.

## Konsequenzen
- Die Originaldateien in `hero-pics/` bzw. `pics/` sind bit-identisch in ihren Bilddaten,
  aber frei von GPS-Koordinaten und sonstigen EXIF/IPTC-Metadaten — sicher
  fürs Einchecken ins Repository.
- Aufnahmedatum, Kameramodell etc. gehen dabei ebenfalls verloren, da sie im
  selben Marker-Segment stehen wie die GPS-Daten. Das wird in Kauf genommen,
  da diese Information für den Zweck der Seite nicht benötigt wird.
- Neue Originalfotos sollten vor dem `git add` durch
  `python3 scripts/strip-exif.py` laufen, bevor sie committet werden — analog
  zum bestehenden Workflow mit `prepare-images.py` für die Web-Kopien.
- Das Skript ersetzt nicht die Bildaufbereitung aus
  [ADR 0004](0004-bildaufbereitung.md); beide Skripte haben unterschiedliche
  Zwecke (Archivqualität ohne Metadaten vs. verkleinerte Web-Kopien).
