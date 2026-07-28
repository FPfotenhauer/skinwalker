# ADR 0010: Signal-Workflow fuer Bildbeitraege

## Status
Angenommen

## Kontext
Beitraege unterhalb des Hero-Headers werden bisher manuell in `site/index.html`
ergaenzt. Bilder fuer solche Beitraege liegen als Originale in `pics/` und als
Web-Kopien in `site/img/pics/`. Vor einem Commit muessen GPS/EXIF-Daten aus den
Originalen entfernt werden (siehe ADR 0007), weil per Smartphone gesendete
Fotos private Standortdaten enthalten koennen.

Frank moechte neue Beitraege per Signal an Paw liefern: ein Bild sowie
Ueberschrift und Text. Paw soll daraus keinen direkten Push auf `develop`
machen, sondern einen Pull Request gegen `develop` erstellen.

## Entscheidung
Ein neues Hilfsskript `scripts/create-post-pr.py` erzeugt einen Beitrag aus
einem lokalen Bildpfad, einer Ueberschrift, Text und optionalem Alt-Text.
Der Signal-Dienst darf dieses Skript nur nach einem ausdruecklichen
`skinwalker post`-Befehl von Frank aufrufen.

Der Ablauf ist:

1. Genau ein ausstehendes Signal-Bild auswaehlen.
2. Bild nach `pics/` kopieren.
3. `scripts/strip-exif.py` ausfuehren und pruefen, dass keine APP1/APP13-
   Metadaten-Segmente mehr vorhanden sind.
4. `scripts/prepare-images.py` ausfuehren.
5. Einen neuen `<article class="post">` mit aktuellem Datum in
   `site/index.html` einfuegen.
6. Einen Branch von `develop` erstellen, committen, pushen und einen Pull
   Request gegen `develop` oeffnen.

Das Datum kommt immer vom aktuellen Systemdatum des Ausfuehrungszeitpunkts.
Ueberschrift und Text muessen per Signal geliefert werden.

## Konsequenzen
- Paw erstellt Skinwalker-Beitraege nur bei explizitem Signal-Befehl, nicht aus
  beliebigen gesendeten Bildern.
- Originalbilder im PR sind vor dem Commit von EXIF/GPS/XMP/IPTC-Metadaten
  befreit.
- Der PR bleibt der Kontrollpunkt vor `develop`; Frank kann den Beitrag und das
  bereinigte Bild vor dem Merge pruefen.
- Der lokale Rechner braucht Python 3 mit Pillow, weil `prepare-images.py` die
  Web-Kopie erzeugt.
