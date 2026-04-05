import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
"""
views/vista_base.py
═══════════════════════════════════════════════════════════════════
Clase base para todas las vistas — Patrón MVC
  · Integra ThemeManager para temas reactivos
  · Centraliza: favicon, widgets comunes, helpers de UI
═══════════════════════════════════════════════════════════════════
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys, os

from utils.utilidades import bloquear_no_numericos
from utils.temas import ThemeManager, tm

try:
    from tkcalendar import DateEntry
    CALENDAR_OK = True
except ImportError:
    CALENDAR_OK = False

FUENTE_TITULO  = ("Segoe UI", 13, "bold")
FUENTE_LABEL   = ("Segoe UI", 9)
FUENTE_ENTRADA = ("Segoe UI", 9)
FUENTE_BTN     = ("Segoe UI", 9, "bold")


class _ColorProxy:
    """Permite usar COLOR['clave'] y devuelve el color del tema activo."""
    def __getitem__(self, clave):
        return tm().color(clave)
    def get(self, clave, default=""):
        try:
            return tm().color(clave)
        except Exception:
            return default

COLOR = _ColorProxy()


def aplicar_estilo_ttk(root: tk.Tk):
    tm().inicializar(root)


def crear_boton(parent, texto: str, comando, color: str = "primario",
                ancho: int = 14, icono: str = "") -> tk.Button:
    label = f"{icono}  {texto}" if icono else texto
    return tk.Button(
        parent, text=label, command=comando,
        bg=tm().color(color),
        fg=tm().color("texto_inv"),
        activebackground=tm().color("primario_lt"),
        activeforeground=tm().color("texto_inv"),
        font=FUENTE_BTN, width=ancho,
        relief="flat", cursor="hand2", bd=0, padx=6, pady=4
    )


def crear_campo_fecha(parent, **kwargs) -> tk.Widget:
    if CALENDAR_OK:
        return DateEntry(
            parent, width=19,
            background=tm().color("primario"),
            foreground=tm().color("texto_inv"),
            borderwidth=2, date_pattern="yyyy-mm-dd",
            font=FUENTE_ENTRADA, **kwargs
        )
    e = tk.Entry(parent, width=22, font=FUENTE_ENTRADA,
                 bg=tm().color("fondo_entrada"), fg=tm().color("texto"),
                 insertbackground=tm().color("texto"), relief="flat")
    e.insert(0, "YYYY-MM-DD")
    return e


def crear_entry_numerico(parent, width: int = 22) -> tk.Entry:
    e = tk.Entry(parent, width=width, font=FUENTE_ENTRADA,
                 bg=tm().color("fondo_entrada"), fg=tm().color("texto"),
                 insertbackground=tm().color("texto"), relief="flat")
    e.bind("<KeyPress>", bloquear_no_numericos)
    return e


class VistaBase:
    """Clase base con herramientas comunes para todas las vistas."""

    def _registrar_en_tema(self):
        if hasattr(self, "_refrescar_tema"):
            tm().registrar_observer(self._refrescar_tema)

    # ── Widgets con tema ──────────────────────────────────────────

    def _frame_con_tema(self, parent, tipo="frm") -> tk.Frame:
        clave = "fondo_frm" if tipo == "frm" else "fondo"
        return tk.Frame(parent, bg=tm().color(clave))

    def _label_con_tema(self, parent, texto="", fuente=None,
                        color_texto="texto", color_fondo="fondo_frm", **kwargs):
        return tk.Label(parent, text=texto, font=fuente or FUENTE_LABEL,
                        bg=tm().color(color_fondo), fg=tm().color(color_texto), **kwargs)

    def _entry_con_tema(self, parent, width=22) -> tk.Entry:
        return tk.Entry(parent, width=width, font=FUENTE_ENTRADA,
                        bg=tm().color("fondo_entrada"), fg=tm().color("texto"),
                        insertbackground=tm().color("texto"),
                        highlightbackground=tm().color("borde"),
                        highlightcolor=tm().color("primario"),
                        highlightthickness=1, relief="flat")

    # ── Tabla ────────────────────────────────────────────────────

    def construir_tabla(self, parent, columnas: list, alturas: int = 16) -> ttk.Treeview:
        frame = tk.Frame(parent, bg=tm().color("fondo"))
        frame.pack(fill="both", expand=True, padx=6, pady=4)

        tv = ttk.Treeview(frame, columns=columnas, show="headings", height=alturas)
        for col in columnas:
            tv.heading(col, text=col, anchor="center")
            tv.column(col, width=100, anchor="center", minwidth=60)

        sb_v = ttk.Scrollbar(frame, orient="vertical",   command=tv.yview)
        sb_h = ttk.Scrollbar(frame, orient="horizontal", command=tv.xview)
        tv.configure(yscrollcommand=sb_v.set, xscrollcommand=sb_h.set)
        sb_v.pack(side="right",  fill="y")
        sb_h.pack(side="bottom", fill="x")
        tv.pack(fill="both", expand=True)
        self._actualizar_tags_tabla(tv)
        return tv

    def _actualizar_tags_tabla(self, tv: ttk.Treeview):
        tv.tag_configure("par",   background=tm().color("fila_par"),
                         foreground=tm().color("texto"))
        tv.tag_configure("impar", background=tm().color("fila_impar"),
                         foreground=tm().color("texto"))

    def poblar_tabla(self, tv: ttk.Treeview, filas: list):
        for item in tv.get_children():
            tv.delete(item)
        self._actualizar_tags_tabla(tv)
        for idx, fila in enumerate(filas):
            tag = "par" if idx % 2 == 0 else "impar"
            tv.insert("", "end", values=fila, tags=(tag,))

    # ── Diálogos ─────────────────────────────────────────────────

    @staticmethod
    def confirmar(mensaje: str) -> bool:
        return messagebox.askyesno("⚠ Confirmar operación", mensaje)

    @staticmethod
    def info(mensaje: str):
        messagebox.showinfo("✅ Información", mensaje)

    @staticmethod
    def error(mensaje: str):
        messagebox.showerror("❌ Error", mensaje)

    @staticmethod
    def advertencia(mensaje: str):
        messagebox.showwarning("⚠ Atención", mensaje)

    # ── Refresco recursivo ────────────────────────────────────────

    def _refrescar_frame(self, widget, clave_fondo="fondo_frm"):
        cls = widget.winfo_class()
        try:
            if cls == "Frame":
                widget.configure(bg=tm().color(clave_fondo))
            elif cls == "Label":
                widget.configure(bg=tm().color(clave_fondo), fg=tm().color("texto"))
            elif cls == "Entry":
                widget.configure(
                    bg=tm().color("fondo_entrada"), fg=tm().color("texto"),
                    insertbackground=tm().color("texto"),
                    highlightbackground=tm().color("borde"),
                    highlightcolor=tm().color("primario"),
                )
        except Exception:
            pass
        for hijo in widget.winfo_children():
            if hijo.winfo_class() in ("TLabelframe", "TNotebook"):
                continue
            self._refrescar_frame(hijo, clave_fondo)
