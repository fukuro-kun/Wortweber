# TODO Liste für Wortweber

## Dringend
- [ ] Beheben der Typ-Inkonsistenz in wortweber_backend.py bei der Verarbeitung von audio_resampled.
- [ ] Refactoring hinsichtlich aller Standardeinstellungen, welche als Variablen in config.py zu hinterlegen sind.

## Benutzeroberfläche und Benutzererfahrung
- [ ] Implementieren von Mouseover-Hints für alle Flächen in der GUI, die nach 2-3 Sekunden aufpoppen und Funktionen erklären.
- [ ] Hinzufügen einer detaillierten Erklärung zur Auswahl und Bedeutung der verschiedenen Whisper-Modelle (tiny, base, small, medium, large) in der Benutzerdokumentation und als Mouseover-Hint im Modell-Auswahlmenü.
- [ ] Optimierung der Theme-Auswahl und -Anwendung im Kontext von Openbox-Einstellungen und Linux MATE-Themes.
- [ ] Verbesserung der Zuverlässigkeit bei der Wiederherstellung der Fensterposition und -größe.

## Funktionserweiterungen
- [ ] Implementierung zusätzlicher Module für die Ausgabe (z.B. Ollama-Unterstützung).
- [ ] Verbesserung der Shortcut-Funktionalität (Manuelle Einstellung, Erfassung, Zuverlässigkeit).

## Codequalität und Wartung
- [ ] Überprüfen und aktualisieren der Versionsangaben in requirements.txt. Erwägen Sie die Verwendung von Versionsbereichen für bessere langfristige Kompatibilität.
- [ ] Überarbeiten und aktualisieren der Tests, insbesondere test_audio_processor.py, um sie mit der aktuellen Implementierung in Einklang zu bringen.
- [ ] Erweiterung der Testabdeckung für neu hinzugefügte Funktionen und Module.
- [ ] Implementierung robusterer Fehlerbehandlung.

## Dokumentation
- [ ] Erklären Sie in der Entwicklerdokumentation (DEVELOPMENT.md), warum sowohl tkinter als auch ttkthemes verwendet werden und welche Vorteile dies bietet.

## Internationalisierung
- [ ] Vorbereitung der Anwendung für zukünftige Mehrsprachigkeit durch Auslagern aller Zeichenketten in separate Ressourcendateien.
