import tkinter as tk
from tkinter import messagebox

fases = []

def guardar_fase():

    fase = {
        "codigo": entry_codigo.get(),
        "nombre": entry_nombre.get(),
        "avance": entry_avance.get()
    }

    fases.append(fase)

    messagebox.showinfo("Éxito", "Fase registrada")


def mostrar_fases():

    lista.delete(0, tk.END)

    for f in fases:
        lista.insert(tk.END, f)


def ventana_fases():

    global entry_codigo, entry_nombre, entry_avance, lista

    ventana = tk.Toplevel()
    ventana.title("Gestión de Fases")

    tk.Label(ventana, text="Código fase").pack()
    entry_codigo = tk.Entry(ventana)
    entry_codigo.pack()

    tk.Label(ventana, text="Nombre fase").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()

    tk.Label(ventana, text="Avance (%)").pack()
    entry_avance = tk.Entry(ventana)
    entry_avance.pack()

    tk.Button(ventana, text="Guardar", command=guardar_fase).pack()
    tk.Button(ventana, text="Mostrar", command=mostrar_fases).pack()

    lista = tk.Listbox(ventana)
    lista.pack(fill="both", expand=True)