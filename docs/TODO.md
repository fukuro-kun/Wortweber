# TODO Liste für Wortweber

## Dringendes
- [x] Das initiale Ausgrauen der Verzögerungs-Optionen, wenn Eingabemodus="Ins Textfenster" implementieren

## Priorität Hoch
- [x] Refactoring hinsichtlich aller Standardeinstellungen, welche als Variablen in config.py zu hinterlegen sind
- [ ] Verbesserung der Shortcut-Funktionalität (Manuelle Einstellung, Erfassung, Zuverlässigkeit)
- [ ] Implementierung von Unit-Tests für jedes neue Modul zur Verbesserung der Codequalität und Wartbarkeit
- [x] Implementierung einer Testaufnahme-Funktion für Entwicklungs- und Debugging-Zwecke
- [ ] Optimierung der Theme-Auswahl und -Anwendung im Kontext von Openbox Einstellungen und Linux MATE-Themes

## Priorität Mittel
- [ ] Implementierung zusätzlicher Module für die Ausgabe (z.B. Ollama-Unterstützung)
- [ ] Erweiterung der Testabdeckung, insbesondere für kritische Funktionen
- [ ] Einrichtung einer Staging-Umgebung für gründlichere Tests vor Veröffentlichungen
- [ ] Entwicklung eines klaren Rollback-Plans für problematische Releases
- [ ] Implementierung robusterer Fehlerbehandlung in allen Modulen

## Priorität Niedrig
- [ ] Internationalisierung der Anwendung mittels einfacher Module in Form von String-Dateien
- [ ] Implementierung eines Plugin-Systems basierend auf der neuen modularen Struktur
- [ ] Untersuchung möglicher Performance-Probleme beim Laden großer Transkriptionen
- [ ] Hinzufügen von Tooltips für verschiedene Optionen in der GUI

## Kontinuierliche Verbesserungen
- [ ] Regelmäßige Code-Reviews durchführen
- [ ] Aktualisieren der Abhängigkeiten auf die neuesten stabilen Versionen
- [ ] Verbesserte Dokumentation zur neuen Struktur der Textoperationen im Backend
- [ ] Detailliertere Dokumentation von Änderungen und deren erwarteten Auswirkungen

## Abgeschlossen
- [x] Implementieren einer robusteren Methode zur Speicherung und Wiederherstellung der Fensterposition
- [x] Optimieren der Häufigkeit der Einstellungsspeicherung
- [x] Verbessern der Fehlerbehandlung beim Laden der Einstellungen
- [x] Optimieren des Modellwechsels
- [x] Aktualisieren der Benutzerdokumentation für neue Funktionen

## Zukünftige Überlegungen
- [ ] Mögliche Einführung von asyncio für verbesserte Nebenläufigkeit, insbesondere bei der Audioaufnahme und -verarbeitung
- [ ] Berücksichtigung von Mehrbildschirm-Setups bei der Fensterpositionierung
- [ ] Implementierung einer Mindestgröße für das Fenster
- [ ] Implementieren einer Funktion zum Zurücksetzen der Einstellungen auf Standardwerte
