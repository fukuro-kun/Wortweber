# Wortweber - Echtzeit-Sprachtranskription mit KI
# Copyright (C) 2024 fukuro-kun
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# Standardbibliotheken
import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, List
import json

# Drittanbieterbibliotheken
import requests

# Projektspezifische Module
from src.plugin_system.plugin_interface import AbstractPlugin
from src.plugin_system.event_system import EventSystem
from src.utils.error_handling import handle_exceptions, logger

class OllamaLLMChatPlugin(AbstractPlugin):
    """
    Ein Plugin für den Chat mit einem von Ollama gehosteten LLM.

    Dieses Plugin ermöglicht die Interaktion mit einem Large Language Model (LLM),
    das von Ollama gehostet wird, über eine grafische Benutzeroberfläche.
    """

    def __init__(self):
        """Initialisiert das OllamaLLMChatPlugin mit Standardwerten."""
        self._name = "Ollama LLM Chat Plugin"
        self._version = "1.0.1"
        self._description = "Ein Plugin für den Chat mit einem von Ollama gehosteten LLM"
        self._author = "Wortweber-Entwickler"
        self._chat_window = None
        self._chat_display = None
        self._input_text = None
        self._chat_history = []
        self._system_message = "Du bist ein hilfreicher Assistent."
        self._llm_model = "llama3.1:8b-instruct-q6_K"
        self._ollama_base_url = "http://localhost:11434"
        self._ollama_chat_endpoint = "/api/chat"
        self._ollama_tags_endpoint = "/api/tags"

    @property
    def name(self) -> str:
        """Gibt den Namen des Plugins zurück."""
        return self._name

    @property
    def version(self) -> str:
        """Gibt die Version des Plugins zurück."""
        return self._version

    @property
    def description(self) -> str:
        """Gibt die Beschreibung des Plugins zurück."""
        return self._description

    @property
    def author(self) -> str:
        """Gibt den Autor des Plugins zurück."""
        return self._author

    def activate(self, settings: Dict[str, Any]) -> None:
        """
        Aktiviert das Plugin mit den gegebenen Einstellungen.

        Args:
            settings (Dict[str, Any]): Ein Dictionary mit Plugin-Einstellungen.
        """
        self._system_message = settings.get('system_message', self._system_message)
        self._llm_model = settings.get('llm_model', self._llm_model)
        self._ollama_base_url = settings.get('ollama_base_url', self._ollama_base_url)

    def deactivate(self) -> Optional[Dict[str, Any]]:
        """
        Deaktiviert das Plugin und gibt die aktuellen Einstellungen zurück.

        Returns:
            Optional[Dict[str, Any]]: Ein Dictionary mit den aktuellen Einstellungen oder None.
        """
        if self._chat_window:
            self._chat_window.destroy()
        return {
            'system_message': self._system_message,
            'llm_model': self._llm_model,
            'ollama_base_url': self._ollama_base_url
        }

    def process_text(self, text: str) -> str:
        """
        Verarbeitet den eingegebenen Text und fügt ihn ggf. in das Eingabefeld ein.

        Args:
            text (str): Der zu verarbeitende Text.

        Returns:
            str: Der verarbeitete Text.
        """
        if self._chat_window and self._input_text and self._input_text.focus_get() == self._input_text:
            self._input_text.insert(tk.END, text)
        return text

    def get_settings(self) -> Dict[str, Any]:
        """
        Gibt die aktuellen Einstellungen des Plugins zurück.

        Returns:
            Dict[str, Any]: Ein Dictionary mit den aktuellen Einstellungen.
        """
        return {
            'system_message': self._system_message,
            'llm_model': self._llm_model,
            'ollama_base_url': self._ollama_base_url
        }

    def set_settings(self, settings: Dict[str, Any]) -> None:
        """
        Setzt die Einstellungen des Plugins.

        Args:
            settings (Dict[str, Any]): Ein Dictionary mit den neuen Einstellungen.
        """
        self._system_message = settings.get('system_message', self._system_message)
        self._llm_model = settings.get('llm_model', self._llm_model)
        self._ollama_base_url = settings.get('ollama_base_url', self._ollama_base_url)
        logger.info(f"Einstellungen für {self.name} aktualisiert: {settings}")

    def get_menu_entries(self) -> List[Dict[str, Any]]:
        """
        Gibt die Menüeinträge für das Plugin zurück.

        Returns:
            List[Dict[str, Any]]: Eine Liste von Dictionaries, die Menüeinträge repräsentieren.
        """
        return [{
            'label': 'Ollama LLM Chat',
            'command': self.open_chat_window
        }]

    def get_ui_elements(self) -> Dict[str, Any]:
        """
        Gibt UI-Elemente für das Plugin zurück.

        Returns:
            Dict[str, Any]: Ein Dictionary mit UI-Elementen.
        """
        return {
            "buttons": [
                {
                    "text": "Ollama LLM Chat",
                    "command": self.open_chat_window
                }
            ]
        }

    def open_chat_window(self):
        """Öffnet das Chat-Fenster oder bringt es in den Vordergrund, wenn es bereits existiert."""
        if self._chat_window:
            self._chat_window.destroy()

        self._chat_window = tk.Toplevel()
        self._chat_window.title("Ollama LLM Chat")
        self._chat_window.geometry("600x400")

        # Verwenden Sie den gleichen Stil wie das Hauptfenster
        style = ttk.Style()
        bg_color = style.lookup('TFrame', 'background')
        fg_color = style.lookup('TLabel', 'foreground')

        self._chat_display = tk.Text(self._chat_window, wrap='word',
                                    bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self._chat_display.pack(expand=True, fill='both', padx=10, pady=10)

        input_frame = ttk.Frame(self._chat_window)
        input_frame.pack(fill='x', padx=10, pady=10)

        self._input_text = tk.Text(input_frame, height=3, wrap='word',
                                bg=bg_color, fg=fg_color, insertbackground=fg_color)
        self._input_text.pack(side='left', expand=True, fill='both')

        send_button = ttk.Button(input_frame, text="Senden", command=self.send_message)
        send_button.pack(side='right')

    @handle_exceptions
    def send_message(self):
        """Sendet die Nachricht aus dem Eingabefeld an das LLM und aktualisiert den Chat-Verlauf."""
        if self._input_text:
            user_message = self._input_text.get("1.0", tk.END).strip()
            if user_message:
                self.update_chat_display(f"\nUser: {user_message}\n")
                self._input_text.delete("1.0", tk.END)
                self.get_llm_response(user_message)

    @handle_exceptions
    def get_llm_response(self, user_message: str):
        """
        Holt die Antwort vom LLM und aktualisiert den Chat-Verlauf.

        Args:
            user_message (str): Die Nachricht des Benutzers.
        """
        if not self.test_api_connection():
            self.update_chat_display("Error: Keine Verbindung zur Ollama API möglich. Bitte überprüfen Sie Ihre Einstellungen und stellen Sie sicher, dass der Ollama-Dienst läuft.")
            return

        # Füge die Benutzernachricht zum Chatverlauf hinzu
        self._chat_history.append({"role": "user", "content": user_message})

        payload = {
            "model": self._llm_model,
            "messages": [{"role": "system", "content": self._system_message}] + self._chat_history,
            "stream": True
        }

        try:
            response = requests.post(f"{self._ollama_base_url}{self._ollama_chat_endpoint}", json=payload, stream=True, timeout=30)
            response.raise_for_status()

            self.update_chat_display("\nAssistant: ")
            full_response = ""
            for line in response.iter_lines():
                if line:
                    try:
                        json_response = json.loads(line)
                        if 'message' in json_response and 'content' in json_response['message']:
                            content = json_response['message']['content']
                            full_response += content
                            self.update_chat_display(content, append=True)
                    except json.JSONDecodeError:
                        logger.warning(f"Konnte Zeile nicht als JSON dekodieren: {line}")

            if full_response:
                # Füge die LLM-Antwort zum Chatverlauf hinzu
                self._chat_history.append({"role": "assistant", "content": full_response})
                self.update_chat_display("\n")  # Neue Zeile nach der Antwort
                logger.info(f"Vollständige Antwort erhalten, Länge: {len(full_response)} Zeichen")
            else:
                self.update_chat_display("Error: Keine lesbare Antwort vom LLM erhalten.")

        except requests.RequestException as e:
            error_message = f"Fehler bei der Verbindung zum LLM: {str(e)}"
            self.update_chat_display(f"Error: {error_message}")
            logger.error(error_message)

    @handle_exceptions
    def test_api_connection(self):
        """
        Testet die Verbindung zur Ollama API.

        Returns:
            bool: True, wenn die Verbindung erfolgreich ist, sonst False.
        """
        try:
            response = requests.get(f"{self._ollama_base_url}{self._ollama_tags_endpoint}", timeout=5)
            response.raise_for_status()
            logger.info("Ollama API-Verbindung erfolgreich getestet.")
            return True
        except requests.RequestException as e:
            logger.error(f"Fehler bei der Verbindung zur Ollama API: {str(e)}")
            return False

    @handle_exceptions
    def get_available_models(self):
        """
        Holt die Liste der verfügbaren Modelle von der Ollama API.

        Returns:
            List[str]: Eine Liste der verfügbaren Modellnamen oder eine leere Liste bei Fehlern.
        """
        try:
            response = requests.get(f"{self._ollama_base_url}{self._ollama_tags_endpoint}", timeout=5)
            response.raise_for_status()
            data = response.json()
            return [model['name'] for model in data.get('models', [])]
        except requests.RequestException as e:
            logger.error(f"Fehler beim Abrufen der verfügbaren Modelle: {str(e)}")
            return []

    def update_chat_display(self, message: str, append: bool = False):
        """
        Aktualisiert die Chat-Anzeige mit einer neuen Nachricht.

        Args:
            message (str): Die anzuzeigende Nachricht.
            append (bool): Wenn True, wird die Nachricht an die bestehende angehängt.
        """
        if self._chat_display:
            self._chat_display.config(state=tk.NORMAL)
            if append:
                self._chat_display.insert(tk.END, message)
            else:
                self._chat_display.insert(tk.END, message + "\n")
            self._chat_display.config(state=tk.DISABLED)
            self._chat_display.see(tk.END)

    def get_config_ui(self, parent: tk.Widget) -> ttk.Frame:
        """
        Erstellt und gibt die Konfigurationsoberfläche für das Plugin zurück.

        Args:
            parent (tk.Widget): Das übergeordnete Widget.

        Returns:
            ttk.Frame: Ein Frame mit Konfigurationselementen.
        """
        frame = ttk.Frame(parent)

        ttk.Label(frame, text="System Message:").pack(anchor='w')
        system_message_entry = ttk.Entry(frame, width=50)
        system_message_entry.insert(0, self._system_message)
        system_message_entry.pack(fill='x')

        ttk.Label(frame, text="LLM Model:").pack(anchor='w')
        llm_model_entry = ttk.Entry(frame)
        llm_model_entry.insert(0, self._llm_model)
        llm_model_entry.pack(fill='x')

        ttk.Label(frame, text="Ollama API Basis-URL:").pack(anchor='w')
        api_url_entry = ttk.Entry(frame)
        api_url_entry.insert(0, self._ollama_base_url)
        api_url_entry.pack(fill='x')

        def save_settings():
            self._system_message = system_message_entry.get()
            self._llm_model = llm_model_entry.get()
            self._ollama_base_url = api_url_entry.get()

        save_button = ttk.Button(frame, text="Einstellungen speichern", command=save_settings)
        save_button.pack(pady=10)

        return frame

    def register_events(self, event_system: EventSystem) -> None:
        """
        Registriert Event-Listener für das Plugin.

        Args:
            event_system (EventSystem): Das Event-System der Anwendung.
        """
        event_system.add_listener("text_transcribed", self.on_text_transcribed)

    def on_text_transcribed(self, text: str) -> None:
        """
        Wird aufgerufen, wenn neuer Text transkribiert wurde.

        Args:
            text (str): Der transkribierte Text.
        """
        self.process_text(text)

# Zusätzliche Erklärungen:

# 1. Chatverlauf:
#    Der Chatverlauf wird nun in self._chat_history gespeichert und bei jeder Anfrage
#    an das LLM gesendet. Dies ermöglicht es dem Modell, auf vorherige Nachrichten
#    Bezug zu nehmen und den Kontext der Unterhaltung zu berücksichtigen.

# 2. Formatierung der Chat-Anzeige:
#    Die update_chat_display Methode wurde angepasst, um eine klare Trennung zwischen
#    Benutzer- und Assistenten-Nachrichten zu gewährleisten. Jede Nachricht beginnt in
#    einer neuen Zeile, was die Lesbarkeit verbessert.

# 3. Streaming-Verarbeitung:
#    Die get_llm_response Methode verarbeitet die API-Antwort als Stream, was eine
#    flüssigere und reaktionsschnellere Benutzererfahrung ermöglicht.

# 4. Fehlerbehandlung:
#    Es wurden zusätzliche Fehlerprüfungen und Logging-Anweisungen hinzugefügt, um
#    potenzielle Probleme bei der API-Kommunikation besser diagnostizieren zu können.

# 5. Konfigurationsoberfläche:
#    Die get_config_ui Methode bietet eine einfache Möglichkeit, die Plugin-Einstellungen
#    anzupassen, einschließlich des System-Messages, des verwendeten Modells und der API-URL.

# 6. URL-Struktur:
#    Die URL-Struktur wurde überarbeitet, um eine klare Trennung zwischen Basis-URL und
#    spezifischen Endpunkten zu ermöglichen. Dies verbessert die Flexibilität und
#    reduziert die Fehleranfälligkeit bei API-Anfragen.

# Diese Implementierung bietet eine robuste und benutzerfreundliche Schnittstelle für
# die Interaktion mit dem Ollama-LLM, während sie die Projektrichtlinien für Stil und
# Dokumentation einhält.
