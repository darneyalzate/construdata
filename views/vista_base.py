from tkinter import ttk

FUENTE_TITULO = ("Segoe UI", 12, "bold")

def aplicar_estilo_ttk(root):
    style = ttk.Style(root)
    style.theme_use("clam")