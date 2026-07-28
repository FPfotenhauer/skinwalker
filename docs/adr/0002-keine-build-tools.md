# ADR 0002: Handgeschriebenes HTML/CSS/JS ohne Build-Schritt

## Status
Angenommen

## Kontext
Für eine statische Seite ([ADR 0001](0001-static-site-statt-wordpress.md)) gibt
es grundsätzlich zwei Wege: die Seiten von Hand in HTML/CSS/JS schreiben, oder
einen Static-Site-Generator (z.B. Eleventy, Hugo) einsetzen, der aus
Inhaltsdateien (Markdown/JSON) automatisch HTML erzeugt.

Ein Generator würde das Hinzufügen vieler Bilder etwas komfortabler machen,
verlangt aber eine lokale Node.js/Toolchain-Installation, einen Build-Schritt
vor jedem Upload und Pflege einer zusätzlichen Abhängigkeit über Jahre hinweg.
Bei der überschaubaren Anzahl an Bildern und dem Wunsch nach maximaler
Einfachheit überwiegt der Aufwand den Nutzen.

## Entscheidung
Die Seite besteht aus einer handgeschriebenen `index.html`, einer CSS-Datei
und optional etwas Vanilla-JavaScript (z.B. für eine Lightbox-Ansicht). Es
gibt keinen Build-Prozess, kein Framework und keine Paketabhängigkeiten für
die Website selbst. Ein neues Bild mit Text wird hinzugefügt, indem ein
bestehender HTML-Block in der Galerie kopiert und angepasst wird.

Die einzige Ausnahme ist ein separates, optionales Hilfsskript zur
Bildaufbereitung (siehe [ADR 0004](0004-bildaufbereitung.md)) — das erzeugt
keine HTML-Struktur, sondern nur optimierte Bilddateien, und ist kein
Bestandteil eines "Seiten-Builds".

## Konsequenzen
- Die hochgeladenen Dateien sind exakt die Dateien, die im Repository liegen
  — kein Zwischenschritt, keine Toolchain-Abhängigkeit, funktioniert auch in
  vielen Jahren noch ohne Anpassung.
- Neue Bilder/Texte hinzuzufügen bedeutet manuelles Copy-Paste eines
  HTML-Blocks statt eines einfachen Dateidrops. Bei der erwarteten geringen
  Anzahl an Bildern ist das akzeptabel.
- Es gibt keine Templating-Wiederverwendung; Änderungen am Layout aller
  Galerie-Einträge (z.B. neues Design) müssen ggf. mehrfach angepasst werden,
  falls sie nicht über gemeinsames CSS gelöst werden können.
