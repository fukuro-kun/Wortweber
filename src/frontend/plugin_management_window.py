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
from tkinter import ttk, messagebox
from src.utils.error_handling import handle_exceptions, logger
from src.plugin_system.plugin_manager import PluginManager
from typing import Any

class PluginManagementWindow:
    @handle_exceptions
    def __init__(self, parent, plugin_manager: PluginManager):
        self.parent = parent
        self.plugin_manager = plugin_manager
        self.window = tk.Toplevel(parent)
        self.window.title("Plugin-Verwaltung")
        self.window.geometry("600x400")
        self.create_widgets()

    @handle_exceptions
    def create_widgets(self):
        self.tree = self.create_plugin_tree()
        self.create_buttons()

    @handle_exceptions
    def create_plugin_tree(self):
        columns = ("Name", "Version", "Status", "Aktiv", "Einstellungen")
        tree = ttk.Treeview(self.window, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col, anchor="center")
            tree.column(col, anchor="center", width=100)

        tree.column("Name", width=200)
        tree.column("Einstellungen", width=100)

        # Erstelle Tags für aktive und inaktive Plugins
        tree.tag_configure('active', foreground='green')
        tree.tag_configure('inactive', foreground='red')

        tree.pack(expand=True, fill="both", padx=10, pady=10)

        self.update_plugin_list(tree)
        return tree

    @handle_exceptions
    def update_plugin_list(self, tree):
        for item in tree.get_children():
            tree.delete(item)

        for plugin_info in self.plugin_manager.get_plugin_info():
            plugin_name = plugin_info['name']
            is_active = plugin_info['active']
            status_text = "Aktiv" if is_active else "Inaktiv"
            status_tag = 'active' if is_active else 'inactive'

            item = tree.insert("", "end", values=(
                plugin_name,
                plugin_info['version'],
                status_text,
                "☑" if is_active else "☐",
                "⚙"
            ))

            # Wende das Tag nur auf die Status-Spalte an
            tree.item(item, tags=(status_tag,))

        tree.bind("<ButtonRelease-1>", self.on_tree_click)

    @handle_exceptions
    def on_tree_click(self, event):
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
        if plugin_name in self.plugin_manager.active_plugins:
            self.plugin_manager.deactivate_plugin(plugin_name)
        else:
            self.plugin_manager.activate_plugin(plugin_name)
        self.update_plugin_list(self.tree)

    @handle_exceptions
    def open_plugin_settings(self, plugin_name):
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
        button_frame = ttk.Frame(self.window)
        button_frame.pack(fill="x", padx=10, pady=10)

        ttk.Button(button_frame, text="Schließen", command=self.window.destroy).pack(side="right")

    @classmethod
    @handle_exceptions
    def open_window(cls, parent, plugin_manager):
        return cls(parent, plugin_manager)
