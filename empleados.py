import tkinter as tk
from tkinter import messagebox

empleados = []

def guardar_empleado():

    empleado = {
        "dni": entry_dni.get(),
        "nombre": entry_nombre.get(),
        "cargo": entry_cargo.get()
    }

    empleados.append(empleado)

    messagebox.showinfo("Éxito", "Empleado registrado")


def mostrar_empleados():

    lista.delete(0, tk.END)

    for e in empleados:
        lista.insert(tk.END, e)


def ventana_empleados():

    global entry_dni, entry_nombre, entry_cargo, lista

    ventana = tk.Toplevel()
    ventana.title("Gestión de Empleados")

    tk.Label(ventana, text="DNI").pack()
    entry_dni = tk.Entry(ventana)
    entry_dni.pack()

    tk.Label(ventana, text="Nombre").pack()
    entry_nombre = tk.Entry(ventana)
    entry_nombre.pack()

    tk.Label(ventana, text="Cargo").pack()
    entry_cargo = tk.Entry(ventana)
    entry_cargo.pack()

    tk.Button(ventana, text="Guardar", command=guardar_empleado).pack()
    tk.Button(ventana, text="Mostrar", command=mostrar_empleados).pack()

    lista = tk.Listbox(ventana)
    lista.pack(fill="both", expand=True)