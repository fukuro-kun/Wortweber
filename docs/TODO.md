# TODO Liste für Wortweber

## Dringendes
- [ ] Überprüfung und Optimierung der Gerätekompatibilität für verschiedene Systemkonfigurationen

## Priorität Hoch
- [ ] Verbesserung der Shortcut-Funktionalität (Manuelle Einstellung, Erfassung, Zuverlässigkeit)

## Priorität Mittel
- [ ] Implementierung zusätzlicher Module für die Ausgabe (z.B. Ollama-Unterstützung)
- [ ] Erweiterung der Testabdeckung, insbesondere für kritische Funktionen
- [ ] Einrichtung einer Staging-Umgebung für gründlichere Tests vor Veröffentlichungen
- [ ] Entwicklung eines klaren Rollback-Plans für problematische Releases

## Priorität Niedrig
- [ ] Behandlung des Exception-Fehlers beim Schließen der App während des initialen Modellladens
- [ ] Internationalisierung der Anwendung mittels einfacher Module in Form von String-Dateien
- [ ] Implementierung eines Plugin-Systems basierend auf der neuen modularen Struktur
- [ ] Untersuchung möglicher Performance-Probleme beim Laden großer Transkriptionen
- [ ] Hinzufügen von Tooltips für verschiedene Optionen in der GUI
- [ ] Implementierung einer Funktion zum Zurücksetzen der Einstellungen auf Standardwerte
- [ ] Überprüfung und mögliche Optimierung der Parallelisierungseffizienz der Tests
- [ ] Überprüfen und gegebenenfalls Unterdrücken der ALSA-Warnungen am Anfang der Testausgabe für eine übersichtlichere Darstellung
- [ ] Erweiterung der Testabdeckung für die neuen Optionsfenster- und Farbverwaltungsfunktionen

## Kontinuierliche Verbesserungen
- [ ] Regelmäßige Code-Reviews durchführen
- [ ] Aktualisieren der Abhängigkeiten auf die neuesten stabilen Versionen
- [ ] Verbesserte Dokumentation zur neuen Struktur der Textoperationen im Backend
- [ ] Detailliertere Dokumentation von Änderungen und deren erwarteten Auswirkungen
- [ ] Regelmäßige Überprüfung und Aktualisierung der Kommentare im Code

## Neue Aufgaben
- [ ] Durchführen von Benutzertest zur Evaluierung der neuen Farbauswahlfunktion
- [ ] Implementierung von Vorschau-Funktionalität für Farbänderungen
- [ ] Optimierung der Farbauswahl-Performance bei großen Transkriptionen
- [ ] Erwägung der Implementierung von Farbthemen oder Voreinstellungen für schnelle Anpassungen

## Abgeschlossen
- [x] Überprüfung und Optimierung der Speichernutzung, insbesondere bei der Verarbeitung großer Audioaufnahmen
- [x] Implementierung einer Funktion zum Zurücksetzen der Einstellungen auf Standardwerte
- [x] Implementierung robusterer Fehlerbehandlung in allen Modulen
- [x] Implementierung von Vorschau-Funktionalität für Farbänderungen
- [x] Beheben der DeprecationWarnings für `unittest.makeSuite()` durch Umstellung auf `unittest.TestLoader.loadTestsFromTestCase()`
- [x] Erweiterung der Fehlerprotokolle für detailliertere Diagnosen bei Transkriptionsproblemen
- [x] Implementierung zusätzlicher Tests für die neue Audiovorverarbeitungslogik
- [x] Implementierung von Unit-Tests für jedes neue Modul zur Verbesserung der Codequalität und Wartbarkeit
- [x] Optimierung der Theme-Auswahl und -Anwendung im Kontext von Openbox Einstellungen und Linux MATE-Themes
- [x] Implementieren einer robusteren Methode zur Speicherung und Wiederherstellung der Fensterposition
- [x] Optimieren der Häufigkeit der Einstellungsspeicherung
- [x] Verbessern der Fehlerbehandlung beim Laden der Einstellungen
- [x] Optimieren des Modellwechsels
- [x] Aktualisieren der Benutzerdokumentation für neue Funktionen

## Zukünftige Überlegungen
- [ ] Mögliche Einführung von asyncio für verbesserte Nebenläufigkeit, insbesondere bei der Audioaufnahme und -verarbeitung
- [ ] Berücksichtigung von Mehrbildschirm-Setups bei der Fensterpositionierung
- [ ] Implementierung einer Mindestgröße für das Fenster
- [ ] Untersuchung der Möglichkeit, verschiedene Audiocodecs zu unterstützen
- [ ] Evaluierung alternativer Spracherkennungsmodelle für mögliche zukünftige Integration
