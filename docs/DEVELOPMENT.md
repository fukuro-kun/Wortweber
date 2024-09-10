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
