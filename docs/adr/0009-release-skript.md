# ADR 0009: Release-Skript zur vollständigen Vorbereitung von site/

## Status
Angenommen

## Kontext
Vor dem Hochladen mussten bisher mehrere Schritte manuell in der richtigen
Reihenfolge ausgeführt werden: `strip-exif.py` (GPS/EXIF aus den Originalen
entfernen, [ADR 0007](0007-exif-entfernung-aus-originalen.md)),
`prepare-images.py` (Web-Kopien erzeugen, [ADR 0004](0004-bildaufbereitung.md))
und — neu hinzugekommen — das persönliche `impressum.md` in eine
`site/impressum.html` überführen. Das Ziel ist, dass am Ende nur noch der
Inhalt von `site/` auf den Webspace kopiert werden muss, ohne dass private
Daten (Original-EXIF, `impressum.md`) dabei mit hochgeladen oder ins Git-
Repository übernommen werden.

`impressum.md` bleibt bewusst außerhalb von Git (`.gitignore`), da es echte
persönliche Daten (Name, Anschrift) enthält. Für die Umwandlung in HTML war
keine Markdown-Bibliothek auf dem Rechner installiert; da das Dokument nur
eine sehr einfache, selbst festgelegte Struktur hat (Überschriften, durch
Leerzeilen getrennte Absätze, `**fett**`), reicht dafür ein kleiner
selbstgeschriebener Konverter ohne neue Abhängigkeit.

## Entscheidung
Ein neues Skript `scripts/release.py` orchestriert die drei Schritte in der
richtigen Reihenfolge:

1. `strip-exif.py` ausführen
2. `prepare-images.py` ausführen
3. Falls `impressum.md` existiert: Inhalt über einen minimalen, im Skript
   eingebauten Markdown-zu-HTML-Konverter in `site/impressum.html`
   schreiben, eingebettet in dieselbe Kopf-/Fußzeilen-Struktur wie
   `index.html`. Fehlt `impressum.md`, wird der Schritt übersprungen und eine
   Warnung ausgegeben (kein Abbruch).

`index.html` verlinkt im Footer fest auf `impressum.html`. Der Nutzer führt
`python3 scripts/release.py` einmal aus und lädt danach ausschließlich den
Inhalt von `site/` hoch.

## Konsequenzen
- Ein einziger Befehl statt drei einzelner Skript-Aufrufe vor jedem Release.
- `site/impressum.html` ist eine generierte Datei (aus `impressum.md`) und
  wird bei jedem Lauf neu geschrieben — keine manuellen Änderungen direkt in
  `site/impressum.html` vornehmen, sie gehen beim nächsten Release verloren.
- Der eingebaute Markdown-Konverter ist bewusst minimal und nur auf die
  Struktur von `impressum.md`/`impressum.example.md` ausgelegt (Überschriften,
  Absätze, Fettschrift) — kein allgemeiner Markdown-Parser. Das bleibt im
  Sinne von [ADR 0002](0002-keine-build-tools.md), da hier keine neue
  Abhängigkeit für die eigentliche Website eingeführt wird.
- Falls `impressum.md` beim Release fehlt, bleibt eine eventuell vorhandene
  alte `site/impressum.html` unverändert stehen; der Footer-Link würde in
  einem frischen Checkout ohne `impressum.md` ins Leere laufen, bis das
  Skript einmal mit vorhandenem `impressum.md` gelaufen ist.
