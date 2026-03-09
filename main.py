import tkinter as tk
from proyectos import ventana_proyectos
from fases import ventana_fases
from materiales import ventana_materiales
from empleados import ventana_empleados


ventana = tk.Tk()
ventana.title("Sistema Construdata")
ventana.geometry("400x400")


titulo = tk.Label(ventana, text="Sistema de Gestión Construdata", font=("Arial", 14))
titulo.pack(pady=20)


btn1 = tk.Button(ventana, text="Gestión de Proyectos", width=25, command=ventana_proyectos)
btn1.pack(pady=5)

btn2 = tk.Button(ventana, text="Gestión de Fases", width=25, command=ventana_fases)
btn2.pack(pady=5)

btn3 = tk.Button(ventana, text="Gestión de Materiales", width=25, command=ventana_materiales)
btn3.pack(pady=5)

btn4 = tk.Button(ventana, text="Gestión de Empleados", width=25, command=ventana_empleados)
btn4.pack(pady=5)


ventana.mainloop()