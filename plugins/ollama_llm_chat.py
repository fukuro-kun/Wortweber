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

# Drittanbieterbibliotheken
import requests

# Projektspezifische Module
from src.plugin_system.plugin_interface import AbstractPlugin
from src.plugin_system.event_system import EventSystem
from src.utils.error_handling import logger

class OllamaLLMChatPlugin(AbstractPlugin):
    """
    Ein Plugin für den Chat mit einem von Ollama gehosteten LLM.

    Dieses Plugin ermöglicht die Interaktion mit einem Large Language Model (LLM),
    das von Ollama gehostet wird, über eine grafische Benutzeroberfläche.
    """

    def __init__(self):
        """Initialisiert das OllamaLLMChatPlugin mit Standardwerten."""
        self._name = "Ollama LLM Chat Plugin"
        self._version = "1.0.0"
        self._description = "Ein Plugin für den Chat mit einem von Ollama gehosteten LLM"
        self._author = "Wortweber-Entwickler"
        self._chat_window = None
        self._chat_display = None
        self._input_text = None
        self._chat_history = []
        self._system_message = "Du bist ein hilfreicher Assistent."
        self._llm_model = "llama3.1:8b-instruct-q6_K"
        self._ollama_api_url = "http://127.0.0.1:11434/api/generate"

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
        self._ollama_api_url = settings.get('ollama_api_url', self._ollama_api_url)

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
            'ollama_api_url': self._ollama_api_url
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
            'ollama_api_url': self._ollama_api_url
        }

    def set_settings(self, settings: Dict[str, Any]) -> None:
        """
        Setzt die Einstellungen des Plugins.

        Args:
            settings (Dict[str, Any]): Ein Dictionary mit den neuen Einstellungen.
        """
        self._system_message = settings.get('system_message', self._system_message)
        self._llm_model = settings.get('llm_model', self._llm_model)
        self._ollama_api_url = settings.get('ollama_api_url', self._ollama_api_url)
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

        self._chat_display = tk.Text(self._chat_window, state='disabled')
        self._chat_display.pack(expand=True, fill='both', padx=10, pady=10)

        input_frame = tk.Frame(self._chat_window)
        input_frame.pack(fill='x', padx=10, pady=10)

        self._input_text = tk.Text(input_frame, height=3)
        self._input_text.pack(side='left', expand=True, fill='both')

        send_button = ttk.Button(input_frame, text="Senden", command=self.send_message)
        send_button.pack(side='right')

    def send_message(self):
        """Sendet die Nachricht aus dem Eingabefeld an das LLM und aktualisiert den Chat-Verlauf."""
        if self._input_text:
            user_message = self._input_text.get("1.0", tk.END).strip()
            if user_message:
                self.update_chat_display(f"User: {user_message}")
                self._input_text.delete("1.0", tk.END)
                self.get_llm_response(user_message)

    def get_llm_response(self, user_message: str):
        """
        Holt die Antwort vom LLM und aktualisiert den Chat-Verlauf.

        Args:
            user_message (str): Die Nachricht des Benutzers.
        """
        prompt = f"{self._system_message}\n\nUser: {user_message}\nAssistant:"
        try:
            response = requests.post(self._ollama_api_url, json={
                "model": self._llm_model,
                "prompt": prompt
            })
            response.raise_for_status()
            assistant_message = response.json()['response']
            self.update_chat_display(f"Assistant: {assistant_message}")
        except requests.RequestException as e:
            self.update_chat_display(f"Error: Konnte keine Verbindung zum LLM herstellen. {str(e)}")

    def update_chat_display(self, message: str):
        """
        Aktualisiert die Chat-Anzeige mit einer neuen Nachricht.

        Args:
            message (str): Die anzuzeigende Nachricht.
        """
        if self._chat_display:
            self._chat_display.config(state='normal')
            self._chat_display.insert(tk.END, message + "\n\n")
            self._chat_display.config(state='disabled')
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

        ttk.Label(frame, text="Ollama API URL:").pack(anchor='w')
        api_url_entry = ttk.Entry(frame)
        api_url_entry.insert(0, self._ollama_api_url)
        api_url_entry.pack(fill='x')

        def save_settings():
            self._system_message = system_message_entry.get()
            self._llm_model = llm_model_entry.get()
            self._ollama_api_url = api_url_entry.get()

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

# 1. Klassenstruktur:
#    Die OllamaLLMChatPlugin-Klasse implementiert das AbstractPlugin-Interface und
#    bietet Funktionen für die Interaktion mit einem Ollama-gehosteten LLM.

# 2. Chat-Fenster:
#    Das Plugin erstellt ein separates Fenster für den Chat, das Text anzeigen
#    und Benutzereingaben entgegennehmen kann.

# 3. LLM-Interaktion:
#    Die get_llm_response-Methode sendet Anfragen an das LLM und verarbeitet die Antworten.

# 4. Konfiguration:
#    Das Plugin bietet eine Benutzeroberfläche zur Konfiguration von System-Nachrichten,
#    LLM-Modell und API-URL.

# 5. Event-Handling:
#    Das Plugin registriert sich für das "text_transcribed"-Event, um auf neue
#    Transkriptionen reagieren zu können.
