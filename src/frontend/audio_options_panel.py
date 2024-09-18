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

# src/frontend/audio_options_panel.py

import tkinter as tk
from tkinter import ttk
import pyaudio
from src.utils.error_handling import handle_exceptions, logger
from src.config import DEFAULT_AUDIO_DEVICE_INDEX

class AudioOptionsPanel(ttk.Frame):
    @handle_exceptions
    def __init__(self, parent, settings_manager, on_device_change_callback, backend):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.on_device_change_callback = on_device_change_callback
        self.backend = backend
        self.audio_devices = self.get_audio_devices()
        self.initial_device = self.settings_manager.get_setting("audio_device_index", DEFAULT_AUDIO_DEVICE_INDEX)
        self.selected_device = tk.StringVar(value=self.initial_device)
        self.setup_ui()

    @handle_exceptions
    def setup_ui(self):
        ttk.Label(self, text="Audiogeräte:").pack(anchor="w", padx=5, pady=5)
        for index, name in self.audio_devices.items():
            ttk.Radiobutton(
                self,
                text=name,
                variable=self.selected_device,
                value=index,
                command=self.on_device_change
            ).pack(anchor="w", padx=20, pady=2)

        bottom_frame = ttk.Frame(self)
        bottom_frame.pack(fill=tk.X, padx=5, pady=10)

        refresh_button = ttk.Button(bottom_frame, text="Geräteliste aktualisieren", command=self.refresh_devices)
        refresh_button.pack(side=tk.LEFT)

        # Kontrollfenster für das aktuell verwendete Gerät
        ttk.Label(bottom_frame, text="Aktuell verwendetes Gerät:").pack(side=tk.LEFT, padx=(20, 5))
        self.current_device_label = ttk.Label(bottom_frame, text="", wraplength=300)
        self.current_device_label.pack(side=tk.LEFT)

        self.update_current_device_label()

    @handle_exceptions
    def get_audio_devices(self):
        p = pyaudio.PyAudio()
        devices = {}
        try:
            for i in range(p.get_device_count()):
                device_info = p.get_device_info_by_index(i)
                if device_info['maxInputChannels'] > 0:  # Nur Eingabegeräte
                    devices[str(i)] = f"{device_info['name']} (Index: {i})"
        finally:
            p.terminate()
        return devices

    @handle_exceptions
    def on_device_change(self):
        selected_index = self.selected_device.get()
        self.settings_manager.set_setting("audio_device_index", selected_index)
        self.settings_manager.save_settings()
        logger.info(f"Audiogerät in Einstellungen geändert zu Index: {selected_index}")

        # Aktualisiere das Backend
        if self.on_device_change_callback:
            self.on_device_change_callback()

        # Warte kurz, um sicherzustellen, dass das Backend aktualisiert wurde
        self.after(100, self.update_current_device_label)

    @handle_exceptions
    def refresh_devices(self):
        """Aktualisiert die Liste der Audiogeräte."""
        self.audio_devices = self.get_audio_devices()
        for widget in self.winfo_children():
            widget.destroy()
        self.setup_ui()
        logger.info("Audiogeräteliste aktualisiert")

    @handle_exceptions
    def undo_changes(self):
        """Setzt die Audiogeräteauswahl auf den ursprünglichen Wert zurück."""
        self.selected_device.set(self.initial_device)
        self.on_device_change()
        logger.info(f"Audiogeräteauswahl zurückgesetzt auf: {self.initial_device}")

    @handle_exceptions
    def update_current_device_label(self):
        """Aktualisiert das Label mit dem aktuell verwendeten Gerät."""
        current_device = self.backend.audio_processor.get_current_device_info()
        if current_device:
            self.current_device_label.config(text=f"{current_device['name']} (Index: {current_device['index']})")
        else:
            self.current_device_label.config(text="Kein Gerät ausgewählt oder verfügbar")


# Zusätzliche Erklärungen:

# 1. Klasse AudioOptionsPanel:
#    Diese Klasse erstellt ein Tkinter Frame, das die Audiogeräteauswahl ermöglicht.

# 2. Initialisierung:
#    Im Konstruktor werden der SettingsManager und ein Callback für Geräteänderungen übergeben.
#    Die verfügbaren Audiogeräte werden bei der Initialisierung abgerufen.

# 3. UI-Aufbau:
#    Die setup_ui Methode erstellt die Benutzeroberfläche mit Radiobuttons für jedes verfügbare Audiogerät
#    und einem Button zum Aktualisieren der Geräteliste.

# 4. Audiogeräte abrufen:
#    Die get_audio_devices Methode verwendet PyAudio, um alle verfügbaren Eingabegeräte zu identifizieren.

# 5. Geräteänderung:
#    Wenn der Benutzer ein anderes Gerät auswählt, wird die Änderung sofort gespeichert und das Callback aufgerufen.

# 6. Aktualisierung der Geräteliste:
#    Die refresh_devices Methode ermöglicht es, die Liste der Audiogeräte zur Laufzeit zu aktualisieren.

# 7. Rückgängig machen von Änderungen:
#    Die undo_changes Methode setzt die Auswahl auf den ursprünglichen Wert zurück.

# 8. Fehlerbehandlung:
#    Alle Methoden sind mit dem @handle_exceptions Decorator versehen, um eine einheitliche Fehlerbehandlung zu gewährleisten.

# Diese Implementierung bietet eine benutzerfreundliche Oberfläche zur Auswahl und Verwaltung von Audiogeräten,
# mit der Möglichkeit, die Geräteliste zu aktualisieren, auf Geräteänderungen zu reagieren und Änderungen rückgängig zu machen.
