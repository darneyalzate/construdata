import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
"""
views/vista_proyectos.py  — con soporte de temas reactivos
"""
import tkinter as tk
from tkinter import ttk

from views.vista_base import (VistaBase, COLOR, FUENTE_LABEL, FUENTE_ENTRADA,
                               FUENTE_BTN, crear_boton, crear_campo_fecha,
                               crear_entry_numerico, CALENDAR_OK)
from utils.temas import tm
from controllers.controladores import ProyectoController
from models.modelos import Proyecto
from utils.utilidades import (es_vacio, es_numero, es_entero,
                               seleccionar_imagen, guardar_imagen,
                               cargar_preview, exportar_excel, exportar_pdf)

COLS = ("ID", "Código", "Nombre", "Dirección", "Tipo",
        "Área m²", "Pisos", "Estado", "Presupuesto", "Gerente", "F.Inicio", "F.Fin")


class VistaProyectos(VistaBase):

    def __init__(self, notebook: ttk.Notebook):
        self.tab = tk.Frame(notebook, bg=tm().color("fondo"))
        notebook.add(self.tab, text="  🏗 Proyectos  ")
        self._id_seleccionado = None
        self._var_img = tk.StringVar()
        self._widgets_tema = []
        self._construir_ui()
        self._registrar_en_tema()
        self.ver_todos()

    def _construir_ui(self):
        self._izq = tk.Frame(self.tab, bg=tm().color("fondo"), width=320)
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

    def _mk_entry(self, parent):
        e = tk.Entry(parent, width=22, font=FUENTE_ENTRADA,
                     bg=tm().color("fondo_entrada"), fg=tm().color("texto"),
                     insertbackground=tm().color("texto"),
                     highlightbackground=tm().color("borde"),
                     highlightcolor=tm().color("primario"),
                     highlightthickness=1, relief="flat")
        self._widgets_tema.append((e, "fondo_entrada", "texto"))
        return e

    def _construir_formulario(self, parent):
        self._frm = ttk.LabelFrame(parent, text="Datos del Proyecto")
        self._frm.pack(fill="both", expand=True, padx=4, pady=4)

        campos = [
            ("Código *",    "e_cod",   "text"),
            ("Nombre *",    "e_nom",   "text"),
            ("Dirección",   "e_dir",   "text"),
            ("Tipo",        "e_tipo",  "text"),
            ("Estado",      "e_est",   "combo_estado"),
            ("Gerente",     "e_ger",   "text"),
            ("Área m²",     "e_area",  "num"),
            ("Pisos",       "e_pisos", "num"),
            ("Presupuesto", "e_pre",   "num"),
            ("Fecha Inicio","e_fini",  "fecha"),
            ("Fecha Fin",   "e_ffin",  "fecha"),
        ]

        for i, (etiq, attr, tipo) in enumerate(campos):
            self._mk_label(self._frm, etiq).grid(
                row=i, column=0, sticky="w", padx=8, pady=4)
            if tipo == "num":
                w = crear_entry_numerico(self._frm, width=20)
                self._widgets_tema.append((w, "fondo_entrada", "texto"))
            elif tipo == "fecha":
                w = crear_campo_fecha(self._frm)
            elif tipo == "combo_estado":
                w = ttk.Combobox(self._frm, width=19, font=FUENTE_ENTRADA,
                                 values=["Activo", "En pausa", "Finalizado", "Cancelado"])
                w.set("Activo")
            else:
                w = self._mk_entry(self._frm)
            w.grid(row=i, column=1, padx=8, pady=4, sticky="w")
            setattr(self, attr, w)

        # Imagen
        self._frm_img = ttk.LabelFrame(self._frm, text="Imagen del Proyecto")
        self._frm_img.grid(row=len(campos), column=0, columnspan=2,
                           sticky="ew", padx=8, pady=6)
        self.lbl_img = tk.Label(self._frm_img, text="Sin imagen",
                                width=15, height=5, relief="groove",
                                bg=tm().color("fondo_entrada"),
                                fg=tm().color("texto_sec"))
        self.lbl_img.pack(side="left", padx=6, pady=4)
        self._widgets_tema.append((self.lbl_img, "fondo_entrada", "texto_sec"))

        frm_img_btns = tk.Frame(self._frm_img, bg=tm().color("fondo_frm"))
        frm_img_btns.pack(side="left", padx=6)
        self._widgets_tema.append((frm_img_btns, "fondo_frm", None))
        crear_boton(frm_img_btns, "Seleccionar",
                    lambda: seleccionar_imagen(self.lbl_img, self._var_img),
                    "primario", 10, "📁").pack(pady=3, fill="x")
        crear_boton(frm_img_btns, "Quitar",
                    self._quitar_imagen, "neutro", 10, "🗑").pack(pady=3, fill="x")
        nota = tk.Label(frm_img_btns, text="JPG · PNG · GIF  (máx 5 MB)",
                        fg=tm().color("texto_sec"), font=("Segoe UI", 8),
                        bg=tm().color("fondo_frm"))
        nota.pack()
        self._widgets_tema.append((nota, "fondo_frm", "texto_sec"))

        frm_btns = tk.Frame(self._frm, bg=tm().color("fondo_frm"))
        frm_btns.grid(row=len(campos) + 1, column=0, columnspan=2, pady=10)
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
            f.pack(pady=3)
            self._widgets_tema.append((f, "fondo_frm", None))
            for txt, cmd, col in fila_data:
                crear_boton(f, txt, cmd, col, 10).pack(side="left", padx=4)

        f3 = tk.Frame(parent, bg=tm().color("fondo_frm"))
        f3.pack(pady=3)
        self._widgets_tema.append((f3, "fondo_frm", None))
        crear_boton(f3, "📊 Exportar Excel",
                    self._exportar_excel, "excel", 10).pack(side="left", padx=4)
        crear_boton(f3, "📄 Exportar PDF",
                    self._exportar_pdf,   "pdf",   10).pack(side="left", padx=4)

    def _construir_filtros(self, parent):
        self._frm_f = tk.Frame(parent, bg=tm().color("fondo"))
        self._frm_f.pack(fill="x", pady=(0, 6))
        self._widgets_tema.append((self._frm_f, "fondo", None))

        lbl_b = tk.Label(self._frm_f, text="🔍 Buscar:", font=FUENTE_LABEL,
                         bg=tm().color("fondo"), fg=tm().color("texto"))
        lbl_b.pack(side="left", padx=6)
        self._widgets_tema.append((lbl_b, "fondo", "texto"))

        self.e_buscar = tk.Entry(self._frm_f, width=20, font=FUENTE_ENTRADA,
                                 bg=tm().color("fondo_entrada"),
                                 fg=tm().color("texto"),
                                 insertbackground=tm().color("texto"),
                                 relief="flat")
        self.e_buscar.pack(side="left", padx=4)
        self._widgets_tema.append((self.e_buscar, "fondo_entrada", "texto"))
        self.e_buscar.bind("<Return>", lambda e: self.buscar())

        lbl_e = tk.Label(self._frm_f, text="Estado:", font=FUENTE_LABEL,
                         bg=tm().color("fondo"), fg=tm().color("texto"))
        lbl_e.pack(side="left", padx=6)
        self._widgets_tema.append((lbl_e, "fondo", "texto"))

        self.cb_filtro = ttk.Combobox(self._frm_f, width=12, font=FUENTE_ENTRADA,
                                      values=["", "Activo", "En pausa",
                                              "Finalizado", "Cancelado"])
        self.cb_filtro.pack(side="left", padx=4)

        crear_boton(self._frm_f, "Filtrar",
                    self.filtrar,   "primario",    10, "🔍").pack(side="left", padx=4)
        crear_boton(self._frm_f, "Ver todos",
                    self.ver_todos, "primario_lt", 10, "📋").pack(side="left", padx=4)

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

    def _leer_campos(self):
        def gv(w):
            if isinstance(w, ttk.Combobox): return w.get()
            try: return w.get_date().strftime("%Y-%m-%d") if CALENDAR_OK else w.get()
            except AttributeError: return w.get()
        return dict(
            codigo=self.e_cod.get().strip(), nombre=self.e_nom.get().strip(),
            direccion=self.e_dir.get().strip(), tipo=self.e_tipo.get().strip(),
            estado=gv(self.e_est), gerente=self.e_ger.get().strip(),
            area=self.e_area.get().strip(), pisos=self.e_pisos.get().strip(),
            pre=self.e_pre.get().strip(), f_ini=gv(self.e_fini), f_fin=gv(self.e_ffin),
        )

    def _validar(self, d):
        if es_vacio(d["codigo"]):
            self.advertencia("El Código es obligatorio."); return False
        if es_vacio(d["nombre"]) or len(d["nombre"]) < 3:
            self.advertencia("El Nombre debe tener al menos 3 caracteres."); return False
        if d["area"]  and not es_numero(d["area"]):
            self.advertencia("El Área debe ser un número."); return False
        if d["pisos"] and not es_entero(d["pisos"]):
            self.advertencia("Los Pisos deben ser entero."); return False
        if d["pre"]   and not es_numero(d["pre"]):
            self.advertencia("El Presupuesto debe ser número."); return False
        return True

    def registrar(self):
        d = self._leer_campos()
        if not self._validar(d): return
        if ProyectoController.existe(d["codigo"]):
            self.error(f"Ya existe un proyecto con código '{d['codigo']}'."); return
        p = Proyecto(
            codigo=d["codigo"], nombre=d["nombre"], direccion=d["direccion"],
            tipo_construccion=d["tipo"], estado=d["estado"],
            gerente_proyecto=d["gerente"],
            area_total=float(d["area"])    if d["area"]  else None,
            cantidad_pisos=int(d["pisos"]) if d["pisos"] else None,
            presupuesto=float(d["pre"])    if d["pre"]   else None,
            fecha_inicio=d["f_ini"], fecha_fin=d["f_fin"]
        )
        if self._var_img.get():
            p.imagen = guardar_imagen(self._var_img.get(), f"proyecto_{d['codigo']}")
        ProyectoController.registrar(p)
        self.info("Proyecto registrado correctamente.")
        self.limpiar(); self.ver_todos()

    def actualizar(self):
        if self._id_seleccionado is None:
            self.advertencia("Selecciona un proyecto en la tabla primero."); return
        d = self._leer_campos()
        if not self._validar(d): return
        if not self.confirmar(f"¿Actualizar el proyecto '{d['nombre']}'?"): return
        p = Proyecto(
            codigo=d["codigo"], nombre=d["nombre"], direccion=d["direccion"],
            tipo_construccion=d["tipo"], estado=d["estado"],
            gerente_proyecto=d["gerente"],
            area_total=float(d["area"])    if d["area"]  else None,
            cantidad_pisos=int(d["pisos"]) if d["pisos"] else None,
            presupuesto=float(d["pre"])    if d["pre"]   else None,
            fecha_inicio=d["f_ini"], fecha_fin=d["f_fin"],
            id_proyecto=self._id_seleccionado
        )
        if self._var_img.get():
            p.imagen = guardar_imagen(self._var_img.get(), f"proyecto_{d['codigo']}")
        ProyectoController.actualizar(p)
        self.info("Proyecto actualizado.")
        self.limpiar(); self.ver_todos()

    def eliminar(self):
        sel = self.tv.selection()
        if not sel:
            self.advertencia("Selecciona un proyecto de la tabla."); return
        vals = self.tv.item(sel[0])["values"]
        if not self.confirmar(
                f"¿Eliminar el proyecto '{vals[2]}'?\nEsta acción no se puede deshacer."):
            return
        ProyectoController.eliminar(int(vals[0]))
        self.info("Proyecto eliminado.")
        self.limpiar(); self.ver_todos()

    def limpiar(self):
        for attr in ["e_cod", "e_nom", "e_dir", "e_tipo", "e_ger",
                     "e_area", "e_pisos", "e_pre"]:
            w = getattr(self, attr)
            if isinstance(w, tk.Entry): w.delete(0, "end")
        if isinstance(self.e_est, ttk.Combobox): self.e_est.set("Activo")
        self._quitar_imagen(); self._id_seleccionado = None

    def _quitar_imagen(self):
        self._var_img.set("")
        self.lbl_img.config(image="", text="Sin imagen")

    def ver_todos(self):
        filas = ProyectoController.listar()
        self.poblar_tabla(self.tv, [r[:12] for r in filas])
        self.tv.bind("<<TreeviewSelect>>", self._on_seleccion)

    def filtrar(self):
        filas = ProyectoController.listar(filtro_estado=self.cb_filtro.get())
        self.poblar_tabla(self.tv, [r[:12] for r in filas])

    def buscar(self):
        t = self.e_buscar.get().strip()
        if not t: self.ver_todos(); return
        self.poblar_tabla(self.tv, ProyectoController.buscar(t))

    def _on_seleccion(self, event=None):
        sel = self.tv.selection()
        if not sel: return
        vals = self.tv.item(sel[0])["values"]
        self._id_seleccionado = int(vals[0])
        for widget, valor in [
            (self.e_cod,  vals[1]), (self.e_nom,  vals[2]),
            (self.e_dir,  vals[3]), (self.e_tipo, vals[4]),
            (self.e_ger,  vals[9]),
        ]:
            widget.delete(0, "end")
            widget.insert(0, str(valor) if valor else "")
        for widget, valor in [
            (self.e_area, vals[5]), (self.e_pisos, vals[6]), (self.e_pre, vals[8])]:
            widget.delete(0, "end")
            if valor and str(valor) not in ("None", ""):
                widget.insert(0, str(valor))
        if isinstance(self.e_est, ttk.Combobox):
            self.e_est.set(vals[7] if vals[7] else "Activo")

    def _exportar_excel(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos para exportar."); return
        exportar_excel("Proyectos", list(COLS), filas,
                       f"Estado: {self.cb_filtro.get() or 'Todos'}")

    def _exportar_pdf(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos para exportar."); return
        exportar_pdf("Proyectos", list(COLS), filas,
                     f"Estado: {self.cb_filtro.get() or 'Todos'}")