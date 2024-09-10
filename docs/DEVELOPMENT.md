## Git-Workflow Best Practices

1. Vor jeder Operation den aktuellen Status und Branch prüfen:
   ```
   git status
   git branch
   ```

2. Vor dem Beginn neuer Entwicklungen sicherstellen, dass der lokale Branch aktuell ist:
   ```
   git pull origin [branch-name]
   ```

3. Regelmäßig den Status der Änderungen überprüfen:
   ```
   git status
   ```

4. Nach jedem Merge oder Branch-Wechsel den aktiven Branch verifizieren:
   ```
   git branch
   ```

5. Vor dem Push zum Remote-Repository den finalen Status prüfen:
   ```
   git status
   ```

Diese Schritte helfen, versehentliche Änderungen im falschen Branch oder unbeabsichtigte Merges zu vermeiden.


## Experimenteller Code

Ein experimenteller Ansatz zur chunk-weisen Verarbeitung wurde in der Datei `src/whisper_push_to_talk_dev.py` implementiert.
Dieser Code wurde aus dem aktiven Entwicklungszweig entfernt, ist aber in der Git-Historie verfügbar.
Um den Code einzusehen oder wiederherzustellen, kann folgender Befehl verwendet werden:

```bash
git show 4dfd1b0ac4998e306fc97c35e6c3abb9fbd71b0c:src/whisper_push_to_talk_dev.py
```
