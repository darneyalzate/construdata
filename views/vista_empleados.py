import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
"""
views/vista_empleados.py — con soporte de temas reactivos
"""
import tkinter as tk
from tkinter import ttk

from views.vista_base import (VistaBase, FUENTE_LABEL, FUENTE_ENTRADA,
                               crear_boton, crear_campo_fecha,
                               crear_entry_numerico, CALENDAR_OK)
from utils.temas import tm
from controllers.controladores import EmpleadoController
from models.modelos import Empleado
from utils.utilidades import (es_vacio, es_numero, es_entero,
                               seleccionar_imagen, guardar_imagen,
                               cargar_preview, exportar_excel, exportar_pdf)

COLS = ("ID", "DNI", "Nombres", "Apellidos", "Teléfono",
        "Cargo", "Salario", "Contrato", "Email", "F.Ingreso")


class VistaEmpleados(VistaBase):

    def __init__(self, notebook: ttk.Notebook):
        self.tab = tk.Frame(notebook, bg=tm().color("fondo"))
        notebook.add(self.tab, text="  👷 Empleados  ")
        self._id_seleccionado = None
        self._var_foto = tk.StringVar()
        self._widgets_tema = []
        self._construir_ui()
        self._registrar_en_tema()
        self.ver_todos()

    # ══════════════════════════════════════════════════════════════
    #  UI
    # ══════════════════════════════════════════════════════════════

    def _construir_ui(self):
        self._izq = tk.Frame(self.tab, bg=tm().color("fondo"), width=300)
        self._izq.pack(side="left", fill="y", padx=(10, 4), pady=10)
        self._izq.pack_propagate(False)
        self._der = tk.Frame(self.tab, bg=tm().color("fondo"))
        self._der.pack(side="left", fill="both", expand=True, padx=(4, 10), pady=10)
        self._construir_formulario(self._izq)
        self._construir_filtros(self._der)
        self.tv = self.construir_tabla(self._der, COLS, alturas=16)

    def _mk_label(self, parent, texto):
        lbl = tk.Label(parent, text=texto, font=FUENTE_LABEL,
                       bg=tm().color("fondo_frm"), fg=tm().color("texto"))
        self._widgets_tema.append((lbl, "fondo_frm", "texto"))
        return lbl

    def _mk_entry(self, parent, width=22):
        e = tk.Entry(parent, width=width, font=FUENTE_ENTRADA,
                     bg=tm().color("fondo_entrada"), fg=tm().color("texto"),
                     insertbackground=tm().color("texto"),
                     highlightbackground=tm().color("borde"),
                     highlightcolor=tm().color("primario"),
                     highlightthickness=1, relief="flat")
        self._widgets_tema.append((e, "fondo_entrada", "texto"))
        return e

    def _construir_formulario(self, parent):
        self._frm = ttk.LabelFrame(parent, text="Datos del Empleado")
        self._frm.pack(fill="both", expand=True, padx=4, pady=4)

        campos = [
            ("DNI *",         "e_dni",      "text"),
            ("Nombres *",     "e_nombres",  "text"),
            ("Apellidos *",   "e_apellidos","text"),
            ("Teléfono",      "e_tel",      "text"),
            ("Cargo",         "e_cargo",    "text"),
            ("Salario",       "e_salario",  "num"),
            ("Tipo Contrato", "e_contrato", "combo_contrato"),
            ("Email",         "e_email",    "text"),
            ("F. Ingreso",    "e_fingreso", "fecha"),
        ]

        for i, (etiq, attr, tipo) in enumerate(campos):
            self._mk_label(self._frm, etiq).grid(
                row=i, column=0, sticky="w", padx=6, pady=2)
            if tipo == "num":
                w = crear_entry_numerico(self._frm, width=20)
                self._widgets_tema.append((w, "fondo_entrada", "texto"))
            elif tipo == "fecha":
                w = crear_campo_fecha(self._frm)
            elif tipo == "combo_contrato":
                w = ttk.Combobox(self._frm, width=19, font=FUENTE_ENTRADA,
                                 values=["Indefinido", "Término fijo",
                                         "Obra o labor", "Prestación de servicios"])
                w.set("Indefinido")
            else:
                w = self._mk_entry(self._frm)
            w.grid(row=i, column=1, padx=6, pady=2, sticky="w")
            setattr(self, attr, w)

        # Foto
        self._frm_foto = ttk.LabelFrame(self._frm, text="Foto del Empleado")
        self._frm_foto.grid(row=len(campos), column=0, columnspan=2,
                            sticky="ew", padx=6, pady=6)
        self.lbl_foto = tk.Label(self._frm_foto, text="Sin foto",
                                 width=15, height=5, relief="groove",
                                 bg=tm().color("fondo_entrada"),
                                 fg=tm().color("texto_sec"))
        self.lbl_foto.pack(side="left", padx=6, pady=4)
        self._widgets_tema.append((self.lbl_foto, "fondo_entrada", "texto_sec"))

        frm_foto_btns = tk.Frame(self._frm_foto, bg=tm().color("fondo_frm"))
        frm_foto_btns.pack(side="left", padx=6)
        self._widgets_tema.append((frm_foto_btns, "fondo_frm", None))
        crear_boton(frm_foto_btns, "Seleccionar",
                    lambda: seleccionar_imagen(self.lbl_foto, self._var_foto),
                    "primario", 14, "📁").pack(pady=2)
        crear_boton(frm_foto_btns, "Quitar",
                    self._quitar_foto, "neutro", 14, "🗑").pack(pady=2)

        # Botones CRUD
        frm_btns = tk.Frame(self._frm, bg=tm().color("fondo_frm"))
        frm_btns.grid(row=len(campos) + 1, column=0, columnspan=2, pady=8)
        self._widgets_tema.append((frm_btns, "fondo_frm", None))
        self._construir_botones_crud(frm_btns)

    def _construir_botones_crud(self, parent):
        for fila_data in [
            [("💾 Registrar", self.registrar,  "secundario"),
             ("✏ Actualizar", self.actualizar, "advertencia")],
            [("🗑 Eliminar",  self.eliminar,   "peligro"),
             ("🔄 Limpiar",   self.limpiar,    "neutro")],
        ]:
            f = tk.Frame(parent, bg=tm().color("fondo_frm"))
            f.pack(pady=2)
            self._widgets_tema.append((f, "fondo_frm", None))
            for txt, cmd, col in fila_data:
                crear_boton(f, txt, cmd, col, 12).pack(side="left", padx=3)

        f3 = tk.Frame(parent, bg=tm().color("fondo_frm"))
        f3.pack(pady=2)
        self._widgets_tema.append((f3, "fondo_frm", None))
        crear_boton(f3, "📊 Exportar Excel",
                    self._exportar_excel, "excel", 16).pack(side="left", padx=3)
        crear_boton(f3, "📄 Exportar PDF",
                    self._exportar_pdf,   "pdf",   16).pack(side="left", padx=3)

    def _construir_filtros(self, parent):
        self._frm_f = tk.Frame(parent, bg=tm().color("fondo"))
        self._frm_f.pack(fill="x", pady=(0, 4))
        self._widgets_tema.append((self._frm_f, "fondo", None))

        lbl_b = tk.Label(self._frm_f, text="🔍 Buscar:", font=FUENTE_LABEL,
                         bg=tm().color("fondo"), fg=tm().color("texto"))
        lbl_b.pack(side="left", padx=4)
        self._widgets_tema.append((lbl_b, "fondo", "texto"))

        self.e_buscar = tk.Entry(self._frm_f, width=20, font=FUENTE_ENTRADA,
                                 bg=tm().color("fondo_entrada"),
                                 fg=tm().color("texto"),
                                 insertbackground=tm().color("texto"),
                                 relief="flat")
        self.e_buscar.pack(side="left", padx=4)
        self._widgets_tema.append((self.e_buscar, "fondo_entrada", "texto"))
        self.e_buscar.bind("<Return>", lambda e: self.buscar())

        lbl_c = tk.Label(self._frm_f, text="Cargo:", font=FUENTE_LABEL,
                         bg=tm().color("fondo"), fg=tm().color("texto"))
        lbl_c.pack(side="left", padx=4)
        self._widgets_tema.append((lbl_c, "fondo", "texto"))

        self.e_filtro_cargo = tk.Entry(self._frm_f, width=14, font=FUENTE_ENTRADA,
                                       bg=tm().color("fondo_entrada"),
                                       fg=tm().color("texto"), relief="flat")
        self.e_filtro_cargo.pack(side="left", padx=4)
        self._widgets_tema.append((self.e_filtro_cargo, "fondo_entrada", "texto"))

        crear_boton(self._frm_f, "Filtrar",
                    self.filtrar,    "primario",    8, "🔍").pack(side="left", padx=3)
        crear_boton(self._frm_f, "Ver todos",
                    self.ver_todos,  "primario_lt", 8, "📋").pack(side="left", padx=3)

    # ══════════════════════════════════════════════════════════════
    #  TEMA
    # ══════════════════════════════════════════════════════════════

    def _refrescar_tema(self):
        self.tab.configure(bg=tm().color("fondo"))
        self._izq.configure(bg=tm().color("fondo"))
        self._der.configure(bg=tm().color("fondo"))
        for widget, clave_bg, clave_fg in self._widgets_tema:
            try:
                kw = {"bg": tm().color(clave_bg)} if clave_bg else {}
                if clave_fg:
                    kw["fg"] = tm().color(clave_fg)
                if isinstance(widget, tk.Entry):
                    kw["insertbackground"] = tm().color("texto")
                widget.configure(**kw)
            except Exception:
                pass
        if hasattr(self, "tv"):
            self._actualizar_tags_tabla(self.tv)

    # ══════════════════════════════════════════════════════════════
    #  CRUD
    # ══════════════════════════════════════════════════════════════

    def _leer_campos(self):
        def gv(w):
            if isinstance(w, ttk.Combobox): return w.get()
            try: return w.get_date().strftime("%Y-%m-%d") if CALENDAR_OK else w.get()
            except AttributeError: return w.get()
        return dict(
            dni=self.e_dni.get().strip(),
            nombres=self.e_nombres.get().strip(),
            apellidos=self.e_apellidos.get().strip(),
            telefono=self.e_tel.get().strip(),
            cargo=self.e_cargo.get().strip(),
            salario=self.e_salario.get().strip(),
            contrato=gv(self.e_contrato),
            email=self.e_email.get().strip(),
            f_ingreso=gv(self.e_fingreso),
        )

    def _validar(self, d):
        if es_vacio(d["dni"]):
            self.advertencia("El DNI es obligatorio."); return False
        if es_vacio(d["nombres"]) or len(d["nombres"]) < 2:
            self.advertencia("El Nombre debe tener al menos 2 caracteres."); return False
        if es_vacio(d["apellidos"]) or len(d["apellidos"]) < 2:
            self.advertencia("Los Apellidos deben tener al menos 2 caracteres."); return False
        if d["salario"] and not es_numero(d["salario"]):
            self.advertencia("El Salario debe ser un número."); return False
        return True

    def registrar(self):
        d = self._leer_campos()
        if not self._validar(d): return
        if EmpleadoController.existe(d["dni"]):
            self.error(f"Ya existe un empleado con DNI '{d['dni']}'."); return
        e = Empleado(
            dni=d["dni"], nombres=d["nombres"], apellidos=d["apellidos"],
            telefono=d["telefono"], cargo=d["cargo"],
            salario=float(d["salario"]) if d["salario"] else None,
            tipo_contrato=d["contrato"], email=d["email"],
            fecha_ingreso=d["f_ingreso"]
        )
        if self._var_foto.get():
            e.foto = guardar_imagen(self._var_foto.get(), f"empleado_{d['dni']}")
        EmpleadoController.registrar(e)
        self.info("Empleado registrado correctamente.")
        self.limpiar(); self.ver_todos()

    def actualizar(self):
        if self._id_seleccionado is None:
            self.advertencia("Selecciona un empleado en la tabla primero."); return
        d = self._leer_campos()
        if not self._validar(d): return
        if not self.confirmar(f"¿Actualizar el empleado '{d['nombres']} {d['apellidos']}'?"): return
        e = Empleado(
            dni=d["dni"], nombres=d["nombres"], apellidos=d["apellidos"],
            telefono=d["telefono"], cargo=d["cargo"],
            salario=float(d["salario"]) if d["salario"] else None,
            tipo_contrato=d["contrato"], email=d["email"],
            fecha_ingreso=d["f_ingreso"], id_empleado=self._id_seleccionado
        )
        if self._var_foto.get():
            e.foto = guardar_imagen(self._var_foto.get(), f"empleado_{d['dni']}")
        EmpleadoController.actualizar(e)
        self.info("Empleado actualizado.")
        self.limpiar(); self.ver_todos()

    def eliminar(self):
        sel = self.tv.selection()
        if not sel:
            self.advertencia("Selecciona un empleado de la tabla."); return
        vals = self.tv.item(sel[0])["values"]
        if not self.confirmar(f"¿Eliminar a '{vals[2]} {vals[3]}'?\nEsta acción no se puede deshacer."):
            return
        EmpleadoController.eliminar(int(vals[0]))
        self.info("Empleado eliminado.")
        self.limpiar(); self.ver_todos()

    def limpiar(self):
        for attr in ["e_dni", "e_nombres", "e_apellidos", "e_tel",
                     "e_cargo", "e_salario", "e_email"]:
            w = getattr(self, attr)
            if isinstance(w, tk.Entry): w.delete(0, "end")
        if isinstance(self.e_contrato, ttk.Combobox):
            self.e_contrato.set("Indefinido")
        self._quitar_foto()
        self._id_seleccionado = None

    def _quitar_foto(self):
        self._var_foto.set("")
        self.lbl_foto.config(image="", text="Sin foto")

    # ══════════════════════════════════════════════════════════════
    #  CONSULTAS / TABLA
    # ══════════════════════════════════════════════════════════════

    def ver_todos(self):
        filas = EmpleadoController.listar()
        self.poblar_tabla(self.tv, [r[:10] for r in filas])
        self.tv.bind("<<TreeviewSelect>>", self._on_seleccion)

    def filtrar(self):
        filas = EmpleadoController.listar(filtro_cargo=self.e_filtro_cargo.get())
        self.poblar_tabla(self.tv, [r[:10] for r in filas])

    def buscar(self):
        t = self.e_buscar.get().strip()
        if not t: self.ver_todos(); return
        self.poblar_tabla(self.tv, EmpleadoController.buscar(t))

    def _on_seleccion(self, event=None):
        sel = self.tv.selection()
        if not sel: return
        vals = self.tv.item(sel[0])["values"]
        self._id_seleccionado = int(vals[0])
        for widget, valor in [
            (self.e_dni,      vals[1]), (self.e_nombres,   vals[2]),
            (self.e_apellidos,vals[3]), (self.e_tel,       vals[4]),
            (self.e_cargo,    vals[5]), (self.e_email,     vals[8]),
        ]:
            widget.delete(0, "end")
            widget.insert(0, str(valor) if valor else "")
        self.e_salario.delete(0, "end")
        if vals[6] and str(vals[6]) not in ("None", ""):
            self.e_salario.insert(0, str(vals[6]))
        if isinstance(self.e_contrato, ttk.Combobox):
            self.e_contrato.set(vals[7] if vals[7] else "Indefinido")

    # ══════════════════════════════════════════════════════════════
    #  EXPORTACIÓN
    # ══════════════════════════════════════════════════════════════

    def _exportar_excel(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos para exportar."); return
        exportar_excel("Empleados", list(COLS), filas,
                       f"Cargo: {self.e_filtro_cargo.get() or 'Todos'}")

    def _exportar_pdf(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos para exportar."); return
        exportar_pdf("Empleados", list(COLS), filas,
                     f"Cargo: {self.e_filtro_cargo.get() or 'Todos'}")