# TODO Liste für Wortweber

## Kernfunktionen
### Hohe Priorität
- [ ] Durchführung umfassender Tests für die neue Shortcut-Funktionalität
- [ ] Überprüfung und Optimierung der Gerätekompatibilität für verschiedene Systemkonfigurationen
- [ ] Durchführung umfassender Tests für die Zahlwort-Konvertierungsfunktionalität
- [x] Entwicklung einer detaillierten API-Dokumentation für Plugin-Entwickler

### Mittlere Priorität
- [ ] Implementierung umfassender Tests für das überarbeitete Plugin-System
- [ ] Optimieren der Effizienz der Zahlwortverarbeitung für sehr große Zahlen
- [ ] Implementierung zusätzlicher Module für die Ausgabe (z.B. Ollama-Unterstützung)
- [ ] Überprüfen und ggf. Verbessern der Fehlerbehandlung in der TextProcessor-Klasse

### Niedrige Priorität
- [ ] Implementierung eines Mechanismus zur Überprüfung von Plugin-Abhängigkeiten
- [ ] Entwicklung zusätzlicher Beispiel-Plugins zur Demonstration der Systemfähigkeiten
- [ ] Untersuchung der Unterstützung verschiedener Audiocodecs
- [ ] Evaluierung alternativer Spracherkennungsmodelle für zukünftige Integration
- [ ] Implementierung eines Plugin-Systems

## Benutzeroberfläche und Bedienung
### Hohe Priorität
- [ ] Implementierung von Unit-Tests für die Incognito-Modus-Funktionalität
- [ ] Überprüfung der Kompatibilität mit verschiedenen Eingabeformaten
- [ ] Entwicklung eines Plans für regelmäßige manuelle UI-Tests

### Mittlere Priorität
- [ ] Implementierung eines Internationalisierungssystems für zukünftige Mehrsprachigkeit
- [ ] Erstellung einer detaillierten Dokumentation für den Incognito-Modus
- [ ] Verbesserung der Benutzerführung durch Tooltips und erweiterte Einstellungsmöglichkeiten

### Niedrige Priorität
- [ ] Anpassungen für Mehrbildschirm-Setups
- [ ] Implementierung einer Mindestfenstergröße
- [ ] Implementierung von Funktionen zum Zurücksetzen von Einstellungen, einschließlich Farbeinstellungen

## Qualitätssicherung und Dokumentation
### Hohe Priorität
- [ ] Überprüfung und Verbesserung der Testabdeckung
- [ ] Erweiterung der Typ-Annotationen auf alle Teile des Codes
- [ ] Entwicklung eines Konzepts für konsistente Namenskonventionen

### Mittlere Priorität
- [ ] Umfassende Erweiterung der Testabdeckung für kritische Funktionen und UI-Komponenten
- [ ] Einrichtung einer Staging-Umgebung und Entwicklung eines Rollback-Plans für Releases
- [ ] Überprüfung und Optimierung der Importstruktur in allen Dateien

### Kontinuierliche Verbesserungen
- [ ] Durchführung regelmäßiger Code-Reviews und Aktualisierung von Abhängigkeiten
- [ ] Verbesserung der Dokumentation, insbesondere für Textoperationen
- [ ] Regelmäßige Überprüfung und Aktualisierung von Code-Kommentaren

## Erweiterungen und Optimierungen
### Hohe Priorität
- [ ] Optimierung des Ressourcenmanagements in kritischen Komponenten
- [ ] Überprüfung und Zentralisierung von hartcodierten Werten in der Konfigurationsdatei
- [ ] Optimierung der Testausführung, einschließlich Parallelisierung

### Mittlere Priorität
- [ ] Evaluierung von asyncio für verbesserte Nebenläufigkeit in der Audioverarbeitung
- [ ] Implementierung von Unit-Tests für neue Komponenten wie `wortweber.sh`
- [ ] Untersuchung von Performance-Problemen im Plugin-System

## Agentenbasierte Funktionen
- [ ] Entwicklung des Single-Agent-Systems (KI-Modell mit Bash-Zugang)
