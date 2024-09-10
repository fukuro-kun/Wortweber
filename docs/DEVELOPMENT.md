## Chunk-weise Verarbeitung und Echtzeittranskription (Experimentell)

Die Implementierung der Chunk-weisen Verarbeitung und Echtzeittranskription war ein experimenteller Ansatz, der letztendlich nicht wie erwartet funktionierte und daher nicht in den Hauptentwicklungszweig integriert wurde.

Hauptmerkmale des Versuchs:
1. Dynamische Anpassung der Chunk-Größe basierend auf erkannten Sprechpausen.
2. Echtzeitverarbeitung der Audiodaten für sofortige Transkription.
3. Implementierung von Sprachauswahl und optionaler Zahlennormalisierung.

Unüberwindbare Probleme:
- Wiederholungen in der Transkription: Die Chunk-weise Verarbeitung führte zu häufigen Wiederholungen von bereits transkribiertem Text.
- Inkonsistente Ergebnisse: Die Qualität der Transkription variierte stark zwischen verschiedenen Chunks.
- Erhöhte Komplexität: Der Ansatz erhöhte die Komplexität des Systems, ohne die erwarteten Vorteile zu liefern.

Relevante Commits:
- 3c1339e: Initiale Implementierung der Pausenerkennung und dynamischen Chunk-Erstellung
- ddeff46, f32bcbb, b0e8adc: Versuche, die Robustheit der Pausenerkennung zu verbessern
- ed6015e: Hinzufügung von Sprachauswahl und Zahlennormalisierung

Dieser Entwicklungszweig wird nicht weiter aktiv verfolgt, bleibt aber als Referenz und für mögliche zukünftige Überarbeitungen erhalten.
