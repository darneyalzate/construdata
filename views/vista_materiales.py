import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
"""
views/vista_materiales.py — con soporte de temas reactivos
"""
import tkinter as tk
from tkinter import ttk
import sys, os

from views.vista_base import (VistaBase, FUENTE_LABEL, FUENTE_ENTRADA,
                               crear_boton, crear_entry_numerico)
from utils.temas import tm
from controllers.controladores import MaterialController, ProveedorController
from models.modelos import Material
from utils.utilidades import (es_vacio, es_numero, validar_longitud,
                               seleccionar_imagen, guardar_imagen,
                               exportar_excel, exportar_pdf)

COLS = ("ID","Código","Descripción","Categoría","Unidad","Precio","Stock","ID Proveedor")


class VistaMateriales(VistaBase):

    def __init__(self, notebook):
        self.tab = tk.Frame(notebook, bg=tm().color("fondo"))
        notebook.add(self.tab, text="  🧱 Materiales  ")
        self._id_seleccionado = None
        self._var_img = tk.StringVar()
        self._widgets_tema = []
        self._construir_ui()
        self._registrar_en_tema()
        self.ver_todos()

    def _construir_ui(self):
        self._izq = tk.Frame(self.tab, bg=tm().color("fondo"), width=300)
        self._izq.pack(side="left", fill="y", padx=(10,4), pady=10)
        self._izq.pack_propagate(False)
        self._der = tk.Frame(self.tab, bg=tm().color("fondo"))
        self._der.pack(side="left", fill="both", expand=True, padx=(4,10), pady=10)
        self._construir_formulario(self._izq)
        self._construir_filtros(self._der)
        self.tv = self.construir_tabla(self._der, COLS, alturas=16)

    def _reg(self, widget, bg, fg=None):
        self._widgets_tema.append((widget,bg,fg)); return widget

    def _mk_label(self, parent, texto):
        return self._reg(tk.Label(parent,text=texto,font=FUENTE_LABEL,
                                  bg=tm().color("fondo_frm"),fg=tm().color("texto")),
                         "fondo_frm","texto")

    def _mk_entry(self, parent):
        e = tk.Entry(parent, width=22, font=FUENTE_ENTRADA,
                     bg=tm().color("fondo_entrada"), fg=tm().color("texto"),
                     insertbackground=tm().color("texto"),
                     highlightbackground=tm().color("borde"),
                     highlightcolor=tm().color("primario"),
                     highlightthickness=1, relief="flat")
        self._reg(e,"fondo_entrada","texto"); return e

    def _construir_formulario(self, parent):
        self._frm = ttk.LabelFrame(parent, text="Datos del Material")
        self._frm.pack(fill="both", expand=True, padx=4, pady=4)
        campos = [
            ("Código *","e_cod","text"),("Descripción *","e_des","text"),
            ("Categoría","e_cat","combo_cat"),("Unidad medida","e_uni","combo_uni"),
            ("Precio unit.","e_pre","num"),("Stock","e_sto","num"),
            ("Proveedor","e_pro","combo_pro"),
        ]
        for i,(etiq,attr,tipo) in enumerate(campos):
            self._mk_label(self._frm, etiq).grid(row=i, column=0, sticky="w", padx=6, pady=2)
            if tipo == "num":
                w = crear_entry_numerico(self._frm, width=20)
                self._reg(w,"fondo_entrada","texto")
            elif tipo == "combo_cat":
                w = ttk.Combobox(self._frm, width=19, font=FUENTE_ENTRADA,
                                 values=["Cementos","Acero","Madera","Eléctrico",
                                         "Plomería","Pintura","Herramientas","Otro"])
                w.set("")
            elif tipo == "combo_uni":
                w = ttk.Combobox(self._frm, width=19, font=FUENTE_ENTRADA,
                                 values=["m²","m³","ml","kg","ton",
                                         "unidad","bolsa","galón","litro"])
                w.set("")
            elif tipo == "combo_pro":
                w = ttk.Combobox(self._frm, width=19, font=FUENTE_ENTRADA)
                self._cb_proveedor = w
            else:
                w = self._mk_entry(self._frm)
            w.grid(row=i, column=1, padx=6, pady=2, sticky="w")
            setattr(self, attr, w)
        self._actualizar_proveedores()

        # Imagen
        self._frm_img = ttk.LabelFrame(self._frm, text="Imagen del Material")
        self._frm_img.grid(row=len(campos), column=0, columnspan=2, sticky="ew", padx=6, pady=6)
        self.lbl_img = tk.Label(self._frm_img, text="Sin imagen", width=15, height=5,
                                relief="groove", bg=tm().color("fondo_entrada"),
                                fg=tm().color("texto_sec"))
        self.lbl_img.pack(side="left", padx=6, pady=4)
        self._reg(self.lbl_img,"fondo_entrada","texto_sec")
        fb = self._reg(tk.Frame(self._frm_img, bg=tm().color("fondo_frm")),"fondo_frm")
        fb.pack(side="left",padx=6)
        crear_boton(fb,"Seleccionar",lambda: seleccionar_imagen(self.lbl_img, self._var_img),
                    "primario",14,"📁").pack(pady=2)
        crear_boton(fb,"Quitar",self._quitar_imagen,"neutro",14,"🗑").pack(pady=2)
        self._reg(tk.Label(fb,text="JPG · PNG · GIF  (máx 5 MB)",
                           fg=tm().color("texto_sec"),font=("Segoe UI",7),
                           bg=tm().color("fondo_frm")),"fondo_frm","texto_sec").pack()

        frm_btns = self._reg(tk.Frame(self._frm, bg=tm().color("fondo_frm")),"fondo_frm")
        frm_btns.grid(row=len(campos)+1, column=0, columnspan=2, pady=8)
        for fd in [
            [("💾 Registrar",self.registrar,"secundario"),("✏ Actualizar",self.actualizar,"advertencia")],
            [("🗑 Eliminar",self.eliminar,"peligro"),("🔄 Limpiar",self.limpiar,"neutro")],
        ]:
            f = self._reg(tk.Frame(frm_btns,bg=tm().color("fondo_frm")),"fondo_frm")
            f.pack(pady=2)
            for txt,cmd,col in fd:
                crear_boton(f,txt,cmd,col,12).pack(side="left",padx=3)
        f3 = self._reg(tk.Frame(frm_btns,bg=tm().color("fondo_frm")),"fondo_frm")
        f3.pack(pady=2)
        crear_boton(f3,"📊 Exportar Excel",self._exportar_excel,"excel",16).pack(side="left",padx=3)
        crear_boton(f3,"📄 Exportar PDF",  self._exportar_pdf,  "pdf",  16).pack(side="left",padx=3)

    def _construir_filtros(self, parent):
        self._frm_f = self._reg(tk.Frame(parent,bg=tm().color("fondo")),"fondo")
        self._frm_f.pack(fill="x",pady=(0,4))
        self._reg(tk.Label(self._frm_f,text="🔍 Buscar:",font=FUENTE_LABEL,
                           bg=tm().color("fondo"),fg=tm().color("texto")),"fondo","texto").pack(side="left",padx=4)
        self.e_buscar = self._reg(tk.Entry(self._frm_f, width=20, font=FUENTE_ENTRADA,
                                           bg=tm().color("fondo_entrada"),fg=tm().color("texto"),
                                           insertbackground=tm().color("texto"),relief="flat"),
                                  "fondo_entrada","texto")
        self.e_buscar.pack(side="left",padx=4)
        self.e_buscar.bind("<Return>",lambda e: self.buscar())
        self._reg(tk.Label(self._frm_f,text="Categoría:",font=FUENTE_LABEL,
                           bg=tm().color("fondo"),fg=tm().color("texto")),"fondo","texto").pack(side="left",padx=4)
        self.cb_filtro_cat = ttk.Combobox(self._frm_f, width=12, font=FUENTE_ENTRADA,
                                          values=["","Cementos","Acero","Madera","Eléctrico",
                                                  "Plomería","Pintura","Herramientas","Otro"])
        self.cb_filtro_cat.pack(side="left",padx=4)
        crear_boton(self._frm_f,"Filtrar",  self.filtrar,  "primario",   8,"🔍").pack(side="left",padx=3)
        crear_boton(self._frm_f,"Ver todos",self.ver_todos,"primario_lt", 8,"📋").pack(side="left",padx=3)

    # ── TEMA ─────────────────────────────────────────────────────

    def _refrescar_tema(self):
        self.tab.configure(bg=tm().color("fondo"))
        self._izq.configure(bg=tm().color("fondo"))
        self._der.configure(bg=tm().color("fondo"))
        for widget,bg,fg in self._widgets_tema:
            try:
                kw = {"bg": tm().color(bg)} if bg else {}
                if fg: kw["fg"] = tm().color(fg)
                if isinstance(widget, tk.Entry): kw["insertbackground"] = tm().color("texto")
                widget.configure(**kw)
            except Exception: pass
        if hasattr(self,"tv"): self._actualizar_tags_tabla(self.tv)

    # ── CRUD ─────────────────────────────────────────────────────

    def _actualizar_proveedores(self):
        provs = ProveedorController.lista_nombres()
        self._proveedores_map = {nombre: pid for pid,nombre in provs}
        self._cb_proveedor["values"] = [""] + [n for _,n in provs]
        self._cb_proveedor.set("")

    def _leer_campos(self):
        return dict(cod=self.e_cod.get().strip(), des=self.e_des.get().strip(),
                    cat=self.e_cat.get(), uni=self.e_uni.get(),
                    pre=self.e_pre.get().strip(), sto=self.e_sto.get().strip(),
                    pro=self.e_pro.get())

    def _validar(self, d):
        if es_vacio(d["cod"]): self.advertencia("El Código es obligatorio."); return False
        if not validar_longitud(d["des"],3,100):
            self.advertencia("La Descripción debe tener entre 3 y 100 caracteres."); return False
        if d["pre"] and not es_numero(d["pre"]): self.advertencia("El Precio debe ser número."); return False
        if d["sto"] and not es_numero(d["sto"]): self.advertencia("El Stock debe ser número."); return False
        return True

    def registrar(self):
        d = self._leer_campos()
        if not self._validar(d): return
        if MaterialController.existe(d["cod"]):
            self.error(f"Ya existe un material con código '{d['cod']}'."); return
        m = Material(codigo=d["cod"], descripcion=d["des"], categoria=d["cat"],
                     unidad_medida=d["uni"],
                     precio_unitario=float(d["pre"]) if d["pre"] else 0.0,
                     stock=float(d["sto"]) if d["sto"] else 0.0,
                     proveedor_preferido=self._proveedores_map.get(d["pro"]))
        if self._var_img.get():
            m.imagen = guardar_imagen(self._var_img.get(), f"material_{d['cod']}")
        MaterialController.registrar(m)
        self.info("Material registrado."); self.limpiar(); self.ver_todos()

    def actualizar(self):
        if self._id_seleccionado is None:
            self.advertencia("Selecciona un material en la tabla primero."); return
        d = self._leer_campos()
        if not self._validar(d): return
        if not self.confirmar(f"¿Actualizar el material '{d['des']}'?"): return
        m = Material(codigo=d["cod"], descripcion=d["des"], categoria=d["cat"],
                     unidad_medida=d["uni"],
                     precio_unitario=float(d["pre"]) if d["pre"] else 0.0,
                     stock=float(d["sto"]) if d["sto"] else 0.0,
                     proveedor_preferido=self._proveedores_map.get(d["pro"]),
                     id_material=self._id_seleccionado)
        if self._var_img.get():
            m.imagen = guardar_imagen(self._var_img.get(), f"material_{d['cod']}")
        MaterialController.actualizar(m)
        self.info("Material actualizado."); self.limpiar(); self.ver_todos()

    def eliminar(self):
        sel = self.tv.selection()
        if not sel: self.advertencia("Selecciona un material."); return
        vals = self.tv.item(sel[0])["values"]
        if not self.confirmar(f"¿Eliminar el material '{vals[2]}'?"): return
        MaterialController.eliminar(int(vals[0]))
        self.info("Material eliminado."); self.limpiar(); self.ver_todos()

    def limpiar(self):
        self.e_cod.delete(0,"end"); self.e_des.delete(0,"end")
        self.e_pre.delete(0,"end"); self.e_sto.delete(0,"end")
        for cb in [self.e_cat, self.e_uni, self._cb_proveedor]: cb.set("")
        self._quitar_imagen(); self._id_seleccionado = None

    def _quitar_imagen(self):
        self._var_img.set(""); self.lbl_img.config(image="", text="Sin imagen")

    def ver_todos(self):
        self._actualizar_proveedores()
        self.poblar_tabla(self.tv, MaterialController.listar())
        self.tv.bind("<<TreeviewSelect>>", self._on_seleccion)

    def filtrar(self):
        self.poblar_tabla(self.tv, MaterialController.listar(filtro_cat=self.cb_filtro_cat.get()))

    def buscar(self):
        t = self.e_buscar.get().strip()
        if not t: self.ver_todos(); return
        self.poblar_tabla(self.tv, MaterialController.buscar(t))

    def _on_seleccion(self, event=None):
        sel = self.tv.selection()
        if not sel: return
        vals = self.tv.item(sel[0])["values"]
        self._id_seleccionado = int(vals[0])
        self.e_cod.delete(0,"end"); self.e_cod.insert(0, str(vals[1]))
        self.e_des.delete(0,"end"); self.e_des.insert(0, str(vals[2]))
        self.e_cat.set(vals[3] or ""); self.e_uni.set(vals[4] or "")
        self.e_pre.delete(0,"end")
        if vals[5] and str(vals[5]) not in ("None",""): self.e_pre.insert(0, str(vals[5]))
        self.e_sto.delete(0,"end")
        if vals[6] and str(vals[6]) not in ("None",""): self.e_sto.insert(0, str(vals[6]))

    def _exportar_excel(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos."); return
        exportar_excel("Materiales", list(COLS), filas,
                       f"Categoría: {self.cb_filtro_cat.get() or 'Todas'}")

    def _exportar_pdf(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos."); return
        exportar_pdf("Materiales", list(COLS), filas,
                     f"Categoría: {self.cb_filtro_cat.get() or 'Todas'}")
