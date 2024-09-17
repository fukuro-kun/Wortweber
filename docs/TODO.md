# TODO Liste für Wortweber

## Dringendes
- [ ] Überprüfung und Optimierung der Gerätekompatibilität für verschiedene Systemkonfigurationen, einschließlich Verbesserung der Shortcut-Funktionalität

## Priorität Hoch
- [ ] Durchführung umfassender Tests für die neue Zahlwort-Konvertierungsfunktionalität
- [ ] Implementierung von Unit-Tests für die neue Zahlwort-Konvertierungsfunktionalität
- [ ] Überprüfung der Kompatibilität mit verschiedenen Eingabeformaten (z.B. gemischte Text- und Zahleneingaben)
- [ ] Überprüfung und Verbesserung der Testabdeckung
- [ ] Erweiterung der Typ-Annotationen auf alle Teile des Codes und Entwicklung eines Konzepts für konsistente Namenskonventionen
- [ ] Implementierung von Unit-Tests für die neue Incognito-Modus-Funktionalität
- [ ] Durchführung umfassender Tests für die neue Zahlwort-Konvertierungsfunktionalität

## Priorität Mittel
- [ ] Implementieren umfangreicher Tests für die neue Zahlwortverarbeitungslogik
- [ ] Optimieren der Effizienz der Zahlwortverarbeitung für sehr große Zahlen
- [ ] Erweiterung der Dokumentation zur detaillierten Erklärung der Zahlwortverarbeitungslogik
- [ ] Implementierung zusätzlicher Module für die Ausgabe (z.B. Ollama-Unterstützung)
- [ ] Umfassende Erweiterung der Testabdeckung, insbesondere für kritische Funktionen, UI-Komponenten, Optionsfenster, Farbverwaltung und neue Kontextmanager-Funktionalität
- [ ] Einrichtung einer Staging-Umgebung und Entwicklung eines Rollback-Plans für Releases
- [ ] Überprüfung und Optimierung der Importstruktur in allen Dateien
- [ ] Implementierung eines Internationalisierungssystems für zukünftige Mehrsprachigkeit
- [ ] Erstellung einer detaillierten Dokumentation für Benutzer über die Funktionsweise und Grenzen des Incognito-Modus
- [ ] Entwicklung eines Plans für regelmäßige manuelle UI-Tests

## Priorität Niedrig
- [ ] Überprüfen und ggf. Verbessern der Fehlerbehandlung in der TextProcessor-Klasse
- [ ] Implementierung eines Plugin-Systems und Untersuchung von Performance-Problemen
- [ ] Verbesserung der Benutzerführung durch Tooltips und erweiterte Einstellungsmöglichkeiten
- [ ] Optimierung der Testausführung, einschließlich Parallelisierung und ALSA-Warnungsunterdrückung
- [ ] Implementierung von Unit-Tests für neue Komponenten wie `wortweber.sh`

## Kontinuierliche Verbesserungen
- [ ] Durchführung regelmäßiger Code-Reviews und Aktualisierung von Abhängigkeiten
- [ ] Verbesserung der Dokumentation, insbesondere für Textoperationen und erwartete Änderungsauswirkungen
- [ ] Regelmäßige Überprüfung und Aktualisierung von Code-Kommentaren
- [ ] Optimierung des Ressourcenmanagements in kritischen Komponenten

## Neue Aufgaben
- [ ] Implementierung von Funktionen zum Zurücksetzen von Einstellungen, einschließlich Farbeinstellungen
- [ ] Entwicklung von Farbthemen oder Voreinstellungen für schnelle Anpassungen
- [ ] Überprüfung und Zentralisierung von hartcodierten Werten in der Konfigurationsdatei

## Zukünftige Überlegungen
- [ ] Evaluierung von asyncio für verbesserte Nebenläufigkeit in der Audioverarbeitung
- [ ] Anpassungen für Mehrbildschirm-Setups und Implementierung einer Mindestfenstergröße
- [ ] Untersuchung der Unterstützung verschiedener Audiocodecs
- [ ] Evaluierung alternativer Spracherkennungsmodelle für zukünftige Integration


## Abgeschlossene Aufgaben
- [x] Verbessern der Zahlwort-zu-Ziffer-Konvertierung für komplexe deutsche Zahlwörter
- [x] Sicherstellen, dass Nicht-Zahlwörter im verarbeiteten Text korrekt beibehalten werden
- [x] Wiederherstellung und Verbesserung der Textumwandlungen für Ziffern und Zahlwörter
- [x] Überprüfung und Optimierung der GUI-Tests
