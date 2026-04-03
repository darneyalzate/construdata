from tkinter import ttk

class VistaProveedores:
    def __init__(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="🏭 Proveedores")

        ttk.Label(frame, text="Vista de proveedores funcionando").pack(pady=20)