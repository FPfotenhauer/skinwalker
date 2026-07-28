# ADR 0004: Automatisierte Bildaufbereitung über ein lokales Hilfsskript

## Status
Angenommen

## Kontext
Die Originalfotos liegen als Kamera-Dateien vor (bis ca. 2,4 MB, bis
5333×3000 Pixel). In dieser Größe direkt im Web ausgeliefert, würden sie
lange Ladezeiten verursachen, besonders auf Mobilgeräten. Gleichzeitig soll
laut [ADR 0002](0002-keine-build-tools.md) die eigentliche Website ohne
Build-Schritt auskommen.

Beides lässt sich vereinbaren, wenn die Bildaufbereitung nicht als
Seiten-Build, sondern als eigenständiges, optionales Werkzeug behandelt wird:
Es erzeugt lediglich fertige Bilddateien, keine HTML-Struktur.

## Entscheidung
Ein kleines lokales Skript (Python mit Pillow; alternativ ImageMagick, falls
verfügbar) verkleinert und komprimiert neu hinzugefügte Originalbilder aus
`hero-pics/` bzw. `pics/` (siehe
[ADR 0008](0008-trennung-hero-und-body-bilder.md)) auf webtaugliche Maße
(z.B. max. 1920 px Breite) und legt sie im jeweils passenden Ausgabeordner
`site/img/hero/` bzw. `site/img/pics/` ab — als komprimiertes JPEG. Das
Skript wird manuell ausgeführt, wenn ein neues Bild hinzukommt, und ist kein
automatischer Bestandteil des Uploads.

## Konsequenzen
- Originaldateien (`hero-pics/`, `pics/`) bleiben unverändert erhalten; die
  Website nutzt ausschließlich die aufbereiteten Kopien.
- Neues Bild hinzufügen = Originaldatei ablegen, Skript einmal laufen lassen,
  HTML-Block ergänzen (siehe [ADR 0002](0002-keine-build-tools.md)).
- Für die Skript-Ausführung wird lokal Python 3 mit Pillow benötigt — eine
  einmalige, leichtgewichtige Abhängigkeit, die nicht auf dem Webspace
  installiert sein muss, da nur die fertigen Bilder hochgeladen werden.
- Ladezeiten und Datenvolumen der Seite bleiben auch bei hochauflösenden
  Originalen kontrollierbar.
