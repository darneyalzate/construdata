import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import re
import os

# Pillow para imágenes (opcional)
try:
    from PIL import Image, ImageTk
    PIL_OK = True
except ImportError:
    PIL_OK = False

# Carpeta donde se guardan las imágenes del sistema
CARPETA_IMG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "imagenes_construdata")
os.makedirs(CARPETA_IMG, exist_ok=True)


# ============================================================
# FUNCIONES DE IMAGEN
# ============================================================

FORMATOS_OK = (".jpg", ".jpeg", ".png", ".gif")

def seleccionar_imagen(lbl_preview, var_ruta):
    """Abre el explorador, valida la imagen y muestra un preview."""
    if not PIL_OK:
        messagebox.showerror("Error", "Instala Pillow para usar imágenes:\npip install Pillow")
        return
    ruta = filedialog.askopenfilename(
        title="Seleccionar imagen",
        filetypes=[("Imágenes", "*.jpg *.jpeg *.png *.gif")]
    )
    if not ruta:
        return
    # Validar formato
    ext = os.path.splitext(ruta)[1].lower()
    if ext not in FORMATOS_OK:
        messagebox.showerror("Formato inválido", f"No se permite '{ext}'.\nUsa JPG, PNG o GIF.")
        return
    # Validar tamaño (máx 5 MB)
    tam_mb = os.path.getsize(ruta) / (1024 * 1024)
    if tam_mb > 5:
        messagebox.showerror("Imagen muy grande", f"Pesa {tam_mb:.1f} MB. El máximo es 5 MB.")
        return
    # Guardar ruta y mostrar preview
    var_ruta.set(ruta)
    try:
        img = Image.open(ruta)
        img.thumbnail((120, 100))
        foto = ImageTk.PhotoImage(img)
        lbl_preview.config(image=foto, text="")
        lbl_preview.image = foto  # evitar que el garbage collector la elimine
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar la imagen:\n{e}")


def guardar_imagen(ruta_origen, nombre_archivo):
    """Copia y redimensiona la imagen a la carpeta del sistema. Devuelve la ruta destino."""
    if not PIL_OK or not ruta_origen:
        return None
    try:
        ext = os.path.splitext(ruta_origen)[1].lower()
        if ext == ".gif":
            ext = ".png"  # convertir GIF animado a PNG estático
        destino = os.path.join(CARPETA_IMG, f"{nombre_archivo}{ext}")
        img = Image.open(ruta_origen)
        img.thumbnail((800, 600))  # redimensionar si es muy grande
        img.save(destino)
        return destino
    except Exception as e:
        messagebox.showerror("Error al guardar imagen", str(e))
        return None

# ============================================================
# CONEXIÓN A LA BASE DE DATOS
# ============================================================

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="construdata"
    )


# ============================================================
# VALIDACIONES SIMPLES
# ============================================================

def es_vacio(valor):
    return valor.strip() == ""

def es_numero(valor):
    try:
        float(valor)
        return True
    except ValueError:
        return False

def es_email_valido(valor):
    return re.match(r'^[\w\.\+\-]+@[\w\-]+\.[a-zA-Z]{2,}$', valor.strip()) is not None


# ============================================================
# EXPORTAR A EXCEL
# ============================================================

def exportar_excel(titulo, columnas, filas):
    try:
        import openpyxl
    except ImportError:
        messagebox.showerror("Error", "Instala openpyxl:\npip install openpyxl")
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Excel", "*.xlsx")],
        initialfile=f"{titulo}.xlsx"
    )
    if not ruta:
        return

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = titulo

    # Encabezados en negrita
    for col_num, nombre in enumerate(columnas, 1):
        celda = ws.cell(row=1, column=col_num, value=nombre)
        celda.font = openpyxl.styles.Font(bold=True)

    # Datos
    for fila_num, fila in enumerate(filas, 2):
        for col_num, valor in enumerate(fila, 1):
            ws.cell(row=fila_num, column=col_num, value=valor)

    wb.save(ruta)
    messagebox.showinfo("Listo", f"Excel guardado en:\n{ruta}")


# ============================================================
# EXPORTAR A PDF
# ============================================================

def exportar_pdf(titulo, columnas, filas):
    try:
        from fpdf import FPDF
    except ImportError:
        messagebox.showerror("Error", "Instala fpdf2:\npip install fpdf2")
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".pdf",
        filetypes=[("PDF", "*.pdf")],
        initialfile=f"{titulo}.pdf"
    )
    if not ruta:
        return

    pdf = FPDF(orientation="L", format="A4")
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(0, 10, f"Reporte: {titulo}", ln=True, align="C")
    pdf.ln(4)

    ancho_col = (pdf.w - 20) / len(columnas)

    # Encabezados
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_fill_color(200, 200, 200)
    for col in columnas:
        pdf.cell(ancho_col, 8, str(col)[:18], border=1, fill=True, align="C")
    pdf.ln()

    # Filas
    pdf.set_font("Helvetica", "", 8)
    for fila in filas:
        for valor in fila:
            texto = str(valor)[:18] if valor is not None else ""
            pdf.cell(ancho_col, 7, texto, border=1)
        pdf.ln()

    pdf.output(ruta)
    messagebox.showinfo("Listo", f"PDF guardado en:\n{ruta}")


# ============================================================
# VENTANA PRINCIPAL
# ============================================================

ventana = Tk()
ventana.title("Sistema ConstruData")
ventana.geometry("950x600")
ventana.resizable(True, True)

notebook = ttk.Notebook(ventana)
notebook.pack(fill="both", expand=True, padx=10, pady=10)


# ============================================================
# PESTAÑA PROYECTOS
# ============================================================

tab_proy = Frame(notebook)
notebook.add(tab_proy, text="  Proyectos  ")

# --- Formulario ---
frm = LabelFrame(tab_proy, text="Datos del proyecto", padx=10, pady=10)
frm.pack(side=LEFT, fill="y", padx=10, pady=10)

Label(frm, text="Código *").grid(row=0, column=0, sticky="w", pady=3)
e_proy_cod = Entry(frm, width=22)
e_proy_cod.grid(row=0, column=1, pady=3)

Label(frm, text="Nombre *").grid(row=1, column=0, sticky="w", pady=3)
e_proy_nom = Entry(frm, width=22)
e_proy_nom.grid(row=1, column=1, pady=3)

Label(frm, text="Dirección").grid(row=2, column=0, sticky="w", pady=3)
e_proy_dir = Entry(frm, width=22)
e_proy_dir.grid(row=2, column=1, pady=3)

Label(frm, text="Tipo").grid(row=3, column=0, sticky="w", pady=3)
e_proy_tipo = Entry(frm, width=22)
e_proy_tipo.grid(row=3, column=1, pady=3)

Label(frm, text="Área m²").grid(row=4, column=0, sticky="w", pady=3)
e_proy_area = Entry(frm, width=22)
e_proy_area.grid(row=4, column=1, pady=3)

Label(frm, text="Pisos").grid(row=5, column=0, sticky="w", pady=3)
e_proy_pisos = Entry(frm, width=22)
e_proy_pisos.grid(row=5, column=1, pady=3)

Label(frm, text="Estado").grid(row=6, column=0, sticky="w", pady=3)
e_proy_estado = Entry(frm, width=22)
e_proy_estado.grid(row=6, column=1, pady=3)

Label(frm, text="Presupuesto").grid(row=7, column=0, sticky="w", pady=3)
e_proy_pre = Entry(frm, width=22)
e_proy_pre.grid(row=7, column=1, pady=3)

Label(frm, text="Gerente").grid(row=8, column=0, sticky="w", pady=3)
e_proy_ger = Entry(frm, width=22)
e_proy_ger.grid(row=8, column=1, pady=3)

# --- Imagen del proyecto ---
frm_img_proy = LabelFrame(frm, text="Imagen del proyecto", padx=6, pady=6)
frm_img_proy.grid(row=9, column=0, columnspan=2, sticky="ew", pady=6)

lbl_img_proy = Label(frm_img_proy, text="Sin imagen", width=16, height=6,
                     relief="groove", bg="#f0f0f0")
lbl_img_proy.pack(side=LEFT, padx=6)

var_img_proy = StringVar()

frm_img_proy_btns = Frame(frm_img_proy)
frm_img_proy_btns.pack(side=LEFT, padx=8)
Button(frm_img_proy_btns, text="📁 Seleccionar imagen",
       command=lambda: seleccionar_imagen(lbl_img_proy, var_img_proy),
       width=20).pack(pady=3)
Button(frm_img_proy_btns, text="🗑 Quitar imagen",
       command=lambda: [var_img_proy.set(""),
                        lbl_img_proy.config(image="", text="Sin imagen")],
       width=20).pack(pady=3)
Label(frm_img_proy_btns, text="JPG, PNG, GIF — Máx. 5 MB",
      fg="gray", font=("Arial", 8)).pack()

def limpiar_proyectos():
    for e in [e_proy_cod, e_proy_nom, e_proy_dir, e_proy_tipo,
              e_proy_area, e_proy_pisos, e_proy_estado, e_proy_pre, e_proy_ger]:
        e.delete(0, END)
    var_img_proy.set("")
    lbl_img_proy.config(image="", text="Sin imagen")

def registrar_proyecto():
    if es_vacio(e_proy_cod.get()) or es_vacio(e_proy_nom.get()):
        messagebox.showwarning("Atención", "Código y Nombre son obligatorios.")
        return
    if e_proy_area.get() and not es_numero(e_proy_area.get()):
        messagebox.showwarning("Atención", "El Área debe ser un número.")
        return
    if e_proy_pisos.get() and not es_numero(e_proy_pisos.get()):
        messagebox.showwarning("Atención", "Los Pisos deben ser un número.")
        return
    if e_proy_pre.get() and not es_numero(e_proy_pre.get()):
        messagebox.showwarning("Atención", "El Presupuesto debe ser un número.")
        return
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id_proyecto FROM proyectos WHERE codigo=%s", (e_proy_cod.get(),))
        if cur.fetchone():
            messagebox.showerror("Error", "Ya existe un proyecto con ese código.")
            con.close()
            return
        cur.execute("""
            INSERT INTO proyectos
                (codigo, nombre, direccion, tipo_construccion,
                 area_total, cantidad_pisos, estado, presupuesto, gerente_proyecto)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            e_proy_cod.get(), e_proy_nom.get(), e_proy_dir.get(), e_proy_tipo.get(),
            e_proy_area.get() or None, e_proy_pisos.get() or None,
            e_proy_estado.get(), e_proy_pre.get() or None, e_proy_ger.get()
        ))
        con.commit()
        con.close()
        # Guardar imagen si se seleccionó una
        if var_img_proy.get():
            guardar_imagen(var_img_proy.get(), f"proyecto_{e_proy_cod.get()}")
        messagebox.showinfo("Listo", "Proyecto registrado correctamente.")
        limpiar_proyectos()
        ver_proyectos()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

def ver_proyectos():
    for fila in tv_proy.get_children():
        tv_proy.delete(fila)
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id_proyecto, codigo, nombre, direccion, tipo_construccion, "
                    "area_total, cantidad_pisos, estado, presupuesto, gerente_proyecto FROM proyectos")
        for row in cur.fetchall():
            tv_proy.insert("", END, values=row)
        con.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

def eliminar_proyecto():
    sel = tv_proy.selection()
    if not sel:
        messagebox.showwarning("Atención", "Selecciona un proyecto de la tabla.")
        return
    valores = tv_proy.item(sel[0])["values"]
    if not messagebox.askyesno("Confirmar", f"¿Eliminar el proyecto '{valores[2]}'?"):
        return
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM proyectos WHERE id_proyecto=%s", (valores[0],))
        con.commit()
        con.close()
        messagebox.showinfo("Listo", "Proyecto eliminado.")
        ver_proyectos()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

# --- Botones ---
frm_btns = Frame(frm)
frm_btns.grid(row=10, column=0, columnspan=2, pady=10)

Button(frm_btns, text="Registrar",   command=registrar_proyecto, bg="#2e7d32", fg="white", width=10).grid(row=0, column=0, padx=4)
Button(frm_btns, text="Ver todos",   command=ver_proyectos,      bg="#1565c0", fg="white", width=10).grid(row=0, column=1, padx=4)
Button(frm_btns, text="Eliminar",    command=eliminar_proyecto,  bg="#c62828", fg="white", width=10).grid(row=1, column=0, padx=4, pady=4)
Button(frm_btns, text="Limpiar",     command=limpiar_proyectos,  bg="#555555", fg="white", width=10).grid(row=1, column=1, padx=4, pady=4)

COLS_PROY = ("ID","Código","Nombre","Dirección","Tipo","Área","Pisos","Estado","Presupuesto","Gerente")
Button(frm_btns, text="Exportar Excel", command=lambda: exportar_excel(
    "Proyectos", COLS_PROY,
    [tv_proy.item(i)["values"] for i in tv_proy.get_children()]
), bg="#217346", fg="white", width=22).grid(row=2, column=0, columnspan=2, pady=2)

Button(frm_btns, text="Exportar PDF", command=lambda: exportar_pdf(
    "Proyectos", COLS_PROY,
    [tv_proy.item(i)["values"] for i in tv_proy.get_children()]
), bg="#b71c1c", fg="white", width=22).grid(row=3, column=0, columnspan=2, pady=2)

# --- Tabla ---
frm_tabla = Frame(tab_proy)
frm_tabla.pack(side=LEFT, fill="both", expand=True, padx=10, pady=10)

tv_proy = ttk.Treeview(frm_tabla, columns=COLS_PROY, show="headings", height=18)
for col in COLS_PROY:
    tv_proy.heading(col, text=col)
    tv_proy.column(col, width=90, anchor="center")

sb_v = ttk.Scrollbar(frm_tabla, orient="vertical",   command=tv_proy.yview)
sb_h = ttk.Scrollbar(frm_tabla, orient="horizontal", command=tv_proy.xview)
tv_proy.configure(yscrollcommand=sb_v.set, xscrollcommand=sb_h.set)
sb_v.pack(side=RIGHT, fill="y")
sb_h.pack(side=BOTTOM, fill="x")
tv_proy.pack(fill="both", expand=True)

ver_proyectos()


# ============================================================
# PESTAÑA EMPLEADOS
# ============================================================

tab_emp = Frame(notebook)
notebook.add(tab_emp, text="  Empleados  ")

frm2 = LabelFrame(tab_emp, text="Datos del empleado", padx=10, pady=10)
frm2.pack(side=LEFT, fill="y", padx=10, pady=10)

Label(frm2, text="DNI *").grid(row=0, column=0, sticky="w", pady=3)
e_emp_dni = Entry(frm2, width=22)
e_emp_dni.grid(row=0, column=1, pady=3)

Label(frm2, text="Nombres *").grid(row=1, column=0, sticky="w", pady=3)
e_emp_nom = Entry(frm2, width=22)
e_emp_nom.grid(row=1, column=1, pady=3)

Label(frm2, text="Apellidos *").grid(row=2, column=0, sticky="w", pady=3)
e_emp_ape = Entry(frm2, width=22)
e_emp_ape.grid(row=2, column=1, pady=3)

Label(frm2, text="Teléfono").grid(row=3, column=0, sticky="w", pady=3)
e_emp_tel = Entry(frm2, width=22)
e_emp_tel.grid(row=3, column=1, pady=3)

Label(frm2, text="Cargo").grid(row=4, column=0, sticky="w", pady=3)
e_emp_car = Entry(frm2, width=22)
e_emp_car.grid(row=4, column=1, pady=3)

Label(frm2, text="Salario").grid(row=5, column=0, sticky="w", pady=3)
e_emp_sal = Entry(frm2, width=22)
e_emp_sal.grid(row=5, column=1, pady=3)

Label(frm2, text="Tipo contrato").grid(row=6, column=0, sticky="w", pady=3)
e_emp_cont = Entry(frm2, width=22)
e_emp_cont.grid(row=6, column=1, pady=3)

# --- Foto del empleado ---
frm_img_emp = LabelFrame(frm2, text="Foto del empleado", padx=6, pady=6)
frm_img_emp.grid(row=7, column=0, columnspan=2, sticky="ew", pady=6)

lbl_img_emp = Label(frm_img_emp, text="Sin foto", width=16, height=6,
                    relief="groove", bg="#f0f0f0")
lbl_img_emp.pack(side=LEFT, padx=6)

var_img_emp = StringVar()

frm_img_emp_btns = Frame(frm_img_emp)
frm_img_emp_btns.pack(side=LEFT, padx=8)
Button(frm_img_emp_btns, text="📁 Seleccionar foto",
       command=lambda: seleccionar_imagen(lbl_img_emp, var_img_emp),
       width=20).pack(pady=3)
Button(frm_img_emp_btns, text="🗑 Quitar foto",
       command=lambda: [var_img_emp.set(""),
                        lbl_img_emp.config(image="", text="Sin foto")],
       width=20).pack(pady=3)
Label(frm_img_emp_btns, text="JPG, PNG, GIF — Máx. 5 MB",
      fg="gray", font=("Arial", 8)).pack()

def limpiar_empleados():
    for e in [e_emp_dni, e_emp_nom, e_emp_ape, e_emp_tel,
              e_emp_car, e_emp_sal, e_emp_cont]:
        e.delete(0, END)
    var_img_emp.set("")
    lbl_img_emp.config(image="", text="Sin foto")

def registrar_empleado():
    if es_vacio(e_emp_dni.get()) or es_vacio(e_emp_nom.get()) or es_vacio(e_emp_ape.get()):
        messagebox.showwarning("Atención", "DNI, Nombres y Apellidos son obligatorios.")
        return
    if e_emp_sal.get() and not es_numero(e_emp_sal.get()):
        messagebox.showwarning("Atención", "El Salario debe ser un número.")
        return
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id_empleado FROM empleados WHERE dni=%s", (e_emp_dni.get(),))
        if cur.fetchone():
            messagebox.showerror("Error", "Ya existe un empleado con ese DNI.")
            con.close()
            return
        cur.execute("""
            INSERT INTO empleados (dni, nombres, apellidos, telefono, cargo, salario, tipo_contrato)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, (
            e_emp_dni.get(), e_emp_nom.get(), e_emp_ape.get(),
            e_emp_tel.get(), e_emp_car.get(),
            e_emp_sal.get() or None, e_emp_cont.get()
        ))
        con.commit()
        con.close()
        # Guardar foto si se seleccionó una
        if var_img_emp.get():
            guardar_imagen(var_img_emp.get(), f"empleado_{e_emp_dni.get()}")
        messagebox.showinfo("Listo", "Empleado registrado correctamente.")
        limpiar_empleados()
        ver_empleados()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

def ver_empleados():
    for fila in tv_emp.get_children():
        tv_emp.delete(fila)
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id_empleado, dni, nombres, apellidos, "
                    "telefono, cargo, salario, tipo_contrato FROM empleados")
        for row in cur.fetchall():
            tv_emp.insert("", END, values=row)
        con.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

def eliminar_empleado():
    sel = tv_emp.selection()
    if not sel:
        messagebox.showwarning("Atención", "Selecciona un empleado de la tabla.")
        return
    valores = tv_emp.item(sel[0])["values"]
    if not messagebox.askyesno("Confirmar", f"¿Eliminar a '{valores[2]} {valores[3]}'?"):
        return
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM empleados WHERE id_empleado=%s", (valores[0],))
        con.commit()
        con.close()
        messagebox.showinfo("Listo", "Empleado eliminado.")
        ver_empleados()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

frm2_btns = Frame(frm2)
frm2_btns.grid(row=8, column=0, columnspan=2, pady=10)

Button(frm2_btns, text="Registrar",  command=registrar_empleado, bg="#2e7d32", fg="white", width=10).grid(row=0, column=0, padx=4)
Button(frm2_btns, text="Ver todos",  command=ver_empleados,      bg="#1565c0", fg="white", width=10).grid(row=0, column=1, padx=4)
Button(frm2_btns, text="Eliminar",   command=eliminar_empleado,  bg="#c62828", fg="white", width=10).grid(row=1, column=0, padx=4, pady=4)
Button(frm2_btns, text="Limpiar",    command=limpiar_empleados,  bg="#555555", fg="white", width=10).grid(row=1, column=1, padx=4, pady=4)

COLS_EMP = ("ID","DNI","Nombres","Apellidos","Teléfono","Cargo","Salario","Contrato")
Button(frm2_btns, text="Exportar Excel", command=lambda: exportar_excel(
    "Empleados", COLS_EMP,
    [tv_emp.item(i)["values"] for i in tv_emp.get_children()]
), bg="#217346", fg="white", width=22).grid(row=2, column=0, columnspan=2, pady=2)

Button(frm2_btns, text="Exportar PDF", command=lambda: exportar_pdf(
    "Empleados", COLS_EMP,
    [tv_emp.item(i)["values"] for i in tv_emp.get_children()]
), bg="#b71c1c", fg="white", width=22).grid(row=3, column=0, columnspan=2, pady=2)

frm2_tabla = Frame(tab_emp)
frm2_tabla.pack(side=LEFT, fill="both", expand=True, padx=10, pady=10)

tv_emp = ttk.Treeview(frm2_tabla, columns=COLS_EMP, show="headings", height=18)
for col in COLS_EMP:
    tv_emp.heading(col, text=col)
    tv_emp.column(col, width=100, anchor="center")

sb2_v = ttk.Scrollbar(frm2_tabla, orient="vertical",   command=tv_emp.yview)
sb2_h = ttk.Scrollbar(frm2_tabla, orient="horizontal", command=tv_emp.xview)
tv_emp.configure(yscrollcommand=sb2_v.set, xscrollcommand=sb2_h.set)
sb2_v.pack(side=RIGHT, fill="y")
sb2_h.pack(side=BOTTOM, fill="x")
tv_emp.pack(fill="both", expand=True)

ver_empleados()


# ============================================================
# PESTAÑA MATERIALES
# ============================================================

tab_mat = Frame(notebook)
notebook.add(tab_mat, text="  Materiales  ")

frm3 = LabelFrame(tab_mat, text="Datos del material", padx=10, pady=10)
frm3.pack(side=LEFT, fill="y", padx=10, pady=10)

Label(frm3, text="Código *").grid(row=0, column=0, sticky="w", pady=3)
e_mat_cod = Entry(frm3, width=22)
e_mat_cod.grid(row=0, column=1, pady=3)

Label(frm3, text="Descripción *").grid(row=1, column=0, sticky="w", pady=3)
e_mat_des = Entry(frm3, width=22)
e_mat_des.grid(row=1, column=1, pady=3)

Label(frm3, text="Categoría").grid(row=2, column=0, sticky="w", pady=3)
e_mat_cat = Entry(frm3, width=22)
e_mat_cat.grid(row=2, column=1, pady=3)

Label(frm3, text="Unidad medida").grid(row=3, column=0, sticky="w", pady=3)
e_mat_uni = Entry(frm3, width=22)
e_mat_uni.grid(row=3, column=1, pady=3)

Label(frm3, text="ID Proveedor").grid(row=4, column=0, sticky="w", pady=3)
e_mat_pro = Entry(frm3, width=22)
e_mat_pro.grid(row=4, column=1, pady=3)
Label(frm3, text="(número, opcional)", fg="gray", font=("Arial", 8)).grid(
    row=5, column=1, sticky="w")

def limpiar_materiales():
    for e in [e_mat_cod, e_mat_des, e_mat_cat, e_mat_uni, e_mat_pro]:
        e.delete(0, END)

def registrar_material():
    if es_vacio(e_mat_cod.get()) or es_vacio(e_mat_des.get()):
        messagebox.showwarning("Atención", "Código y Descripción son obligatorios.")
        return
    if e_mat_pro.get() and not es_numero(e_mat_pro.get()):
        messagebox.showwarning("Atención", "El ID Proveedor debe ser un número.")
        return
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id_material FROM materiales WHERE codigo=%s", (e_mat_cod.get(),))
        if cur.fetchone():
            messagebox.showerror("Error", "Ya existe un material con ese código.")
            con.close()
            return
        cur.execute("""
            INSERT INTO materiales (codigo, descripcion, categoria, unidad_medida, proveedor_preferido)
            VALUES (%s,%s,%s,%s,%s)
        """, (
            e_mat_cod.get(), e_mat_des.get(), e_mat_cat.get(),
            e_mat_uni.get(), e_mat_pro.get() or None
        ))
        con.commit()
        con.close()
        messagebox.showinfo("Listo", "Material registrado correctamente.")
        limpiar_materiales()
        ver_materiales()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

def ver_materiales():
    for fila in tv_mat.get_children():
        tv_mat.delete(fila)
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id_material, codigo, descripcion, categoria, "
                    "unidad_medida, proveedor_preferido FROM materiales")
        for row in cur.fetchall():
            tv_mat.insert("", END, values=row)
        con.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

def eliminar_material():
    sel = tv_mat.selection()
    if not sel:
        messagebox.showwarning("Atención", "Selecciona un material de la tabla.")
        return
    valores = tv_mat.item(sel[0])["values"]
    if not messagebox.askyesno("Confirmar", f"¿Eliminar el material '{valores[2]}'?"):
        return
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM materiales WHERE id_material=%s", (valores[0],))
        con.commit()
        con.close()
        messagebox.showinfo("Listo", "Material eliminado.")
        ver_materiales()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

frm3_btns = Frame(frm3)
frm3_btns.grid(row=6, column=0, columnspan=2, pady=10)

Button(frm3_btns, text="Registrar",  command=registrar_material, bg="#2e7d32", fg="white", width=10).grid(row=0, column=0, padx=4)
Button(frm3_btns, text="Ver todos",  command=ver_materiales,     bg="#1565c0", fg="white", width=10).grid(row=0, column=1, padx=4)
Button(frm3_btns, text="Eliminar",   command=eliminar_material,  bg="#c62828", fg="white", width=10).grid(row=1, column=0, padx=4, pady=4)
Button(frm3_btns, text="Limpiar",    command=limpiar_materiales, bg="#555555", fg="white", width=10).grid(row=1, column=1, padx=4, pady=4)

COLS_MAT = ("ID","Código","Descripción","Categoría","Unidad","ID Proveedor")
Button(frm3_btns, text="Exportar Excel", command=lambda: exportar_excel(
    "Materiales", COLS_MAT,
    [tv_mat.item(i)["values"] for i in tv_mat.get_children()]
), bg="#217346", fg="white", width=22).grid(row=2, column=0, columnspan=2, pady=2)

Button(frm3_btns, text="Exportar PDF", command=lambda: exportar_pdf(
    "Materiales", COLS_MAT,
    [tv_mat.item(i)["values"] for i in tv_mat.get_children()]
), bg="#b71c1c", fg="white", width=22).grid(row=3, column=0, columnspan=2, pady=2)

frm3_tabla = Frame(tab_mat)
frm3_tabla.pack(side=LEFT, fill="both", expand=True, padx=10, pady=10)

tv_mat = ttk.Treeview(frm3_tabla, columns=COLS_MAT, show="headings", height=18)
for col in COLS_MAT:
    tv_mat.heading(col, text=col)
    tv_mat.column(col, width=120, anchor="center")

sb3_v = ttk.Scrollbar(frm3_tabla, orient="vertical",   command=tv_mat.yview)
sb3_h = ttk.Scrollbar(frm3_tabla, orient="horizontal", command=tv_mat.xview)
tv_mat.configure(yscrollcommand=sb3_v.set, xscrollcommand=sb3_h.set)
sb3_v.pack(side=RIGHT, fill="y")
sb3_h.pack(side=BOTTOM, fill="x")
tv_mat.pack(fill="both", expand=True)

ver_materiales()


# ============================================================
# PESTAÑA PROVEEDORES
# ============================================================

tab_pro = Frame(notebook)
notebook.add(tab_pro, text="  Proveedores  ")

frm4 = LabelFrame(tab_pro, text="Datos del proveedor", padx=10, pady=10)
frm4.pack(side=LEFT, fill="y", padx=10, pady=10)

Label(frm4, text="Nombre *").grid(row=0, column=0, sticky="w", pady=3)
e_pro_nom = Entry(frm4, width=22)
e_pro_nom.grid(row=0, column=1, pady=3)

Label(frm4, text="Teléfono").grid(row=1, column=0, sticky="w", pady=3)
e_pro_tel = Entry(frm4, width=22)
e_pro_tel.grid(row=1, column=1, pady=3)

Label(frm4, text="Dirección").grid(row=2, column=0, sticky="w", pady=3)
e_pro_dir = Entry(frm4, width=22)
e_pro_dir.grid(row=2, column=1, pady=3)

Label(frm4, text="Email *").grid(row=3, column=0, sticky="w", pady=3)
e_pro_mail = Entry(frm4, width=22)
e_pro_mail.grid(row=3, column=1, pady=3)
Label(frm4, text="Ej: correo@dominio.com", fg="gray", font=("Arial", 8)).grid(
    row=4, column=1, sticky="w")

def limpiar_proveedores():
    for e in [e_pro_nom, e_pro_tel, e_pro_dir, e_pro_mail]:
        e.delete(0, END)

def registrar_proveedor():
    if es_vacio(e_pro_nom.get()):
        messagebox.showwarning("Atención", "El Nombre es obligatorio.")
        return
    if not es_vacio(e_pro_mail.get()) and not es_email_valido(e_pro_mail.get()):
        messagebox.showwarning("Atención", "El email no tiene un formato válido.\nEjemplo: correo@dominio.com")
        return
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id_proveedor FROM proveedores WHERE nombre=%s AND telefono=%s",
                    (e_pro_nom.get(), e_pro_tel.get()))
        if cur.fetchone():
            messagebox.showerror("Error", "Ya existe ese proveedor.")
            con.close()
            return
        cur.execute("""
            INSERT INTO proveedores (nombre, telefono, direccion, email)
            VALUES (%s,%s,%s,%s)
        """, (e_pro_nom.get(), e_pro_tel.get(), e_pro_dir.get(), e_pro_mail.get()))
        con.commit()
        con.close()
        messagebox.showinfo("Listo", "Proveedor registrado correctamente.")
        limpiar_proveedores()
        ver_proveedores()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

def ver_proveedores():
    for fila in tv_pro.get_children():
        tv_pro.delete(fila)
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("SELECT id_proveedor, nombre, telefono, direccion, email FROM proveedores")
        for row in cur.fetchall():
            tv_pro.insert("", END, values=row)
        con.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

def eliminar_proveedor():
    sel = tv_pro.selection()
    if not sel:
        messagebox.showwarning("Atención", "Selecciona un proveedor de la tabla.")
        return
    valores = tv_pro.item(sel[0])["values"]
    if not messagebox.askyesno("Confirmar", f"¿Eliminar al proveedor '{valores[1]}'?"):
        return
    try:
        con = conectar()
        cur = con.cursor()
        cur.execute("DELETE FROM proveedores WHERE id_proveedor=%s", (valores[0],))
        con.commit()
        con.close()
        messagebox.showinfo("Listo", "Proveedor eliminado.")
        ver_proveedores()
    except mysql.connector.Error as err:
        messagebox.showerror("Error MySQL", str(err))

frm4_btns = Frame(frm4)
frm4_btns.grid(row=5, column=0, columnspan=2, pady=10)

Button(frm4_btns, text="Registrar",  command=registrar_proveedor, bg="#2e7d32", fg="white", width=10).grid(row=0, column=0, padx=4)
Button(frm4_btns, text="Ver todos",  command=ver_proveedores,     bg="#1565c0", fg="white", width=10).grid(row=0, column=1, padx=4)
Button(frm4_btns, text="Eliminar",   command=eliminar_proveedor,  bg="#c62828", fg="white", width=10).grid(row=1, column=0, padx=4, pady=4)
Button(frm4_btns, text="Limpiar",    command=limpiar_proveedores, bg="#555555", fg="white", width=10).grid(row=1, column=1, padx=4, pady=4)

COLS_PRO = ("ID","Nombre","Teléfono","Dirección","Email")
Button(frm4_btns, text="Exportar Excel", command=lambda: exportar_excel(
    "Proveedores", COLS_PRO,
    [tv_pro.item(i)["values"] for i in tv_pro.get_children()]
), bg="#217346", fg="white", width=22).grid(row=2, column=0, columnspan=2, pady=2)

Button(frm4_btns, text="Exportar PDF", command=lambda: exportar_pdf(
    "Proveedores", COLS_PRO,
    [tv_pro.item(i)["values"] for i in tv_pro.get_children()]
), bg="#b71c1c", fg="white", width=22).grid(row=3, column=0, columnspan=2, pady=2)

frm4_tabla = Frame(tab_pro)
frm4_tabla.pack(side=LEFT, fill="both", expand=True, padx=10, pady=10)

tv_pro = ttk.Treeview(frm4_tabla, columns=COLS_PRO, show="headings", height=18)
for col in COLS_PRO:
    tv_pro.heading(col, text=col)
    tv_pro.column(col, width=140, anchor="center")

sb4_v = ttk.Scrollbar(frm4_tabla, orient="vertical",   command=tv_pro.yview)
sb4_h = ttk.Scrollbar(frm4_tabla, orient="horizontal", command=tv_pro.xview)
tv_pro.configure(yscrollcommand=sb4_v.set, xscrollcommand=sb4_h.set)
sb4_v.pack(side=RIGHT, fill="y")
sb4_h.pack(side=BOTTOM, fill="x")
tv_pro.pack(fill="both", expand=True)

ver_proveedores()


# ============================================================
ventana.mainloop()