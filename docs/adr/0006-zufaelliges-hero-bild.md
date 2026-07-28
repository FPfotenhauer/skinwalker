# ADR 0006: Zufälliges Hero-Bild aus einem Bilderpool

## Status
Angenommen

## Kontext
Der Balkonblick soll laut [ADR 0003](0003-eine-scrollseite.md) groß im Kopf
der Seite stehen. Es existieren mehrere Aufnahmen derselben Aussicht zu
unterschiedlichen Tageszeiten und Wetterlagen (Sonnenuntergang, Dämmerung,
Nacht, Regenbogen). Statt ein einzelnes Bild fest auszuwählen, soll bei jedem
Seitenaufruf zufällig eines aus diesem Pool als Hero-Bild erscheinen.

Da die Seite laut [ADR 0002](0002-keine-build-tools.md) ohne Build-Prozess
auskommt, muss die Zufallsauswahl clientseitig passieren.

## Entscheidung
Eine kleine Vanilla-JS-Datei enthält eine Liste der Dateinamen aller
Hero-Pool-Bilder. Beim Laden der Seite wird zufällig ein Eintrag ausgewählt
und als Hintergrund/Bild des Headers gesetzt. Die Bildliste wird von Hand in
der JS-Datei gepflegt (ein neues Balkonfoto = ein neuer Eintrag in der
Liste), analog zum manuellen Pflegen der Galerie-Blöcke in der HTML.

## Konsequenzen
- Jeder Seitenaufruf kann eine andere Stimmung zeigen, ohne dass mehrere
  Hero-Varianten der Seite gepflegt werden müssten.
- Die Auswahl passiert im Browser; ohne aktiviertes JavaScript wird ein
  festes Fallback-Bild angezeigt (progressive enhancement).
- Da alle Pool-Bilder als Hero geladen werden könnten, müssen alle in
  vergleichbarer, webtauglicher Qualität vorliegen (siehe
  [ADR 0004](0004-bildaufbereitung.md)) — unabhängig davon, ob sie zusätzlich
  auch als Galerie-Eintrag mit Text erscheinen.
