import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
"""
views/vista_materiales.py — con soporte de temas reactivos
"""
import tkinter as tk
from tkinter import ttk

from views.vista_base import (VistaBase, FUENTE_LABEL, FUENTE_ENTRADA,
                               crear_boton, crear_entry_numerico)
from utils.temas import tm
from controllers.controladores import MaterialController, ProveedorController
from models.modelos import Material
from utils.utilidades import (es_vacio, es_numero,
                               seleccionar_imagen, guardar_imagen,
                               exportar_excel, exportar_pdf)

COLS = ("ID", "Código", "Descripción", "Categoría",
        "Unidad", "Precio Unit.", "Stock", "Proveedor")


class VistaMateriales(VistaBase):

    def __init__(self, notebook: ttk.Notebook):
        self.tab = tk.Frame(notebook, bg=tm().color("fondo"))
        notebook.add(self.tab, text="  🧱 Materiales  ")
        self._id_seleccionado = None
        self._var_img = tk.StringVar()
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
        self._frm = ttk.LabelFrame(parent, text="Datos del Material")
        self._frm.pack(fill="both", expand=True, padx=4, pady=4)

        # Combo proveedor — cargado dinámicamente
        self._proveedores = []  # [(id, nombre)]

        campos = [
            ("Código *",     "e_cod",      "text"),
            ("Descripción *","e_desc",     "text"),
            ("Categoría",    "e_cat",      "combo_cat"),
            ("Unidad",       "e_unidad",   "text"),
            ("Precio Unit.", "e_precio",   "num"),
            ("Stock",        "e_stock",    "num"),
            ("Proveedor",    "e_proveedor","combo_prov"),
        ]

        for i, (etiq, attr, tipo) in enumerate(campos):
            self._mk_label(self._frm, etiq).grid(
                row=i, column=0, sticky="w", padx=6, pady=2)
            if tipo == "num":
                w = crear_entry_numerico(self._frm, width=20)
                self._widgets_tema.append((w, "fondo_entrada", "texto"))
            elif tipo == "combo_cat":
                w = ttk.Combobox(self._frm, width=19, font=FUENTE_ENTRADA,
                                 values=["Cementos", "Acero", "Madera",
                                         "Eléctrico", "Pintura", "Agregados",
                                         "Mampostería", "Otro"])
                w.set("")
            elif tipo == "combo_prov":
                w = ttk.Combobox(self._frm, width=19, font=FUENTE_ENTRADA)
                self.cb_proveedor = w
            else:
                w = self._mk_entry(self._frm)
            w.grid(row=i, column=1, padx=6, pady=2, sticky="w")
            setattr(self, attr, w)

        self._cargar_proveedores()

        # Imagen
        self._frm_img = ttk.LabelFrame(self._frm, text="Imagen del Material")
        self._frm_img.grid(row=len(campos), column=0, columnspan=2,
                           sticky="ew", padx=6, pady=6)
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
                    "primario", 14, "📁").pack(pady=2)
        crear_boton(frm_img_btns, "Quitar",
                    self._quitar_imagen, "neutro", 14, "🗑").pack(pady=2)

        frm_btns = tk.Frame(self._frm, bg=tm().color("fondo_frm"))
        frm_btns.grid(row=len(campos) + 1, column=0, columnspan=2, pady=8)
        self._widgets_tema.append((frm_btns, "fondo_frm", None))
        self._construir_botones_crud(frm_btns)

    def _cargar_proveedores(self):
        try:
            self._proveedores = ProveedorController.lista_nombres()
            nombres = [f"{p[0]} - {p[1]}" for p in self._proveedores]
            self.cb_proveedor["values"] = nombres
        except Exception:
            pass

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
                                      values=["", "Cementos", "Acero", "Madera",
                                              "Eléctrico", "Pintura", "Agregados",
                                              "Mampostería", "Otro"])
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

    def _id_proveedor_seleccionado(self):
        val = self.cb_proveedor.get()
        if not val: return None
        try: return int(val.split(" - ")[0])
        except Exception: return None

    def _leer_campos(self):
        return dict(
            codigo=self.e_cod.get().strip(),
            descripcion=self.e_desc.get().strip(),
            categoria=self.e_cat.get().strip(),
            unidad=self.e_unidad.get().strip(),
            precio=self.e_precio.get().strip(),
            stock=self.e_stock.get().strip(),
            proveedor=self._id_proveedor_seleccionado(),
        )

    def _validar(self, d):
        if es_vacio(d["codigo"]):
            self.advertencia("El Código es obligatorio."); return False
        if es_vacio(d["descripcion"]) or len(d["descripcion"]) < 3:
            self.advertencia("La Descripción debe tener al menos 3 caracteres."); return False
        if d["precio"] and not es_numero(d["precio"]):
            self.advertencia("El Precio debe ser un número."); return False
        if d["stock"] and not es_numero(d["stock"]):
            self.advertencia("El Stock debe ser un número."); return False
        return True

    def registrar(self):
        d = self._leer_campos()
        if not self._validar(d): return
        if MaterialController.existe(d["codigo"]):
            self.error(f"Ya existe un material con código '{d['codigo']}'."); return
        m = Material(
            codigo=d["codigo"], descripcion=d["descripcion"],
            categoria=d["categoria"], unidad_medida=d["unidad"],
            precio_unitario=float(d["precio"]) if d["precio"] else 0.0,
            stock=float(d["stock"]) if d["stock"] else 0.0,
            proveedor_preferido=d["proveedor"]
        )
        if self._var_img.get():
            m.imagen = guardar_imagen(self._var_img.get(), f"material_{d['codigo']}")
        MaterialController.registrar(m)
        self.info("Material registrado correctamente.")
        self.limpiar(); self.ver_todos()

    def actualizar(self):
        if self._id_seleccionado is None:
            self.advertencia("Selecciona un material en la tabla primero."); return
        d = self._leer_campos()
        if not self._validar(d): return
        if not self.confirmar(f"¿Actualizar el material '{d['descripcion']}'?"): return
        m = Material(
            codigo=d["codigo"], descripcion=d["descripcion"],
            categoria=d["categoria"], unidad_medida=d["unidad"],
            precio_unitario=float(d["precio"]) if d["precio"] else 0.0,
            stock=float(d["stock"]) if d["stock"] else 0.0,
            proveedor_preferido=d["proveedor"],
            id_material=self._id_seleccionado
        )
        if self._var_img.get():
            m.imagen = guardar_imagen(self._var_img.get(), f"material_{d['codigo']}")
        MaterialController.actualizar(m)
        self.info("Material actualizado.")
        self.limpiar(); self.ver_todos()

    def eliminar(self):
        sel = self.tv.selection()
        if not sel:
            self.advertencia("Selecciona un material de la tabla."); return
        vals = self.tv.item(sel[0])["values"]
        if not self.confirmar(f"¿Eliminar '{vals[2]}'?\nEsta acción no se puede deshacer."):
            return
        MaterialController.eliminar(int(vals[0]))
        self.info("Material eliminado.")
        self.limpiar(); self.ver_todos()

    def limpiar(self):
        for attr in ["e_cod", "e_desc", "e_unidad", "e_precio", "e_stock"]:
            w = getattr(self, attr)
            if isinstance(w, tk.Entry): w.delete(0, "end")
        self.e_cat.set("")
        self.cb_proveedor.set("")
        self._quitar_imagen()
        self._id_seleccionado = None

    def _quitar_imagen(self):
        self._var_img.set("")
        self.lbl_img.config(image="", text="Sin imagen")

    # ══════════════════════════════════════════════════════════════
    #  CONSULTAS / TABLA
    # ══════════════════════════════════════════════════════════════

    def ver_todos(self):
        filas = MaterialController.listar()
        self.poblar_tabla(self.tv, [r[:8] for r in filas])
        self.tv.bind("<<TreeviewSelect>>", self._on_seleccion)

    def filtrar(self):
        filas = MaterialController.listar(filtro_cat=self.cb_filtro.get())
        self.poblar_tabla(self.tv, [r[:8] for r in filas])

    def buscar(self):
        t = self.e_buscar.get().strip()
        if not t: self.ver_todos(); return
        self.poblar_tabla(self.tv, MaterialController.buscar(t))

    def _on_seleccion(self, event=None):
        sel = self.tv.selection()
        if not sel: return
        vals = self.tv.item(sel[0])["values"]
        self._id_seleccionado = int(vals[0])
        for widget, valor in [
            (self.e_cod,   vals[1]),
            (self.e_desc,  vals[2]),
            (self.e_unidad,vals[4]),
        ]:
            widget.delete(0, "end")
            widget.insert(0, str(valor) if valor else "")
        for widget, valor in [(self.e_precio, vals[5]), (self.e_stock, vals[6])]:
            widget.delete(0, "end")
            if valor and str(valor) not in ("None", ""):
                widget.insert(0, str(valor))
        self.e_cat.set(vals[3] if vals[3] else "")

    # ══════════════════════════════════════════════════════════════
    #  EXPORTACIÓN
    # ══════════════════════════════════════════════════════════════

    def _exportar_excel(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos para exportar."); return
        exportar_excel("Materiales", list(COLS), filas,
                       f"Categoría: {self.cb_filtro.get() or 'Todas'}")

    def _exportar_pdf(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos para exportar."); return
        exportar_pdf("Materiales", list(COLS), filas,
                     f"Categoría: {self.cb_filtro.get() or 'Todas'}")