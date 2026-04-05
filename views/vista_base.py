import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
"""
views/vista_base.py
Clase base, constantes de estilo y helpers de widgets compartidos.
"""
import tkinter as tk
from tkinter import ttk, messagebox

from utils.temas import tm

# ── Fuentes ───────────────────────────────────────────────────────
FUENTE_TITULO  = ("Segoe UI", 13, "bold")
FUENTE_LABEL   = ("Segoe UI", 10)
FUENTE_ENTRADA = ("Segoe UI", 10)
FUENTE_BTN     = ("Segoe UI", 10, "bold")

# ── Colores legacy (compatibilidad) ──────────────────────────────
COLOR = {
    "primario":    "#1565C0",
    "secundario":  "#2E7D32",
    "advertencia": "#F57F17",
    "peligro":     "#C62828",
    "neutro":      "#546E7A",
    "excel":       "#1B5E20",
    "pdf":         "#B71C1C",
    "fondo":       "#F5F5F5",
    "texto":       "#212121",
}

# ── Calendar (tkcalendar opcional) ────────────────────────────────
try:
    from tkcalendar import DateEntry
    CALENDAR_OK = True
except ImportError:
    CALENDAR_OK = False


# ══════════════════════════════════════════════════════════════════
#  HELPERS DE WIDGETS
# ══════════════════════════════════════════════════════════════════

# Paleta de botones por tipo
_BTN_COLORES = {
    "primario":    ("#1565C0", "#FFFFFF"),
    "primario_lt": ("#1976D2", "#FFFFFF"),
    "secundario":  ("#2E7D32", "#FFFFFF"),
    "advertencia": ("#F57F17", "#FFFFFF"),
    "peligro":     ("#C62828", "#FFFFFF"),
    "neutro":      ("#546E7A", "#FFFFFF"),
    "excel":       ("#1B5E20", "#FFFFFF"),
    "pdf":         ("#B71C1C", "#FFFFFF"),
}

def crear_boton(parent, texto: str, comando, estilo: str = "primario",
                fuente_size: int = 9, icono: str = "") -> tk.Button:
    """Crea un botón estilizado con color según el tipo."""
    bg, fg = _BTN_COLORES.get(estilo, ("#1565C0", "#FFFFFF"))
    label = f"{icono} {texto}".strip() if icono else texto
    btn = tk.Button(
        parent, text=label, command=comando,
        bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
        font=("Segoe UI", fuente_size, "bold"),
        relief="flat", cursor="hand2", bd=0,
        padx=14, pady=6
    )
    return btn


def crear_campo_fecha(parent) -> tk.Widget:
    """Devuelve un DateEntry si tkcalendar está disponible, o un Entry simple."""
    if CALENDAR_OK:
        w = DateEntry(parent, width=18, font=FUENTE_ENTRADA,
                      date_pattern="yyyy-mm-dd",
                      background=tm().color("primario"),
                      foreground="white",
                      borderwidth=1)
    else:
        w = tk.Entry(parent, width=20, font=FUENTE_ENTRADA,
                     bg=tm().color("fondo_entrada"),
                     fg=tm().color("texto"),
                     insertbackground=tm().color("texto"),
                     relief="flat")
    return w


def crear_entry_numerico(parent, width: int = 10) -> tk.Entry:
    """Entry que solo acepta caracteres numéricos."""
    e = tk.Entry(parent, width=width, font=FUENTE_ENTRADA,
                 bg=tm().color("fondo_entrada"),
                 fg=tm().color("texto"),
                 insertbackground=tm().color("texto"),
                 highlightbackground=tm().color("borde"),
                 highlightcolor=tm().color("primario"),
                 highlightthickness=1, relief="flat")
    def _solo_numeros(evento):
        if evento.char and evento.char not in '0123456789.,\x08\x7f\t':
            return "break"
    e.bind("<KeyPress>", _solo_numeros)
    return e


# ══════════════════════════════════════════════════════════════════
#  APLICAR ESTILO TTK
# ══════════════════════════════════════════════════════════════════

def aplicar_estilo_ttk(root: tk.Tk):
    style = ttk.Style(root)
    style.theme_use("clam")
    # Notebook
    style.configure("TNotebook",
                    background=tm().color("fondo"),
                    borderwidth=0)
    style.configure("TNotebook.Tab",
                    background=tm().color("tab_bg"),
                    foreground=tm().color("tab_fg"),
                    font=("Segoe UI", 9, "bold"),
                    padding=[12, 5])
    style.map("TNotebook.Tab",
              background=[("selected", tm().color("primario"))],
              foreground=[("selected", tm().color("texto_inv"))])
    # LabelFrame
    style.configure("TLabelframe",
                    background=tm().color("fondo_frm"),
                    bordercolor=tm().color("borde"))
    style.configure("TLabelframe.Label",
                    background=tm().color("fondo_frm"),
                    foreground=tm().color("primario"),
                    font=("Segoe UI", 9, "bold"))
    # Treeview
    style.configure("Treeview",
                    background=tm().color("fondo_tabla"),
                    foreground=tm().color("texto"),
                    fieldbackground=tm().color("fondo_tabla"),
                    rowheight=22,
                    font=("Segoe UI", 9))
    style.configure("Treeview.Heading",
                    background=tm().color("primario"),
                    foreground=tm().color("texto_inv"),
                    font=("Segoe UI", 9, "bold"))
    style.map("Treeview",
              background=[("selected", tm().color("primario_lt"))],
              foreground=[("selected", tm().color("texto_inv"))])
    # Scrollbar
    style.configure("Vertical.TScrollbar",
                    background=tm().color("borde"),
                    troughcolor=tm().color("fondo"))
    # Combobox
    style.configure("TCombobox",
                    fieldbackground=tm().color("fondo_entrada"),
                    background=tm().color("fondo_entrada"),
                    foreground=tm().color("texto"))


# ══════════════════════════════════════════════════════════════════
#  CLASE BASE
# ══════════════════════════════════════════════════════════════════

class VistaBase:
    """
    Clase base para todas las vistas.
    Provee: mensajes, tabla genérica, registro en tema.
    """

    # ── Mensajes ─────────────────────────────────────────────────

    def info(self, mensaje: str):
        messagebox.showinfo("Información", mensaje)

    def advertencia(self, mensaje: str):
        messagebox.showwarning("Advertencia", mensaje)

    def error(self, mensaje: str):
        messagebox.showerror("Error", mensaje)

    def confirmar(self, mensaje: str) -> bool:
        return messagebox.askyesno("Confirmar", mensaje)

    # ── Tabla genérica ───────────────────────────────────────────

    def construir_tabla(self, parent, columnas: tuple,
                        alturas: int = 14) -> ttk.Treeview:
        """Crea un Treeview con scrollbars verticales y horizontales."""
        frm = tk.Frame(parent, bg=tm().color("fondo"))
        frm.pack(fill="both", expand=True)

        sb_v = ttk.Scrollbar(frm, orient="vertical")
        sb_h = ttk.Scrollbar(frm, orient="horizontal")

        tv = ttk.Treeview(
            frm,
            columns=columnas,
            show="headings",
            height=alturas,
            yscrollcommand=sb_v.set,
            xscrollcommand=sb_h.set,
        )

        sb_v.config(command=tv.yview)
        sb_h.config(command=tv.xview)

        for col in columnas:
            tv.heading(col, text=col)
            tv.column(col, width=110, anchor="center", minwidth=70)

        # Tags para filas alternas
        tv.tag_configure("par",   background=tm().color("fila_par"))
        tv.tag_configure("impar", background=tm().color("fila_impar"))

        tv.grid(row=0, column=0, sticky="nsew")
        sb_v.grid(row=0, column=1, sticky="ns")
        sb_h.grid(row=1, column=0, sticky="ew")

        frm.rowconfigure(0, weight=1)
        frm.columnconfigure(0, weight=1)

        return tv

    def poblar_tabla(self, tv: ttk.Treeview, filas: list):
        """Limpia y llena el Treeview con las filas dadas."""
        tv.delete(*tv.get_children())
        for i, fila in enumerate(filas):
            tag = "par" if i % 2 == 0 else "impar"
            tv.insert("", "end", values=fila, tags=(tag,))

    def _actualizar_tags_tabla(self, tv: ttk.Treeview):
        """Reaplica los colores de tema a los tags de la tabla."""
        tv.tag_configure("par",   background=tm().color("fila_par"))
        tv.tag_configure("impar", background=tm().color("fila_impar"))

    # ── Registro en ThemeManager ─────────────────────────────────

    def _registrar_en_tema(self):
        """Registra el método _refrescar_tema como observer del ThemeManager."""
        if hasattr(self, "_refrescar_tema"):
            tm().registrar_observer(self._refrescar_tema)