from tkinter import ttk

class VistaProyectos:
    def __init__(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🏗 Proyectos")

        ttk.Label(frame, text="Vista de proyectos funcionando").pack(pady=20)