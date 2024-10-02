# 14. Glossar

Dieses Glossar bietet Definitionen und Erklärungen für wichtige Begriffe und Konzepte, die in der Wortweber Plugin-Entwicklung verwendet werden.

## A

### AbstractPlugin
Die Basisklasse, von der alle Wortweber-Plugins erben müssen. Sie definiert die grundlegende Struktur und Schnittstelle für Plugins.

### Aktivierung (Plugin)
Der Prozess, bei dem ein Plugin in den aktiven Zustand versetzt und zur Verwendung bereitgestellt wird.

### API (Application Programming Interface)
Eine Schnittstelle, die es Plugins ermöglicht, mit der Hauptanwendung zu interagieren. Sie definiert die Methoden und Datenstrukturen für die Kommunikation zwischen Plugins und Wortweber.

### Asynchrone Operationen
Programmierparadigma, bei dem bestimmte Aufgaben unabhängig vom Hauptprogrammfluss ausgeführt werden, um die Reaktionsfähigkeit der Anwendung zu verbessern.

## D

### Deaktivierung (Plugin)
Der Vorgang, bei dem ein aktives Plugin in einen inaktiven Zustand versetzt wird, wodurch seine Funktionalität vorübergehend ausgesetzt wird.

### Dependency Injection
Ein Entwurfsmuster, bei dem Abhängigkeiten einer Klasse von außen injiziert werden. Wird in Wortweber verwendet, um lose Kopplung zwischen Komponenten zu erreichen.

### Docstring
Ein Dokumentations-String in Python, der die Funktionalität einer Klasse, Methode oder Funktion beschreibt. In Wortweber werden Docstrings verwendet, um Plugins und ihre Komponenten zu dokumentieren.

## E

### Einstellungsverwaltung
Der Prozess und die Mechanismen zur Verwaltung von Plugin-spezifischen Konfigurationen und Benutzereinstellungen.

### Event-System
Ein Mechanismus in Wortweber, der es Plugins ermöglicht, auf bestimmte Ereignisse zu reagieren und eigene Ereignisse auszulösen.

## H

### Hook
Ein definierter Punkt in der Hauptanwendung, an dem Plugins ihre Funktionalität einhängen können. Hooks ermöglichen es Plugins, die Funktionalität von Wortweber an bestimmten Stellen zu erweitern oder zu modifizieren.

## I

### Incognito-Modus
Ein Betriebsmodus, der erhöhten Datenschutz bietet, indem bestimmte Daten nicht gespeichert oder protokolliert werden.

## L

### Lazy Loading
Eine Optimierungstechnik, bei der Ressourcen erst dann geladen werden, wenn sie tatsächlich benötigt werden.

### LLM (Large Language Model)
Ein KI-Modell, das auf der Verarbeitung und Generierung natürlicher Sprache spezialisiert ist.

## M

### Metadaten (Plugin)
Beschreibende Informationen über ein Plugin, wie Name, Version, Autor und Beschreibung. Diese Informationen werden für die Verwaltung und Anzeige von Plugins in Wortweber verwendet.

## P

### Plugin
Eine Softwarekomponente, die die Funktionalität von Wortweber erweitert. Muss von AbstractPlugin erben und definierte Schnittstellen implementieren.

### Plugin-Lebenszyklus
Die verschiedenen Stadien, die ein Plugin durchläuft, von der Entdeckung über die Aktivierung bis hin zur Deaktivierung und Entladung.

### PluginLoader
Eine Klasse, die für das dynamische Laden von Plugin-Modulen verantwortlich ist.

### PluginManager
Die zentrale Klasse zur Verwaltung von Plugins in Wortweber. Verantwortlich für das Laden, Aktivieren, Deaktivieren und Koordinieren von Plugins.

## R

### Reflection
Die Fähigkeit eines Programms, seine eigene Struktur zu untersuchen und zu modifizieren. In Wortweber wird Reflection für die dynamische Plugin-Verwaltung und -Konfiguration genutzt.

### RLock
Ein wiedereintrittsfähiges Lock (Reentrant Lock) in Python, das für verbesserte Thread-Sicherheit im Einstellungsmanagement von Wortweber verwendet wird. Es erlaubt demselben Thread, ein Lock mehrmals zu erwerben, ohne sich selbst zu blockieren, was besonders nützlich für verschachtelte Aufrufe innerhalb des SettingsManagers ist.

## S

### Sandbox
Eine isolierte Umgebung, in der Plugins ausgeführt werden, um die Sicherheit zu erhöhen und unbeabsichtigte Interaktionen mit dem Hauptsystem zu verhindern.

### Serialisierung
Der Prozess der Umwandlung von Objekten in ein Format, das gespeichert oder übertragen werden kann. Wichtig für die Persistenz von Plugin-Daten und -Einstellungen.

## T

### Thread-Sicherheit
DDie Eigenschaft einer Softwarekomponente, korrekt zu funktionieren, wenn sie von mehreren Threads gleichzeitig verwendet wird. In Wortweber wird dies im Einstellungsmanagement durch die Verwendung von RLock gewährleistet, was eine sichere gleichzeitige Zugriffe und Änderungen von Einstellungen ermöglicht.

### Type Hinting
Die Praxis, Typinformationen zu Variablen, Funktionsparametern und Rückgabewerten hinzuzufügen. Verbessert die Lesbarkeit und ermöglicht statische Typüberprüfungen.

## V

### Verzögerte Speicherung
Ein Mechanismus im Einstellungsmanagement von Wortweber, der das Speichern von Einstellungen für eine kurze Zeit verzögert. Dies optimiert die Performanz bei häufigen Einstellungsänderungen, indem es mehrere Änderungen zu einem einzelnen Speichervorgang zusammenfasst.

## W

### Wortweber-Core
Der zentrale Teil der Wortweber-Anwendung, der die grundlegende Funktionalität bereitstellt und die Integration von Plugins ermöglicht.
```

Dieses Glossar bietet eine umfassende Übersicht über die wichtigsten Begriffe und Konzepte, die in der Wortweber Plugin-Entwicklung verwendet werden. Es dient als Nachschlagewerk für Entwickler, um schnell Definitionen und Erklärungen für spezifische Terme zu finden.
