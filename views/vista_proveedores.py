import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
"""
views/vista_proveedores.py — con soporte de temas reactivos
"""
import tkinter as tk
from tkinter import ttk

from views.vista_base import (VistaBase, FUENTE_LABEL, FUENTE_ENTRADA,
                               crear_boton)
from utils.temas import tm
from controllers.controladores import ProveedorController
from models.modelos import Proveedor
from utils.utilidades import (es_vacio, exportar_excel, exportar_pdf)

COLS = ("ID", "Nombre", "Teléfono", "Dirección", "Email", "Contacto", "Categoría")


class VistaProveedores(VistaBase):

    def __init__(self, notebook: ttk.Notebook):
        self.tab = tk.Frame(notebook, bg=tm().color("fondo"))
        notebook.add(self.tab, text="  🏭 Proveedores  ")
        self._id_seleccionado = None
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
        self._frm = ttk.LabelFrame(parent, text="Datos del Proveedor")
        self._frm.pack(fill="both", expand=True, padx=4, pady=4)

        campos = [
            ("Nombre *",   "e_nombre",   "text"),
            ("Teléfono",   "e_telefono", "text"),
            ("Dirección",  "e_dir",      "text"),
            ("Email",      "e_email",    "text"),
            ("Contacto",   "e_contacto", "text"),
            ("Categoría",  "e_cat",      "combo_cat"),
        ]

        for i, (etiq, attr, tipo) in enumerate(campos):
            self._mk_label(self._frm, etiq).grid(
                row=i, column=0, sticky="w", padx=6, pady=2)
            if tipo == "combo_cat":
                w = ttk.Combobox(self._frm, width=19, font=FUENTE_ENTRADA,
                                 values=["Acero", "Cementos", "Madera",
                                         "Eléctrico", "Pintura", "Agregados",
                                         "Mampostería", "Herramientas", "Otro"])
                w.set("")
            else:
                w = self._mk_entry(self._frm)
            w.grid(row=i, column=1, padx=6, pady=2, sticky="w")
            setattr(self, attr, w)

        # Botones CRUD
        frm_btns = tk.Frame(self._frm, bg=tm().color("fondo_frm"))
        frm_btns.grid(row=len(campos), column=0, columnspan=2, pady=8)
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

        lbl_c = tk.Label(self._frm_f, text="Categoría:", font=FUENTE_LABEL,
                         bg=tm().color("fondo"), fg=tm().color("texto"))
        lbl_c.pack(side="left", padx=4)
        self._widgets_tema.append((lbl_c, "fondo", "texto"))

        self.cb_filtro = ttk.Combobox(self._frm_f, width=12, font=FUENTE_ENTRADA,
                                      values=["", "Acero", "Cementos", "Madera",
                                              "Eléctrico", "Pintura", "Agregados",
                                              "Mampostería", "Herramientas", "Otro"])
        self.cb_filtro.pack(side="left", padx=4)

        crear_boton(self._frm_f, "Filtrar",
                    self.filtrar,   "primario",    8, "🔍").pack(side="left", padx=3)
        crear_boton(self._frm_f, "Ver todos",
                    self.ver_todos, "primario_lt", 8, "📋").pack(side="left", padx=3)

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
        return dict(
            nombre=self.e_nombre.get().strip(),
            telefono=self.e_telefono.get().strip(),
            direccion=self.e_dir.get().strip(),
            email=self.e_email.get().strip(),
            contacto=self.e_contacto.get().strip(),
            categoria=self.e_cat.get().strip(),
        )

    def _validar(self, d):
        if es_vacio(d["nombre"]) or len(d["nombre"]) < 3:
            self.advertencia("El Nombre debe tener al menos 3 caracteres.")
            return False
        return True

    def registrar(self):
        d = self._leer_campos()
        if not self._validar(d): return
        if ProveedorController.existe(d["nombre"], d["telefono"]):
            self.error("Ya existe un proveedor con ese nombre y teléfono."); return
        p = Proveedor(
            nombre=d["nombre"], telefono=d["telefono"],
            direccion=d["direccion"], email=d["email"],
            contacto=d["contacto"], categoria=d["categoria"]
        )
        ProveedorController.registrar(p)
        self.info("Proveedor registrado correctamente.")
        self.limpiar(); self.ver_todos()

    def actualizar(self):
        if self._id_seleccionado is None:
            self.advertencia("Selecciona un proveedor en la tabla primero."); return
        d = self._leer_campos()
        if not self._validar(d): return
        if not self.confirmar(f"¿Actualizar el proveedor '{d['nombre']}'?"): return
        p = Proveedor(
            nombre=d["nombre"], telefono=d["telefono"],
            direccion=d["direccion"], email=d["email"],
            contacto=d["contacto"], categoria=d["categoria"],
            id_proveedor=self._id_seleccionado
        )
        ProveedorController.actualizar(p)
        self.info("Proveedor actualizado.")
        self.limpiar(); self.ver_todos()

    def eliminar(self):
        sel = self.tv.selection()
        if not sel:
            self.advertencia("Selecciona un proveedor de la tabla."); return
        vals = self.tv.item(sel[0])["values"]
        if not self.confirmar(
                f"¿Eliminar '{vals[1]}'?\nEsta acción no se puede deshacer."):
            return
        ProveedorController.eliminar(int(vals[0]))
        self.info("Proveedor eliminado.")
        self.limpiar(); self.ver_todos()

    def limpiar(self):
        for attr in ["e_nombre", "e_telefono", "e_dir", "e_email", "e_contacto"]:
            w = getattr(self, attr)
            if isinstance(w, tk.Entry): w.delete(0, "end")
        self.e_cat.set("")
        self._id_seleccionado = None

    # ══════════════════════════════════════════════════════════════
    #  CONSULTAS / TABLA
    # ══════════════════════════════════════════════════════════════

    def ver_todos(self):
        filas = ProveedorController.listar()
        self.poblar_tabla(self.tv, [r[:7] for r in filas])
        self.tv.bind("<<TreeviewSelect>>", self._on_seleccion)

    def filtrar(self):
        filas = ProveedorController.listar(filtro_cat=self.cb_filtro.get())
        self.poblar_tabla(self.tv, [r[:7] for r in filas])

    def buscar(self):
        t = self.e_buscar.get().strip()
        if not t: self.ver_todos(); return
        self.poblar_tabla(self.tv, ProveedorController.buscar(t))

    def _on_seleccion(self, event=None):
        sel = self.tv.selection()
        if not sel: return
        vals = self.tv.item(sel[0])["values"]
        self._id_seleccionado = int(vals[0])
        for widget, valor in [
            (self.e_nombre,   vals[1]), (self.e_telefono, vals[2]),
            (self.e_dir,      vals[3]), (self.e_email,    vals[4]),
            (self.e_contacto, vals[5]),
        ]:
            widget.delete(0, "end")
            widget.insert(0, str(valor) if valor else "")
        self.e_cat.set(vals[6] if vals[6] else "")

    # ══════════════════════════════════════════════════════════════
    #  EXPORTACIÓN
    # ══════════════════════════════════════════════════════════════

    def _exportar_excel(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos para exportar."); return
        exportar_excel("Proveedores", list(COLS), filas,
                       f"Categoría: {self.cb_filtro.get() or 'Todas'}")

    def _exportar_pdf(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos para exportar."); return
        exportar_pdf("Proveedores", list(COLS), filas,
                     f"Categoría: {self.cb_filtro.get() or 'Todas'}")