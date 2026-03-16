import mysql.connector
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# =========================
# CONEXION BASE DE DATOS
# =========================

def conectar():

    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="construdata"
    )


# =========================
# VENTANA PRINCIPAL
# =========================

ventana = Tk()
ventana.title("Sistema Construdata")
ventana.geometry("1000x600")


notebook = ttk.Notebook(ventana)
notebook.pack(fill="both", expand=True)


# ==========================================================
# MODULO PROYECTOS
# ==========================================================

frame_proyectos = Frame(notebook)
notebook.add(frame_proyectos,text="Proyectos")


Label(frame_proyectos,text="Codigo").grid(row=0,column=0,padx=10,pady=5)
codigo = Entry(frame_proyectos)
codigo.grid(row=0,column=1)

Label(frame_proyectos,text="Nombre").grid(row=1,column=0)
nombre = Entry(frame_proyectos)
nombre.grid(row=1,column=1)

Label(frame_proyectos,text="Direccion").grid(row=2,column=0)
direccion = Entry(frame_proyectos)
direccion.grid(row=2,column=1)

Label(frame_proyectos,text="Tipo Construccion").grid(row=3,column=0)
tipo = Entry(frame_proyectos)
tipo.grid(row=3,column=1)

Label(frame_proyectos,text="Area").grid(row=4,column=0)
area = Entry(frame_proyectos)
area.grid(row=4,column=1)

Label(frame_proyectos,text="Pisos").grid(row=5,column=0)
pisos = Entry(frame_proyectos)
pisos.grid(row=5,column=1)

Label(frame_proyectos,text="Fecha Inicio").grid(row=0,column=2)
inicio = Entry(frame_proyectos)
inicio.grid(row=0,column=3)

Label(frame_proyectos,text="Fecha Fin").grid(row=1,column=2)
fin = Entry(frame_proyectos)
fin.grid(row=1,column=3)

Label(frame_proyectos,text="Estado").grid(row=2,column=2)
estado = Entry(frame_proyectos)
estado.grid(row=2,column=3)

Label(frame_proyectos,text="Presupuesto").grid(row=3,column=2)
presupuesto = Entry(frame_proyectos)
presupuesto.grid(row=3,column=3)

Label(frame_proyectos,text="Gerente").grid(row=4,column=2)
gerente = Entry(frame_proyectos)
gerente.grid(row=4,column=3)


# TABLA

tabla_proyectos = ttk.Treeview(
    frame_proyectos,
    columns=("Codigo","Nombre","Tipo","Presupuesto","Estado"),
    show="headings"
)

tabla_proyectos.heading("Codigo",text="Codigo")
tabla_proyectos.heading("Nombre",text="Nombre")
tabla_proyectos.heading("Tipo",text="Tipo")
tabla_proyectos.heading("Presupuesto",text="Presupuesto")
tabla_proyectos.heading("Estado",text="Estado")

tabla_proyectos.grid(row=8,column=0,columnspan=4,pady=20)



# REGISTRAR PROYECTO

def registrar_proyecto():

    try:

        db = conectar()
        cursor = db.cursor()

        sql = "CALL sp_registrar_proyecto(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

        valores = (
            codigo.get(),
            nombre.get(),
            direccion.get(),
            tipo.get(),
            area.get(),
            pisos.get(),
            inicio.get(),
            fin.get(),
            estado.get(),
            presupuesto.get(),
            gerente.get()
        )

        cursor.execute(sql,valores)
        db.commit()

        messagebox.showinfo("Exito","Proyecto registrado")

        db.close()

        ver_proyectos()

    except Exception as e:
        messagebox.showerror("Error",str(e))



# VER PROYECTOS

def ver_proyectos():

    for fila in tabla_proyectos.get_children():
        tabla_proyectos.delete(fila)

    db = conectar()
    cursor = db.cursor()

    cursor.execute("CALL sp_ver_proyectos()")

    resultados = cursor.fetchall()

    for fila in resultados:
        tabla_proyectos.insert("",END,values=fila)

    db.close()



Button(frame_proyectos,text="Registrar",command=registrar_proyecto).grid(row=6,column=0,pady=10)

Button(frame_proyectos,text="Ver",command=ver_proyectos).grid(row=6,column=1,pady=10)



# ==========================================================
# MODULO EMPLEADOS
# ==========================================================

frame_empleados = Frame(notebook)
notebook.add(frame_empleados,text="Empleados")


tabla_empleados = ttk.Treeview(
    frame_empleados,
    columns=("Nombres","Apellidos","Especialidad","Cargo","Salario"),
    show="headings"
)

tabla_empleados.heading("Nombres",text="Nombres")
tabla_empleados.heading("Apellidos",text="Apellidos")
tabla_empleados.heading("Especialidad",text="Especialidad")
tabla_empleados.heading("Cargo",text="Cargo")
tabla_empleados.heading("Salario",text="Salario")

tabla_empleados.pack(pady=20)



def ver_empleados():

    for fila in tabla_empleados.get_children():
        tabla_empleados.delete(fila)

    db = conectar()
    cursor = db.cursor()

    cursor.execute("CALL sp_ver_empleados()")

    resultados = cursor.fetchall()

    for fila in resultados:
        tabla_empleados.insert("",END,values=fila)

    db.close()


Button(frame_empleados,text="Ver Empleados",command=ver_empleados).pack()



# ==========================================================
# MODULO MATERIALES
# ==========================================================

frame_materiales = Frame(notebook)
notebook.add(frame_materiales,text="Materiales")


Label(frame_materiales,text="Codigo").grid(row=0,column=0)
codigo_material = Entry(frame_materiales)
codigo_material.grid(row=0,column=1)

Label(frame_materiales,text="Descripcion").grid(row=1,column=0)
descripcion = Entry(frame_materiales)
descripcion.grid(row=1,column=1)

Label(frame_materiales,text="Categoria").grid(row=2,column=0)
categoria = Entry(frame_materiales)
categoria.grid(row=2,column=1)

Label(frame_materiales,text="Unidad").grid(row=3,column=0)
unidad = Entry(frame_materiales)
unidad.grid(row=3,column=1)

Label(frame_materiales,text="Especificaciones").grid(row=4,column=0)
especificaciones = Entry(frame_materiales)
especificaciones.grid(row=4,column=1)

Label(frame_materiales,text="Proveedor ID").grid(row=5,column=0)
proveedor = Entry(frame_materiales)
proveedor.grid(row=5,column=1)



tabla_materiales = ttk.Treeview(
    frame_materiales,
    columns=("Codigo","Descripcion","Categoria","Unidad"),
    show="headings"
)

tabla_materiales.heading("Codigo",text="Codigo")
tabla_materiales.heading("Descripcion",text="Descripcion")
tabla_materiales.heading("Categoria",text="Categoria")
tabla_materiales.heading("Unidad",text="Unidad")

tabla_materiales.grid(row=8,column=0,columnspan=4,pady=20)



def registrar_material():

    db = conectar()
    cursor = db.cursor()

    sql = "CALL sp_registrar_material(%s,%s,%s,%s,%s,%s)"

    valores = (
        codigo_material.get(),
        descripcion.get(),
        categoria.get(),
        unidad.get(),
        especificaciones.get(),
        proveedor.get()
    )

    cursor.execute(sql,valores)
    db.commit()

    messagebox.showinfo("Exito","Material registrado")

    db.close()



Button(frame_materiales,text="Registrar Material",command=registrar_material).grid(row=6,column=0,pady=10)



ventana.mainloop()