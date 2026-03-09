import tkinter as tk
from tkinter import messagebox

proyectos = []

def guardar_proyecto():

    proyecto = {
        "codigo": entry_codigo.get(),
        "nombre": entry_nombre.get(),
        "direccion": entry_direccion.get(),
        "tipo": entry_tipo.get()
    }

    proyectos.append(proyecto)

    messagebox.showinfo("Éxito", "Proyecto registrado")


def mostrar_proyectos():

    lista.delete(0, tk.END)

    for p in proyectos:
        lista.insert(tk.END, p)


def ventana_proyectos():

    global entry_codigo, entry_nombre, entry_direccion, entry_tipo, lista

    ventana = tk.Toplevel()
    ventana.title("Gestión de Proyectos")

    tk.Label(ventana, text="Código").pack()
    entry_codigo = tk.Entry(ventana)
    entry_codigo.pack()

    tk.Label(ventana, text="Nombre").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()

    tk.Label(ventana, text="Dirección").pack()
    entry_direccion = tk.Entry(ventana)
    entry_direccion.pack()

    tk.Label(ventana, text="Tipo").pack()
    entry_tipo = tk.Entry(ventana)
    entry_tipo.pack()

    tk.Button(ventana, text="Guardar", command=guardar_proyecto).pack()
    tk.Button(ventana, text="Mostrar", command=mostrar_proyectos).pack()

    lista = tk.Listbox(ventana)
    lista.pack(fill="both", expand=True)