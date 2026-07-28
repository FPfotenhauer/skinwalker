# ADR 0005: Deployment per manuellem Upload auf bestehenden Webspace

## Status
Angenommen

## Kontext
skinwalker.de läuft auf bereits vorhandenem Webspace (bisher für WordPress
genutzt). Es gibt keine Anforderung nach automatisiertem Deployment,
Versionierung auf dem Server oder CI/CD — die Seite wird selten aktualisiert
(neue Bilder gelegentlich), und der Betreiber möchte selbst die Kontrolle
über den Upload behalten.

## Entscheidung
Die fertigen statischen Dateien aus `site/` werden manuell per FTP/SFTP (z.B.
mit FileZilla oder dem Tool des Hosting-Anbieters) auf den Webspace
hochgeladen. Es wird keine automatisierte Deployment-Pipeline (CI/CD)
eingerichtet.

## Konsequenzen
- Kein zusätzliches Konto/Secret für einen Deployment-Dienst nötig, keine
  Abhängigkeit von einem CI-Anbieter.
- Updates erfordern einen manuellen Schritt (Dateien hochladen); das ist bei
  der erwarteten geringen Änderungsfrequenz kein relevanter Nachteil.
- Das Repository ist die Quelle der Wahrheit für den Seiteninhalt; der
  Webspace-Zustand wird nicht separat versioniert, sollte also nach jedem
  Upload dem Repository-Stand entsprechen.
