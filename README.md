# Automatischer THWS-M2IV-Kalender

Dieses Projekt soll die öffentlich verfügbare THWS-Stundenplanseite stündlich auslesen, daraus eine ICS-Kalenderdatei erstellen und diese mit GitHub Pages bereitstellen. **Python muss dafür nicht auf dem Mac installiert sein**: Das Skript läuft auf den von GitHub bereitgestellten Rechnern (GitHub Actions).

Quelle: <https://business.thws.de/fileadmin/share/vlplan/M2IV%201%20WS%2026_27.html>

## Was das Projekt macht

- Liest Termine aus der HTML-Stundenplanseite und erstellt `stundenplan.ics`.
- Fügt das erkannte Standortkürzel **(Frie)** oder **(Mü)** direkt an den Veranstaltungstitel an. Der Raum bleibt zusätzlich im Ortsfeld des Kalendereintrags.
- Lässt Termine weg, wenn sie in der Quelle eindeutig als entfallen/abgesagt markiert oder in HTML als durchgestrichen gekennzeichnet sind. Wenn ein Termin aus der Quelle vollständig entfernt wird, fehlt er ebenfalls im nächsten Kalenderfeed.
- Verwendet möglichst stabile Ereignis-IDs, sodass Änderungen an Uhrzeit, Raum oder Standort nicht unnötig einen neuen Termin erzeugen.
- Versucht stündlich eine Aktualisierung und kann von Hand gestartet werden.
- Bricht ab, statt einen offensichtlich unvollständigen Kalender zu veröffentlichen, wenn weniger als 25 Termine erkannt werden.

**Wichtige Einschränkung:** Die Änderungen wurden mit künstlichen Beispiel-HTML-Dateien getestet, aber der Live-Abruf der echten THWS-Seite konnte in der Entwicklungsumgebung noch nicht erfolgreich ausgeführt werden. Der erste Lauf in GitHub Actions ist deshalb der verbindliche Live-Test. Solange der Live-Test nicht erfolgreich ist, bitte noch nicht auf den Kalender verlassen.

## Wichtig: Ausfälle und Aktualisierungen

Ein Ausfall kann automatisch erkannt werden, wenn die THWS-Seite den Termin entfernt oder ihn eindeutig als entfallen/abgesagt kennzeichnet. Das Skript lässt ihn dann im neu veröffentlichten ICS-Feed weg. Apple Kalender liest abonnierte Kalender jedoch nach einem eigenen Aktualisierungsplan ein; Änderungen erscheinen daher nicht unbedingt sofort. Auf dem Mac kann man den Kalender außerdem per Rechtsklick auf den Kalendernamen → **Informationen** → **Automatisch aktualisieren** konfigurieren bzw. über **Darstellung → Kalender aktualisieren** neu abrufen.

Wenn ein Dozent eine Vorlesung nur per E-Mail absagt und die THWS-Seite unverändert bleibt, kann dieses Projekt das nicht wissen. Bei kurzfristigen Änderungen immer die Originalseite oder die direkte Nachricht prüfen.

## Dateien

- `update_calendar.py`: Ruft die Seite ab, parst Veranstaltungen, filtert erkennbare Ausfälle und erzeugt den ICS-Feed.
- `.github/workflows/update-calendar.yml`: Führt das Skript stündlich bzw. auf manuellen Start aus und veröffentlicht das Ergebnis.
- `public/index.html`: Statusseite und Link zum Kalender.
- `tests/`: Beispielseite und automatisierte Tests für Frie/Mü, Termine und Ausfälle.

## Schritt-für-Schritt-Einrichtung (ohne Python auf dem Mac)

### 1. Projekt entpacken

1. Lade die ZIP-Datei herunter und öffne sie per Doppelklick im Finder.
2. Öffne den entpackten Ordner `thws_stundenplan_automatik`.
3. Im Finder `⌘` + `Shift` + `.` drücken, um versteckte Dateien anzuzeigen. Das ist wichtig, damit du den Ordner `.github` mit hochlädst.

### 2. Ein öffentliches Repository erstellen

1. Melde dich bei <https://github.com/> an oder erstelle einen Account.
2. Klicke auf **+** → **New repository**.
3. Repository name: `thws-stundenplan-kalender`.
4. Wähle **Public**. GitHub Pages ist im kostenlosen GitHub-Tarif für öffentliche Repositories verfügbar. Bitte bedenke, dass das Projekt und die ICS-Datei dadurch öffentlich sind.
5. Lass **Add a README file**, `.gitignore` und Lizenz zunächst abgewählt und klicke **Create repository**.

### 3. Projektdateien hochladen

1. Im neuen Repository **Add file → Upload files** anklicken.
2. Lade **den Inhalt** des entpackten Ordners hoch, nicht nur den äußeren Ordner `thws_stundenplan_automatik`. Die Datei `update_calendar.py`, die Ordner `public` und `tests` sowie der versteckte Ordner `.github` müssen direkt im Hauptverzeichnis des Repositorys liegen.
3. Kontrolliere vor dem Speichern, dass `.github/workflows/update-calendar.yml` dabei ist.
4. Als Commit message z. B. `Add THWS calendar automation` eintragen und **Commit changes** anklicken.

### 4. GitHub Pages aktivieren

1. Im Repository auf **Settings** klicken.
2. Links **Pages** öffnen.
3. Unter **Build and deployment → Source** `GitHub Actions` auswählen.

### 5. Ersten Live-Test starten

1. Im Repository den Reiter **Actions** öffnen.
2. Links **Update THWS timetable calendar** auswählen.
3. **Run workflow** anklicken und nochmals bestätigen.
4. Den Lauf öffnen. Ein grüner Haken bedeutet, dass das Skript die Website gelesen, ausreichend Termine erkannt und die Seite veröffentlicht hat.
5. Wenn der Lauf rot fehlschlägt, öffne den fehlgeschlagenen Schritt **Fetch THWS page and build calendar** und kopiere die Fehlermeldung. Nicht versuchen, einen leeren oder fehlerhaften Kalender zu abonnieren. Häufigste Ursache wäre ein anderer HTML-Aufbau als in der Testseite; dann muss der Parser angepasst werden.

### 6. ICS-Adresse finden

Nach erfolgreichem Lauf auf **Settings → Pages** gehen. GitHub zeigt dort die veröffentlichte Website-Adresse an. Die Kalenderadresse ist diese Adresse plus `/stundenplan.ics`, zum Beispiel:

`https://DEIN-GITHUB-NAME.github.io/thws-stundenplan-kalender/stundenplan.ics`

Das ist ein Beispiel, keine bereits aktive Adresse. Den Benutzernamen und die Adresse von GitHub übernehmen; nicht wörtlich das Beispiel eingeben.

### 7. Kalender auf dem Mac abonnieren

1. Apple **Kalender** öffnen.
2. In der Menüleiste **Ablage → Neues Kalenderabonnement …** auswählen.
3. Die echte URL mit `/stundenplan.ics` einfügen und **Abonnieren** wählen.
4. Als Namen `THWS M2IV` vergeben. Wenn macOS einen Speicherort anbietet und du den Kalender auch auf anderen Apple-Geräten nutzen möchtest, wähle einen passenden synchronisierten Account; falls er dort nicht erscheint, muss das Abo gegebenenfalls auf dem iPhone separat eingerichtet werden.
5. Nach dem Anlegen mit Rechtsklick auf den Kalender → **Informationen** die automatische Aktualisierung auf **stündlich** setzen, sofern diese Option angeboten wird.

### 8. Änderungen und Ausfälle prüfen

Wenn die THWS-Seite aktualisiert wird, übernimmt GitHub die Änderung normalerweise beim nächsten stündlichen Durchlauf. Du kannst unter **Actions → Update THWS timetable calendar → Run workflow** auch manuell neu abrufen. Anschließend muss Apple Kalender seinen Feed ebenfalls neu laden. Zur Prüfung kannst du **Darstellung → Kalender aktualisieren** wählen. Das Verhalten bei gelöschten Terminen sollte direkt nach dem ersten Live-Abonnement mit einem konkreten Beispiel kontrolliert werden.

## Technische Tests (optional)

Für den Betrieb ist keine lokale Python-Installation nötig. Falls jemand den Parser lokal testen möchte, wird Python 3.11 oder neuer benötigt:

```bash
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
```
