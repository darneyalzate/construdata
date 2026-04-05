import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
"""
views/vista_proveedores.py — con soporte de temas reactivos
"""
import tkinter as tk
from tkinter import ttk
import sys, os

from views.vista_base import (VistaBase, FUENTE_LABEL, FUENTE_ENTRADA, crear_boton)
from utils.temas import tm
from controllers.controladores import ProveedorController
from models.modelos import Proveedor
from utils.utilidades import (es_vacio, es_email_valido, validar_longitud,
                               exportar_excel, exportar_pdf)

COLS = ("ID","Nombre","Teléfono","Dirección","Email","Contacto","Categoría")


class VistaProveedores(VistaBase):

    def __init__(self, notebook):
        self.tab = tk.Frame(notebook, bg=tm().color("fondo"))
        notebook.add(self.tab, text="  🏭 Proveedores  ")
        self._id_seleccionado = None
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
        self.tv = self.construir_tabla(self._der, COLS, alturas=18)

    def _reg(self, widget, bg, fg=None):
        self._widgets_tema.append((widget,bg,fg)); return widget

    def _mk_label(self, parent, texto):
        return self._reg(tk.Label(parent, text=texto, font=FUENTE_LABEL,
                                  bg=tm().color("fondo_frm"), fg=tm().color("texto")),
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
        self._frm = ttk.LabelFrame(parent, text="Datos del Proveedor")
        self._frm.pack(fill="both", expand=True, padx=4, pady=4)

        campos = [
            ("Nombre *","e_nom","text"),("Teléfono","e_tel","text"),
            ("Dirección","e_dir","text"),("Email *","e_mail","text"),
            ("Contacto","e_con","text"),("Categoría","e_cat","combo_cat"),
        ]
        for i,(etiq,attr,tipo) in enumerate(campos):
            self._mk_label(self._frm, etiq).grid(row=i*2, column=0, sticky="w", padx=6, pady=(4,0))
            if tipo == "combo_cat":
                w = ttk.Combobox(self._frm, width=19, font=FUENTE_ENTRADA,
                                 values=["Materiales","Herramientas","Servicios",
                                         "Equipos","Transporte","Otro"])
                w.set("")
            else:
                w = self._mk_entry(self._frm)
            w.grid(row=i*2, column=1, padx=6, pady=(4,0), sticky="w")
            setattr(self, attr, w)

        nota = self._reg(tk.Label(self._frm, text="Ej: contacto@empresa.com",
                                  fg=tm().color("texto_sec"), font=("Segoe UI",7),
                                  bg=tm().color("fondo_frm")),"fondo_frm","texto_sec")
        nota.grid(row=7, column=1, sticky="w", padx=6)

        frm_btns = self._reg(tk.Frame(self._frm, bg=tm().color("fondo_frm")),"fondo_frm")
        frm_btns.grid(row=13, column=0, columnspan=2, pady=12)
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
        self.cb_filtro = ttk.Combobox(self._frm_f, width=12, font=FUENTE_ENTRADA,
                                      values=["","Materiales","Herramientas","Servicios",
                                              "Equipos","Transporte","Otro"])
        self.cb_filtro.pack(side="left",padx=4)
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

    def _leer_campos(self):
        return dict(nom=self.e_nom.get().strip(), tel=self.e_tel.get().strip(),
                    dir=self.e_dir.get().strip(), mail=self.e_mail.get().strip(),
                    con=self.e_con.get().strip(), cat=self.e_cat.get())

    def _validar(self, d):
        if not validar_longitud(d["nom"],3,100):
            self.advertencia("El Nombre debe tener entre 3 y 100 caracteres."); return False
        if es_vacio(d["mail"]): self.advertencia("El Email es obligatorio."); return False
        if not es_email_valido(d["mail"]):
            self.advertencia("Email inválido. Ej: usuario@empresa.com"); return False
        return True

    def registrar(self):
        d = self._leer_campos()
        if not self._validar(d): return
        if ProveedorController.existe(d["nom"], d["tel"]):
            self.error("Ya existe ese proveedor."); return
        p = Proveedor(nombre=d["nom"],telefono=d["tel"],direccion=d["dir"],
                      email=d["mail"],contacto=d["con"],categoria=d["cat"])
        ProveedorController.registrar(p)
        self.info("Proveedor registrado."); self.limpiar(); self.ver_todos()

    def actualizar(self):
        if self._id_seleccionado is None:
            self.advertencia("Selecciona un proveedor en la tabla primero."); return
        d = self._leer_campos()
        if not self._validar(d): return
        if not self.confirmar(f"¿Actualizar al proveedor '{d['nom']}'?"): return
        p = Proveedor(nombre=d["nom"],telefono=d["tel"],direccion=d["dir"],
                      email=d["mail"],contacto=d["con"],categoria=d["cat"],
                      id_proveedor=self._id_seleccionado)
        ProveedorController.actualizar(p)
        self.info("Proveedor actualizado."); self.limpiar(); self.ver_todos()

    def eliminar(self):
        sel = self.tv.selection()
        if not sel: self.advertencia("Selecciona un proveedor."); return
        vals = self.tv.item(sel[0])["values"]
        if not self.confirmar(f"¿Eliminar al proveedor '{vals[1]}'?"): return
        ProveedorController.eliminar(int(vals[0]))
        self.info("Proveedor eliminado."); self.limpiar(); self.ver_todos()

    def limpiar(self):
        for attr in ["e_nom","e_tel","e_dir","e_mail","e_con"]:
            getattr(self, attr).delete(0,"end")
        self.e_cat.set(""); self._id_seleccionado = None

    def ver_todos(self):
        self.poblar_tabla(self.tv, ProveedorController.listar())
        self.tv.bind("<<TreeviewSelect>>", self._on_seleccion)

    def filtrar(self):
        self.poblar_tabla(self.tv, ProveedorController.listar(filtro_cat=self.cb_filtro.get()))

    def buscar(self):
        t = self.e_buscar.get().strip()
        if not t: self.ver_todos(); return
        self.poblar_tabla(self.tv, ProveedorController.buscar(t))

    def _on_seleccion(self, event=None):
        sel = self.tv.selection()
        if not sel: return
        vals = self.tv.item(sel[0])["values"]
        self._id_seleccionado = int(vals[0])
        for attr,val in [("e_nom",vals[1]),("e_tel",vals[2]),("e_dir",vals[3]),
                          ("e_mail",vals[4]),("e_con",vals[5])]:
            w = getattr(self, attr); w.delete(0,"end"); w.insert(0, str(val) if val else "")
        self.e_cat.set(vals[6] or "")

    def _exportar_excel(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos."); return
        exportar_excel("Proveedores", list(COLS), filas,
                       f"Categoría: {self.cb_filtro.get() or 'Todas'}")

    def _exportar_pdf(self):
        filas = [self.tv.item(i)["values"] for i in self.tv.get_children()]
        if not filas: self.advertencia("No hay datos."); return
        exportar_pdf("Proveedores", list(COLS), filas,
                     f"Categoría: {self.cb_filtro.get() or 'Todas'}")
