import tkinter as tk
from tkinter import messagebox

materiales = []

def guardar_material():

    material = {
        "codigo": entry_codigo.get(),
        "descripcion": entry_descripcion.get(),
        "proveedor": entry_proveedor.get()
    }

    materiales.append(material)

    messagebox.showinfo("Éxito", "Material registrado")


def mostrar_materiales():

    lista.delete(0, tk.END)

    for m in materiales:
        lista.insert(tk.END, m)


def ventana_materiales():

    global entry_codigo, entry_descripcion, entry_proveedor, lista

    ventana = tk.Toplevel()
    ventana.title("Gestión de Materiales")

    tk.Label(ventana, text="Código").pack()
    entry_codigo = tk.Entry(ventana)
    entry_codigo.pack()

    tk.Label(ventana, text="Descripción").pack()
    entry_descripcion = tk.Entry(ventana)
    entry_descripcion.pack()

    tk.Label(ventana, text="Proveedor").pack()
    entry_proveedor = tk.Entry(ventana)
    entry_proveedor.pack()

    tk.Button(ventana, text="Guardar", command=guardar_material).pack()
    tk.Button(ventana, text="Mostrar", command=mostrar_materiales).pack()

    lista = tk.Listbox(ventana)
    lista.pack(fill="both", expand=True)