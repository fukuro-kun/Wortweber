# Wortweber Plugin-System Dokumentation

## Inhaltsverzeichnis

1. [Einführung](#1-einführung)
2. [Architektur des Plugin-Systems](#2-architektur-des-plugin-systems)
3. [Entwicklung von Plugins](#3-entwicklung-von-plugins)
4. [Plugin-Schnittstelle](#4-plugin-schnittstelle)
5. [Plugin-Lebenszyklus](#5-plugin-lebenszyklus)
6. [Einstellungsverwaltung für Plugins](#6-einstellungsverwaltung-für-plugins)
7. [Plugin-Verwaltung in der Benutzeroberfläche](#7-plugin-verwaltung-in-der-benutzeroberfläche)
8. [Sicherheitsüberlegungen](#8-sicherheitsüberlegungen)
9. [Best Practices](#9-best-practices)
10. [Fehlerbehebung](#10-fehlerbehebung)
11. [API-Referenz](#11-api-referenz)

## 1. Einführung

Das Wortweber Plugin-System ermöglicht es Entwicklern, die Funktionalität der Anwendung durch benutzerdefinierte Plugins zu erweitern. Diese Dokumentation bietet einen umfassenden Überblick über die Architektur, Entwicklung und Verwaltung von Plugins innerhalb des Wortweber-Ökosystems.

## 2. Architektur des Plugin-Systems

Das Plugin-System von Wortweber basiert auf einer modularen Architektur, die aus folgenden Hauptkomponenten besteht:

- `PluginManager`: Zentrale Klasse zur Verwaltung von Plugins
- `PluginLoader`: Verantwortlich für das dynamische Laden von Plugin-Modulen
- `AbstractPlugin`: Basisklasse, die von allen Plugins implementiert werden muss
- `SettingsManager`: Verwaltet plugin-spezifische Einstellungen

### Schlüsselkonzepte:

- **Dynamisches Laden**: Plugins werden zur Laufzeit geladen, ohne dass die Hauptanwendung neu kompiliert werden muss.
- **Statusverwaltung**: Unterscheidung zwischen aktiven Plugins (in der laufenden Sitzung) und für den Start aktivierten Plugins (beim nächsten Anwendungsstart).
- **Einstellungspersistenz**: Plugin-spezifische Einstellungen werden über Sitzungen hinweg gespeichert.

## 3. Entwicklung von Plugins

Um ein Plugin für Wortweber zu entwickeln, folgen Sie diesen Schritten:

1. Erstellen Sie eine neue Python-Datei im `plugins`-Verzeichnis.
2. Importieren Sie die erforderlichen Module:
   ```python
   from src.plugin_system.plugin_interface import AbstractPlugin
   ```
3. Definieren Sie eine Klasse, die von `AbstractPlugin` erbt:
   ```python
   class MyPlugin(AbstractPlugin):
       def __init__(self):
           self.name = "Mein Plugin"
           self.version = "1.0.0"
           self.description = "Beschreibung meines Plugins"
           self.author = "Ihr Name"
   ```
4. Implementieren Sie die erforderlichen Methoden (siehe [Plugin-Schnittstelle](#4-plugin-schnittstelle)).

## 4. Plugin-Schnittstelle

Jedes Plugin muss die `AbstractPlugin`-Schnittstelle implementieren. Hier sind die wichtigsten Methoden:

- `activate(self, settings: Dict[str, Any]) -> None`: Wird aufgerufen, wenn das Plugin aktiviert wird.
- `deactivate(self) -> Optional[Dict[str, Any]]`: Wird aufgerufen, wenn das Plugin deaktiviert wird.
- `process_text(self, text: str) -> str`: Hauptmethode zur Textverarbeitung.
- `get_settings(self) -> Dict[str, Any]`: Gibt die aktuellen Plugin-Einstellungen zurück.
- `set_settings(self, settings: Dict[str, Any]) -> None`: Setzt neue Plugin-Einstellungen.

## 5. Plugin-Lebenszyklus

1. **Entdeckung**: Der `PluginManager` scannt das `plugins`-Verzeichnis beim Start der Anwendung.
2. **Laden**: Plugins werden durch den `PluginLoader` dynamisch geladen.
3. **Aktivierung**: Plugins können über die Benutzeroberfläche oder programmatisch aktiviert werden.
4. **Ausführung**: Aktive Plugins verarbeiten Text durch ihre `process_text`-Methode.
5. **Deaktivierung**: Plugins können deaktiviert werden, wobei ihre Ressourcen freigegeben werden.
6. **Entladen**: Beim Beenden der Anwendung werden alle Plugins ordnungsgemäß entladen.

## 6. Einstellungsverwaltung für Plugins

Plugins können eigene Einstellungen definieren und verwalten:

- Definieren Sie Standardeinstellungen in der `get_default_settings`-Methode.
- Verwenden Sie `get_settings` und `set_settings` zur Laufzeit.
- Der `SettingsManager` speichert plugin-spezifische Einstellungen persistent.

Beispiel:
```python
def get_default_settings(self) -> Dict[str, Any]:
    return {"option1": True, "option2": "default"}

def get_settings(self) -> Dict[str, Any]:
    return self._settings

def set_settings(self, settings: Dict[str, Any]) -> None:
    self._settings.update(settings)
```

## 7. Plugin-Verwaltung in der Benutzeroberfläche

Wortweber bietet eine grafische Benutzeroberfläche zur Plugin-Verwaltung:

- Aktivieren/Deaktivieren von Plugins
- Konfiguration von Plugin-Einstellungen
- Anzeige von Plugin-Informationen (Name, Version, Autor)

Die `PluginManagementWindow`-Klasse implementiert diese Funktionalität.

## 8. Sicherheitsüberlegungen

- Plugins werden in einer kontrollierten Umgebung ausgeführt.
- Implementieren Sie Überprüfungen für bösartigen oder fehlerhaften Code.
- Begrenzen Sie den Zugriff von Plugins auf kritische Systemressourcen.

## 9. Best Practices

- Folgen Sie dem Prinzip der geringsten Berechtigung.
- Dokumentieren Sie Ihr Plugin gründlich.
- Behandeln Sie Fehler angemessen und geben Sie hilfreiche Fehlermeldungen zurück.
- Testen Sie Ihr Plugin gründlich vor der Verteilung.

## 10. Fehlerbehebung

Häufige Probleme und Lösungen:

- Plugin wird nicht erkannt: Überprüfen Sie den Dateinamen und die Klassenstruktur.
- Aktivierungsfehler: Stellen Sie sicher, dass alle erforderlichen Methoden implementiert sind.
- Einstellungsprobleme: Überprüfen Sie die Datentypen und Strukturen der Einstellungen.

## 11. API-Referenz

Detaillierte Beschreibung aller relevanten Klassen und Methoden:

### PluginManager

- `discover_plugins()`: Scannt das Plugin-Verzeichnis und lädt verfügbare Plugins.
- `activate_plugin(plugin_name: str) -> bool`: Aktiviert ein spezifisches Plugin.
- `deactivate_plugin(plugin_name: str) -> bool`: Deaktiviert ein spezifisches Plugin.
- `process_text_with_plugins(text: str) -> str`: Verarbeitet Text mit allen aktiven Plugins.

### PluginLoader

- `load_plugin(plugin_name: str, settings: Optional[Dict[str, Any]] = None) -> Optional[AbstractPlugin]`: Lädt ein einzelnes Plugin.
- `load_all_plugins(settings: Optional[Dict[str, Dict[str, Any]]] = None) -> List[AbstractPlugin]`: Lädt alle verfügbaren Plugins.

### AbstractPlugin

- `name: str`: Name des Plugins
- `version: str`: Version des Plugins
- `description: str`: Beschreibung des Plugins
- `author: str`: Autor des Plugins
- `activate(settings: Dict[str, Any]) -> None`: Aktiviert das Plugin
- `deactivate() -> Optional[Dict[str, Any]]`: Deaktiviert das Plugin
- `process_text(text: str) -> str`: Verarbeitet Text
- `get_settings() -> Dict[str, Any]`: Gibt die aktuellen Einstellungen zurück
- `set_settings(settings: Dict[str, Any]) -> None`: Setzt neue Einstellungen
