import ttkthemes
import tkinter as tk

class ThemeManager:
    def __init__(self, root, settings_manager):
        self.root = root
        self.settings_manager = settings_manager
        self.themes = sorted(ttkthemes.THEMES)
        self.current_theme_index = 0
        self.current_theme = tk.StringVar(value=self.themes[self.current_theme_index])

    def setup_theme_selection(self, parent):
        theme_frame = tk.Frame(parent)
        theme_frame.pack(fill=tk.X, pady=5)

        ttk.Label(theme_frame, text="Theme:").pack(side=tk.LEFT, padx=(0, 5))
        self.theme_dropdown = ttk.Combobox(theme_frame, textvariable=self.current_theme, values=self.themes, state="readonly", width=15)
        self.theme_dropdown.pack(side=tk.LEFT)
        self.theme_dropdown.bind("<<ComboboxSelected>>", self.on_theme_change)

        ttk.Button(theme_frame, text="Vorheriges Theme", command=self.previous_theme).pack(side=tk.LEFT, padx=5)
        ttk.Button(theme_frame, text="Nächstes Theme", command=self.next_theme).pack(side=tk.LEFT)

    def on_theme_change(self, event=None):
        selected_theme = self.current_theme.get()
        self.change_theme(selected_theme)

    def change_theme(self, theme_name):
        self.root.set_theme(theme_name)
        self.current_theme.set(theme_name)
        self.settings_manager.set_setting("theme", theme_name)

    def next_theme(self):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.change_theme(self.themes[self.current_theme_index])

    def previous_theme(self):
        self.current_theme_index = (self.current_theme_index - 1) % len(self.themes)
        self.change_theme(self.themes[self.current_theme_index])

    def apply_saved_theme(self):
        saved_theme = self.settings_manager.get_setting("theme")
        if saved_theme in self.themes:
            self.change_theme(saved_theme)
        else:
            self.change_theme(self.themes[0])
