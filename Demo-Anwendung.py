import tkinter as tk
from tkinter import ttk
import ttkthemes

class ThemeDemo:
    def __init__(self):
        self.root = ttkthemes.ThemedTk()
        self.root.title("Tkinter Theme Demo")
        self.root.geometry("400x500")

        self.themes = ttkthemes.THEMES
        self.current_theme = tk.StringVar(value=self.themes[0])

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Theme-Auswahl
        theme_frame = ttk.LabelFrame(main_frame, text="Theme Auswahl", padding="10")
        theme_frame.pack(fill=tk.X, pady=(0, 20))

        theme_dropdown = ttk.Combobox(theme_frame, textvariable=self.current_theme, values=self.themes, state="readonly")
        theme_dropdown.pack(fill=tk.X)
        theme_dropdown.bind("<<ComboboxSelected>>", self.change_theme)

        # Demo-Elemente
        demo_frame = ttk.LabelFrame(main_frame, text="Demo-Elemente", padding="10")
        demo_frame.pack(fill=tk.BOTH, expand=True)

        # Buttons
        ttk.Button(demo_frame, text="Standard Button").pack(fill=tk.X, pady=5)
        ttk.Button(demo_frame, text="Deaktivierter Button", state="disabled").pack(fill=tk.X, pady=5)

        # Entry
        ttk.Entry(demo_frame).pack(fill=tk.X, pady=5)

        # Combobox
        ttk.Combobox(demo_frame, values=["Option 1", "Option 2", "Option 3"]).pack(fill=tk.X, pady=5)

        # Checkbuttons
        ttk.Checkbutton(demo_frame, text="Checkbutton 1").pack(anchor=tk.W, pady=2)
        ttk.Checkbutton(demo_frame, text="Checkbutton 2").pack(anchor=tk.W, pady=2)

        # Radiobuttons
        radio_var = tk.StringVar(value="1")
        ttk.Radiobutton(demo_frame, text="Radiobutton 1", variable=radio_var, value="1").pack(anchor=tk.W, pady=2)
        ttk.Radiobutton(demo_frame, text="Radiobutton 2", variable=radio_var, value="2").pack(anchor=tk.W, pady=2)

        # Progressbar
        ttk.Progressbar(demo_frame, value=50).pack(fill=tk.X, pady=5)

        # Notebook (Tabs)
        notebook = ttk.Notebook(demo_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=5)
        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab1, text="Tab 1")
        notebook.add(tab2, text="Tab 2")

    def change_theme(self, event):
        self.root.set_theme(self.current_theme.get())

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    demo = ThemeDemo()
    demo.run()
