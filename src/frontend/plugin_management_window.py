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
from tkinter import ttk, messagebox
from typing import Any

# Projektspezifische Module
from src.utils.error_handling import handle_exceptions, logger
from src.plugin_system.plugin_manager import PluginManager

class PluginManagementWindow(tk.Toplevel):
    """
    Ein Fenster zur Verwaltung von Plugins in der Wortweber-Anwendung.

    Diese Klasse erstellt ein Toplevel-Fenster, das eine Übersicht aller verfügbaren Plugins
    anzeigt und Funktionen zur Aktivierung, Deaktivierung und Konfiguration von Plugins bietet.
    """

    @handle_exceptions
    def __init__(self, parent, plugin_manager: PluginManager, gui):
        """
        Initialisiert das Plugin-Verwaltungsfenster.

        Args:
            parent: Das übergeordnete Tkinter-Widget.
            plugin_manager (PluginManager): Der PluginManager der Anwendung.
            gui: Die Hauptinstanz der GUI.
        """
        super().__init__(parent)
        self.plugin_manager = plugin_manager
        self.gui = gui
        self.title("Plugin-Verwaltung")
        self.create_widgets()
        self.load_window_geometry()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        logger.debug("Plugin-Verwaltungsfenster initialisiert")

    @handle_exceptions
    def create_widgets(self):
        """Erstellt alle Widgets für das Plugin-Verwaltungsfenster."""
        self.tree = self.create_plugin_tree()
        self.create_buttons()

    @handle_exceptions
    def create_plugin_tree(self):
        """
        Erstellt und konfiguriert den Treeview für die Plugin-Liste.

        Returns:
            ttk.Treeview: Der konfigurierte Treeview für die Plugin-Anzeige.
        """
        columns = ("Name", "Version", "Aktueller Status", "Aktivieren bei Anwendungsstart", "Einstellungen")
        tree = ttk.Treeview(self, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=100)

        tree.column("Name", width=200)
        tree.column("Aktueller Status", width=150)
        tree.column("Aktivieren bei Anwendungsstart", width=200)
        tree.column("Einstellungen", width=100)

        # Erstelle Tags für aktive und inaktive Plugins
        tree.tag_configure('active', background='lightgreen')
        tree.tag_configure('inactive', background='lightpink')

        tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.update_plugin_list(tree)
        return tree

    @handle_exceptions
    def update_plugin_list(self, tree):
        """
        Aktualisiert die Plugin-Liste im Treeview.

        Args:
            tree (ttk.Treeview): Der Treeview, der aktualisiert werden soll.
        """
        for item in tree.get_children():
            tree.delete(item)

        enabled_plugins = self.plugin_manager.settings_manager.get_enabled_plugins()

        for plugin_info in self.plugin_manager.get_plugin_info():
            plugin_name = plugin_info['name']
            is_active = plugin_name in self.plugin_manager.active_plugins
            is_enabled = plugin_name in enabled_plugins
            status_tag = 'active' if is_active else 'inactive'

            item = tree.insert("", "end", values=(
                plugin_name,
                plugin_info['version'],
                "Aktiv" if is_active else "Inaktiv",
                "☑" if is_enabled else "☐",
                "⚙"
            ))

            tree.item(item, tags=(status_tag,))

        tree.bind("<ButtonRelease-1>", self.on_tree_click)

    @handle_exceptions
    def on_tree_click(self, event):
        """
        Behandelt Klick-Ereignisse auf den Plugin-Treeview.

        Args:
            event: Das Tkinter-Event-Objekt des Klicks.
        """
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            plugin_name = self.tree.item(item)["values"][0]
            if column == "#3":  # Aktueller Status
                self.toggle_plugin_now(plugin_name)
            elif column == "#4":  # Aktivieren bei Anwendungsstart
                self.toggle_plugin_enabled(plugin_name)
            elif column == "#5":  # Einstellungen
                self.open_plugin_settings(plugin_name)

    @handle_exceptions
    def toggle_plugin_now(self, plugin_name):
        """
        Aktiviert oder deaktiviert ein Plugin sofort.

        Args:
            plugin_name (str): Der Name des zu togglenden Plugins.
        """
        if plugin_name in self.plugin_manager.active_plugins:
            self.plugin_manager.deactivate_plugin(plugin_name)
        else:
            self.plugin_manager.activate_plugin(plugin_name)
        self.update_plugin_list(self.tree)

    @handle_exceptions
    def toggle_plugin_enabled(self, plugin_name):
        """
        Ändert den Aktivierungsstatus eines Plugins für den nächsten Start.

        Args:
            plugin_name (str): Der Name des Plugins, dessen Status geändert werden soll.
        """
        enabled_plugins = self.plugin_manager.settings_manager.get_enabled_plugins()
        is_enabled = plugin_name in enabled_plugins

        # Nutzen Sie hier die neue Methode des PluginManagers
        self.plugin_manager.set_plugin_enabled_at_startup(plugin_name, not is_enabled)

        self.update_plugin_list(self.tree)

    @handle_exceptions
    def open_plugin_settings(self, plugin_name):
        """
        Öffnet ein Einstellungsfenster für ein spezifisches Plugin.

        Args:
            plugin_name (str): Der Name des Plugins, dessen Einstellungen geändert werden sollen.
        """
        plugin = self.plugin_manager.plugins[plugin_name]
        settings_window = tk.Toplevel(self)
        settings_window.title(f"{plugin_name} Einstellungen")
        settings_window.geometry("400x300")

        current_settings = plugin.get_settings()

        for key, value in current_settings.items():
            frame = ttk.Frame(settings_window)
            frame.pack(fill="x", padx=5, pady=5)
            ttk.Label(frame, text=key).pack(side="left")
            entry = ttk.Entry(frame)
            entry.insert(0, str(value))
            entry.pack(side="right", expand=True, fill="x")

        def save_settings():
            new_settings = {}
            for child in settings_window.winfo_children():
                if isinstance(child, ttk.Frame):
                    key = child.winfo_children()[0].cget("text")
                    value_widget = child.winfo_children()[1]
                    if hasattr(value_widget, 'get'):
                        value = value_widget.get()  # type: ignore
                    else:
                        value = value_widget.cget("text")
                    new_settings[key] = value
            self.plugin_manager.update_plugin_settings(plugin_name, new_settings)
            settings_window.destroy()
            self.update_plugin_list(self.tree)

        ttk.Button(settings_window, text="Speichern", command=save_settings).pack(pady=10)

    @handle_exceptions
    def create_buttons(self):
        """Erstellt die Schaltflächen im Plugin-Verwaltungsfenster."""
        button_frame = ttk.Frame(self)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Schließen", command=self.on_closing).pack(side="right")

    @handle_exceptions
    def load_window_geometry(self):
        """Lädt die gespeicherte Fenstergröße und -position."""
        geometry = self.gui.settings_manager.get_setting("plugin_window_geometry")
        if geometry:
            self.geometry(geometry)
            logger.debug(f"Gespeicherte Plugin-Fenstergeometrie geladen: {geometry}")
        else:
            # Wenn keine gespeicherte Geometrie vorhanden ist, zentriere das Fenster
            self.update_idletasks()
            width = self.winfo_width()
            height = self.winfo_height()
            x = (self.winfo_screenwidth() // 2) - (width // 2)
            y = (self.winfo_screenheight() // 2) - (height // 2)
            self.geometry('{}x{}+{}+{}'.format(width, height, x, y))
            logger.debug("Plugin-Fenster zentriert (keine gespeicherte Geometrie)")

    @handle_exceptions
    def on_closing(self):
        """Wird aufgerufen, wenn das Fenster geschlossen wird."""
        current_geometry = self.geometry()
        self.gui.settings_manager.set_setting("plugin_window_geometry", current_geometry)
        logger.info(f"Plugin-Verwaltungsfenster geschlossen, Geometrie {current_geometry} gespeichert")
        self.destroy()

    @classmethod
    @handle_exceptions
    def open_window(cls, parent, plugin_manager, gui):
        """
        Öffnet ein neues Plugin-Verwaltungsfenster.

        Args:
            parent: Das übergeordnete Tkinter-Widget.
            plugin_manager (PluginManager): Der PluginManager der Anwendung.
            gui: Die Hauptinstanz der GUI.

        Returns:
            PluginManagementWindow: Eine neue Instanz des Plugin-Verwaltungsfensters.
        """
        return cls(parent, plugin_manager, gui)

# Zusätzliche Erklärungen:
# Die Klasse PluginManagementWindow implementiert ein Verwaltungsfenster für Plugins.
# Sie ermöglicht es dem Benutzer, Plugins zu aktivieren/deaktivieren, deren Einstellungen zu ändern
# und festzulegen, ob ein Plugin beim nächsten Start der Anwendung aktiviert werden soll.
# Die Methode toggle_plugin_enabled wurde angepasst, um die neue Methode set_plugin_enabled_at_startup
# des PluginManagers zu verwenden, was eine klare Trennung zwischen dem aktuellen Aktivierungsstatus
# und der Einstellung für den nächsten Start gewährleistet.
