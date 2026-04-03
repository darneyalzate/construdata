from tkinter import ttk

class VistaMateriales:
    def __init__(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🧱 Materiales")

        ttk.Label(frame, text="Vista de materiales funcionando").pack(pady=20)