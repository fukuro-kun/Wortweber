import tkinter as tk
from tkinter import ttk, colorchooser
import ttkthemes

class ThemeDemo:
    def __init__(self):
        self.root = ttkthemes.ThemedTk()
        self.root.title("Tkinter Theme und Farb-Demo")
        self.root.geometry("600x700")

        self.themes = sorted(ttkthemes.THEMES)
        self.current_theme_index = 0
        self.current_theme = tk.StringVar(value=self.themes[self.current_theme_index])

        self.text_bg = 'white'
        self.text_fg = 'black'
        self.select_bg = 'lightblue'
        self.select_fg = 'black'

        self.create_widgets()
        self.bind_keys()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Theme-Auswahl
        theme_frame = ttk.LabelFrame(main_frame, text="Theme Auswahl (← →)", padding="10")
        theme_frame.pack(fill=tk.X, pady=(0, 20))

        self.theme_label = ttk.Label(theme_frame, textvariable=self.current_theme, font=("Arial", 12, "bold"))
        self.theme_label.pack(fill=tk.X)

        # Farbauswahl-Buttons
        color_frame = ttk.LabelFrame(main_frame, text="Farbauswahl", padding="10")
        color_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Button(color_frame, text="Textfarbe", command=lambda: self.choose_color('text_fg')).pack(side=tk.LEFT, padx=5)
        ttk.Button(color_frame, text="Texthintergrund", command=lambda: self.choose_color('text_bg')).pack(side=tk.LEFT, padx=5)
        ttk.Button(color_frame, text="Auswahlfarbe", command=lambda: self.choose_color('select_fg')).pack(side=tk.LEFT, padx=5)
        ttk.Button(color_frame, text="Auswahlhintergrund", command=lambda: self.choose_color('select_bg')).pack(side=tk.LEFT, padx=5)

        # Textfeld
        text_frame = ttk.LabelFrame(main_frame, text="Textbeispiel", padding="10")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))

        self.text_widget = tk.Text(text_frame, wrap=tk.WORD, height=10)
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        self.text_widget.insert(tk.END, "Dies ist ein Beispieltext. Sie können diesen Text markieren, um die Auswahlfarben zu sehen.")
        self.update_text_colors()

        # Demo-Elemente
        demo_frame = ttk.LabelFrame(main_frame, text="Demo-Elemente", padding="10")
        demo_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Button(demo_frame, text="Standard Button").pack(fill=tk.X, pady=5)
        ttk.Button(demo_frame, text="Deaktivierter Button", state="disabled").pack(fill=tk.X, pady=5)
        ttk.Entry(demo_frame).pack(fill=tk.X, pady=5)
        ttk.Combobox(demo_frame, values=["Option 1", "Option 2", "Option 3"]).pack(fill=tk.X, pady=5)
        ttk.Checkbutton(demo_frame, text="Checkbutton").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(demo_frame, text="Radiobutton", value=1).pack(anchor=tk.W, pady=2)
        ttk.Progressbar(demo_frame, value=50).pack(fill=tk.X, pady=5)

    def bind_keys(self):
        self.root.bind('<Left>', self.previous_theme)
        self.root.bind('<Right>', self.next_theme)

    def change_theme(self):
        self.root.set_theme(self.current_theme.get())

    def next_theme(self, event=None):
        self.current_theme_index = (self.current_theme_index + 1) % len(self.themes)
        self.current_theme.set(self.themes[self.current_theme_index])
        self.change_theme()

    def previous_theme(self, event=None):
        self.current_theme_index = (self.current_theme_index - 1) % len(self.themes)
        self.current_theme.set(self.themes[self.current_theme_index])
        self.change_theme()

    def choose_color(self, target):
        color = colorchooser.askcolor(title=f"Wählen Sie eine Farbe für {target}")
        if color[1]:
            setattr(self, target, color[1])
            self.update_text_colors()

    def update_text_colors(self):
        self.text_widget.config(fg=self.text_fg, bg=self.text_bg, selectforeground=self.select_fg, selectbackground=self.select_bg)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    demo = ThemeDemo()
    demo.run()
