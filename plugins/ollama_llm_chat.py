import tkinter as tk
from tkinter import ttk
import requests
from src.plugin_system.plugin_interface import AbstractPlugin
from typing import Dict, Any, Optional
from src.plugin_system.event_system import EventSystem

class OllamaLLMChatPlugin(AbstractPlugin):
    def __init__(self):
        self._name = "Ollama LLM Chat Plugin"
        self._version = "1.0.0"
        self._description = "Ein Plugin für den Chat mit einem von Ollama gehosteten LLM"
        self._author = "Wortweber-Entwickler"
        self._chat_window = None
        self._chat_display = None
        self._input_text = None
        self._chat_history = []
        self._system_message = "Du bist ein hilfreicher Assistent."
        self._llm_model = "llama2"
        self._ollama_api_url = "http://localhost:11434/api/generate"

    @property
    def name(self) -> str:
        return self._name

    @property
    def version(self) -> str:
        return self._version

    @property
    def description(self) -> str:
        return self._description

    @property
    def author(self) -> str:
        return self._author

    def activate(self, settings: Dict[str, Any]) -> None:
        self._system_message = settings.get('system_message', self._system_message)
        self._llm_model = settings.get('llm_model', self._llm_model)
        self._ollama_api_url = settings.get('ollama_api_url', self._ollama_api_url)

    def deactivate(self) -> Optional[Dict[str, Any]]:
        if self._chat_window:
            self._chat_window.destroy()
        return {
            'system_message': self._system_message,
            'llm_model': self._llm_model,
            'ollama_api_url': self._ollama_api_url
        }

    def process_text(self, text: str) -> str:
        if self._chat_window and self._input_text and self._input_text.focus_get() == self._input_text:
            self._input_text.insert(tk.END, text)
        return text

    def get_settings(self) -> Dict[str, Any]:
        return {
            'system_message': self._system_message,
            'llm_model': self._llm_model,
            'ollama_api_url': self._ollama_api_url
        }

    def set_settings(self, settings: Dict[str, Any]) -> None:
        self._system_message = settings.get('system_message', self._system_message)
        self._llm_model = settings.get('llm_model', self._llm_model)
        self._ollama_api_url = settings.get('ollama_api_url', self._ollama_api_url)

    def get_ui_elements(self) -> Dict[str, Any]:
        return {
            "buttons": [
                {
                    "text": "Ollama LLM Chat",
                    "command": self.open_chat_window
                }
            ]
        }

    def open_chat_window(self):
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
        if self._input_text:
            user_message = self._input_text.get("1.0", tk.END).strip()
            if user_message:
                self.update_chat_display(f"User: {user_message}")
                self._input_text.delete("1.0", tk.END)
                self.get_llm_response(user_message)

    def get_llm_response(self, user_message: str):
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
        if self._chat_display:
            self._chat_display.config(state='normal')
            self._chat_display.insert(tk.END, message + "\n\n")
            self._chat_display.config(state='disabled')
            self._chat_display.see(tk.END)

    def get_config_ui(self, parent: tk.Widget) -> ttk.Frame:
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
        event_system.add_listener("text_transcribed", self.on_text_transcribed)

    def on_text_transcribed(self, text: str) -> None:
        self.process_text(text)
