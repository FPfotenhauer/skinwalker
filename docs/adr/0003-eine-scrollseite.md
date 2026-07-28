# ADR 0003: Eine durchgehende Seite statt Übersicht mit Einzelseiten

## Status
Angenommen

## Kontext
Die Seite soll den Blick vom Balkon als Herzstück zeigen sowie einige weitere
Bilder mit kurzen Texten. Zwei Strukturen kommen infrage: eine einzelne Seite
zum Durchscrollen (Hero-Bild + Galerie darunter), oder eine Übersichtsseite
mit Vorschaubildern, die auf einzelne Detailseiten pro Bild verlinkt.

Bei einer kleinen, kuratierten Bildersammlung ohne Anspruch auf Kategorien,
Suche oder große Textmengen pro Bild bietet eine einzelne Seite die geringste
Komplexität für Aufbau und Pflege.

## Entscheidung
Die Seite besteht aus einer einzigen `index.html`. Ganz oben steht groß der
Blick vom Balkon als Hero-Bild. Darunter folgt eine vertikal scrollende
Galerie aus Bild-Text-Paaren. Es gibt keine Unterseiten und keine klassische
Navigation.

## Konsequenzen
- Einfachste mögliche Struktur: eine Datei, kein Routing, kein Menü.
- Gut für Mobilgeräte (Scrollen statt Klicken durch Unterseiten).
- Bei sehr vielen zukünftigen Bildern könnte die Seite lang und die initiale
  Ladezeit relevant werden — dem wird durch Lazy-Loading der Bilder begegnet.
- Einzelne Bilder sind nicht direkt per eigener URL verlinkbar (kein Deep
  Link auf ein bestimmtes Foto), was für den aktuellen Zweck akzeptiert wird.
