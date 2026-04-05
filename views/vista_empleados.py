from tkinter import ttk

class VistaEmpleados:
    def __init__(self, notebook):
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="👷 Empleados")

        ttk.Label(frame, text="Vista de empleados funcionando").pack(pady=20)