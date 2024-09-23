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

import tkinter as tk
from tkinter import ttk, messagebox, font
from src.utils.error_handling import handle_exceptions, logger
from src.plugin_system.plugin_manager import PluginManager
from src.frontend.settings_manager import SettingsManager
from typing import Any, Dict

class PluginManagementWindow:
    """
    Fenster zur Verwaltung von Plugins in der Wortweber-Anwendung.
    Ermöglicht das Aktivieren, Deaktivieren und Konfigurieren von Plugins.
    """

    @handle_exceptions
    def __init__(self, parent, plugin_manager: PluginManager):
        """
        Initialisiert das Plugin-Verwaltungsfenster.

        :param parent: Das übergeordnete Tkinter-Fenster
        :param plugin_manager: Eine Instanz des PluginManager
        """
        self.parent = parent
        self.plugin_manager = plugin_manager
        self.settings_manager = plugin_manager.settings_manager
        self.window = tk.Toplevel(parent)
        self.window.title("Plugin-Verwaltung")
        self.window.geometry("600x400")
        self.setup_font()
        self.create_widgets()
        self.drag_item = None
        self.drag_start_y = 0

    @handle_exceptions
    def setup_font(self):
        """Richtet eine geeignete Schriftart für das Fenster ein."""
        available_fonts = font.families()
        symbol_fonts = [
            "Segoe UI Symbol", "Arial Unicode MS", "DejaVu Sans",
            "Noto Sans", "Symbola", "Quivira"
        ]
        chosen_font = next((f for f in symbol_fonts if f in available_fonts), None)

        if chosen_font:
            self.custom_font = font.Font(family=chosen_font, size=10)
            self.window.option_add("*Font", self.custom_font)
        else:
            logger.warning("Keine geeignete Schriftart für Unicode-Symbole gefunden.")
            self.custom_font = font.nametofont("TkDefaultFont")

    @handle_exceptions
    def create_widgets(self):
        """Erstellt die Widgets für das Plugin-Verwaltungsfenster."""
        self.tree = self.create_plugin_tree()
        self.create_buttons()

    @handle_exceptions
    def create_plugin_tree(self):
        """
        Erstellt und konfiguriert den Treeview für die Plugin-Liste.

        :return: Der konfigurierte Treeview
        """
        columns = ("Name", "Version", "Status", "Aktiv", "Einstellungen")
        tree = ttk.Treeview(self.window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=100)

        tree.column("Name", width=200)
        tree.column("Status", width=80)
        tree.column("Aktiv", width=50)
        tree.column("Einstellungen", width=100)

        tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.update_plugin_list(tree)

        tree.bind("<ButtonPress-1>", self.on_tree_press)
        tree.bind("<B1-Motion>", self.on_tree_motion)
        tree.bind("<ButtonRelease-1>", self.on_tree_release)

        return tree

    @handle_exceptions
    def update_plugin_list(self, tree):
        """
        Aktualisiert die Plugin-Liste im Treeview unter Beibehaltung der bestehenden Reihenfolge.
        """
        current_order = [tree.item(child)["values"][0] for child in tree.get_children()]
        for item in tree.get_children():
            tree.delete(item)

        plugin_info_dict = {info['name']: info for info in self.plugin_manager.get_plugin_info()}

        # Zuerst die Plugins in der aktuellen Reihenfolge einfügen
        for plugin_name in current_order:
            if plugin_name in plugin_info_dict:
                self.insert_plugin_to_tree(tree, plugin_info_dict[plugin_name])
                del plugin_info_dict[plugin_name]

        # Dann alle neuen Plugins am Ende einfügen
        for plugin_info in plugin_info_dict.values():
            self.insert_plugin_to_tree(tree, plugin_info)

        tree.bind("<ButtonRelease-1>", self.on_tree_click)

    @handle_exceptions
    def insert_plugin_to_tree(self, tree, plugin_info: Dict[str, Any]):
        """
        Fügt ein einzelnes Plugin in den Treeview ein.

        :param tree: Der Treeview, in den das Plugin eingefügt werden soll
        :param plugin_info: Ein Dictionary mit Informationen über das Plugin
        """
        plugin_name = plugin_info['name']
        is_active = plugin_info['active']
        status_symbol = "✓" if is_active else "✗"
        status_color = 'green' if is_active else 'red'

        item = tree.insert("", "end", values=(
            plugin_name,
            plugin_info['version'],
            status_symbol,
            "☑" if is_active else "☐",
            "Einst."
        ))

        tree.tag_configure(f'status_{item}', foreground=status_color)
        tree.item(item, tags=(f'status_{item}',))

    @handle_exceptions
    def on_tree_press(self, event):
        """
        Behandelt das Drücken der Maustaste auf dem Treeview.

        :param event: Das Mausereignis
        """
        self.drag_start_y = event.y
        self.drag_item = self.tree.identify_row(event.y)
        if self.drag_item:
            self.tree.selection_set(self.drag_item)
            self.tree.tag_configure('dragging', background='lightblue')
            self.tree.item(self.drag_item, tags='dragging')

    @handle_exceptions
    def on_tree_motion(self, event):
        """
        Behandelt die Mausbewegung während des Ziehens eines Items.

        :param event: Das Mausereignis
        """
        if self.drag_item:
            y = event.y - self.drag_start_y
            if abs(y) >= 20:
                move_to = self.tree.index(self.tree.identify_row(event.y))
                self.tree.move(self.drag_item, '', move_to)
                self.drag_start_y = event.y

    @handle_exceptions
    def on_tree_release(self, event):
        """
        Behandelt das Loslassen der Maustaste nach dem Ziehen eines Items.

        :param event: Das Mausereignis
        """
        if self.drag_item:
            new_index = self.tree.index(self.tree.identify_row(event.y))
            item_values = self.tree.item(self.drag_item)['values']
            plugin_name = item_values[0]
            self.plugin_manager.reorder_plugin(plugin_name, new_index)
            self.update_plugin_list(self.tree)
            self.save_plugin_order()
            self.drag_item = None
            self.tree.tag_configure('dragging', background='')

    @handle_exceptions
    def on_tree_click(self, event):
        """
        Behandelt Klick-Events auf den Treeview.

        :param event: Das Klick-Event
        """
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.identify_row(event.y)
            if column == "#4":  # Aktiv-Spalte
                self.toggle_plugin(self.tree.item(item)["values"][0])
            elif column == "#5":  # Einstellungen-Spalte
                self.open_plugin_settings(self.tree.item(item)["values"][0])

    @handle_exceptions
    def toggle_plugin(self, plugin_name):
        """
        Aktiviert oder deaktiviert ein Plugin.

        :param plugin_name: Name des zu togglenden Plugins
        """
        if plugin_name in self.plugin_manager.active_plugins:
            self.plugin_manager.deactivate_plugin(plugin_name)
        else:
            self.plugin_manager.activate_plugin(plugin_name)
        self.update_plugin_list(self.tree)
        logger.info(f"Plugin-Status geändert: {plugin_name}")

    @handle_exceptions
    def open_plugin_settings(self, plugin_name):
        """
        Öffnet das Einstellungsfenster für ein spezifisches Plugin.

        :param plugin_name: Name des Plugins, dessen Einstellungen geöffnet werden sollen
        """
        plugin = self.plugin_manager.plugins[plugin_name]
        settings_window = tk.Toplevel(self.window)
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
                    if isinstance(value_widget, (tk.Entry, ttk.Entry)):
                        value = value_widget.get()
                    elif isinstance(value_widget, tk.Label):
                        value = value_widget.cget("text")
                    else:
                        # Fallback für unbekannte Widget-Typen
                        value = str(value_widget)
                    new_settings[key] = value
            self.plugin_manager.update_plugin_settings(plugin_name, new_settings)
            settings_window.destroy()
            self.update_plugin_list(self.tree)

        ttk.Button(settings_window, text="Speichern", command=save_settings).pack(pady=10)

    @handle_exceptions
    def save_plugin_order(self):
        """Speichert die aktuelle Reihenfolge der Plugins."""
        plugin_order = [self.tree.item(child)["values"][0] for child in self.tree.get_children()]
        self.plugin_manager.save_plugin_order(plugin_order)
        logger.info(f"Plugin-Reihenfolge gespeichert: {plugin_order}")

    @handle_exceptions
    def create_buttons(self):
        """Erstellt die Buttons im Plugin-Verwaltungsfenster."""
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Schließen", command=self.window.destroy).pack(side="right")

    @classmethod
    @handle_exceptions
    def open_window(cls, parent, plugin_manager):
        """
        Klassenmethode zum Öffnen des Plugin-Verwaltungsfensters.

        :param parent: Das übergeordnete Tkinter-Fenster
        :param plugin_manager: Eine Instanz des PluginManager
        :return: Eine Instanz des PluginManagementWindow
        """
        return cls(parent, plugin_manager)


# Zusätzliche Erklärungen:

# 1. Drag-and-Drop Funktionalität:
#    Die Methoden on_tree_press, on_tree_motion und on_tree_release implementieren
#    die Drag-and-Drop-Funktionalität für die Neuanordnung von Plugins.

# 2. Persistenz:
#    Die save_plugin_order Methode sorgt dafür, dass die Reihenfolge der Plugins
#    nach jeder Änderung gespeichert wird.

# 3. Plugin-Aktivierung:
#    Die toggle_plugin Methode ermöglicht das Ein- und Ausschalten von Plugins
#    direkt aus der GUI heraus.

# 4. Einstellungsverwaltung:
#    Die open_plugin_settings Methode öffnet ein separates Fenster zur Konfiguration
#    der spezifischen Einstellungen jedes Plugins.

# 5. Fehlerbehandlung:
#    Alle Methoden sind mit dem @handle_exceptions Decorator versehen, um eine
#    konsistente Fehlerbehandlung zu gewährleisten.

# Diese Implementierung bietet eine benutzerfreundliche und erweiterbare Schnittstelle
# zur Verwaltung von Plugins in der Wortweber-Anwendung, mit Fokus auf Flexibilität
# und robuste Fehlerbehandlung.
