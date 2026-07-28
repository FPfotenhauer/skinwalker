# ADR 0001: Statische Seite statt WordPress

## Status
Angenommen

## Kontext
skinwalker.de lief bisher auf WordPress. Der Inhalt der Seite soll aber nur aus
wenigen Bildern mit kurzen Begleittexten bestehen — kein Blog, keine
Kommentare, keine Nutzerkonten, keine Plugins. WordPress bringt dafür
unnötigen Aufwand mit sich: Datenbank, PHP-Betrieb, Updates/Sicherheitspatches,
Plugin-Pflege, Login-Absicherung. Der bisherige Betreiber empfindet das als
"viel zu übertrieben" für den eigentlichen Zweck der Seite.

## Entscheidung
Die Seite wird als reine statische Website (HTML/CSS/JS-Dateien) umgesetzt.
Es gibt keine Datenbank, keine serverseitige Programmiersprache und kein CMS
mehr. Die fertigen Dateien werden direkt per FTP/SFTP auf den bestehenden
Webspace hochgeladen.

## Konsequenzen
- Kein Wartungsaufwand für Software-Updates, keine Angriffsfläche durch
  CMS/Plugins/Datenbank.
- Hosting-Anforderungen sinken auf reines Ausliefern statischer Dateien —
  jeder einfache Webspace reicht, PHP/MySQL werden nicht mehr benötigt.
- Änderungen an Inhalten erfordern direktes Bearbeiten der Dateien
  (siehe [ADR 0002](0002-keine-build-tools.md)) statt eines Redaktionssystems.
- Bestehende WordPress-Inhalte (falls noch vorhanden) werden nicht migriert,
  da die neue Seite inhaltlich neu aufgebaut wird.
