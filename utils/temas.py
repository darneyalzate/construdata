import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
"""
utils/temas.py
═══════════════════════════════════════════════════════════════════
ThemeManager — Motor central de temas visuales
  · Patrón Singleton + Observer
  · 3 temas: Claro · Oscuro · Alto Contraste
  · Propagación reactiva a TODOS los widgets de la app
  · Persiste la preferencia del usuario en un archivo JSON
═══════════════════════════════════════════════════════════════════
"""
import os
import json
import tkinter as tk
from tkinter import ttk
from typing import Callable, Dict, List


# ══════════════════════════════════════════════════════════════════
#  DEFINICIÓN DE PALETAS
# ══════════════════════════════════════════════════════════════════

PALETAS: Dict[str, Dict[str, str]] = {

    # ─── TEMA CLARO (por defecto) ─────────────────────────────────
    "claro": {
        # Acción
        "primario":      "#1565C0",
        "primario_lt":   "#1E88E5",
        "primario_dk":   "#0D47A1",
        "secundario":    "#2E7D32",
        "peligro":       "#C62828",
        "advertencia":   "#E65100",
        "neutro":        "#546E7A",
        "excel":         "#217346",
        "pdf":           "#B71C1C",
        # Superficies
        "fondo":         "#F5F5F5",
        "fondo_frm":     "#FFFFFF",
        "fondo_entrada": "#FFFFFF",
        "fondo_tabla":   "#FFFFFF",
        "fila_par":      "#E3F2FD",
        "fila_impar":    "#FFFFFF",
        # Texto
        "texto":         "#212121",
        "texto_sec":     "#546E7A",
        "texto_inv":     "#FFFFFF",
        # Bordes
        "borde":         "#B0BEC5",
        "borde_frm":     "#CFD8DC",
        # Barra título
        "barra_bg":      "#1565C0",
        "barra_fg":      "#FFFFFF",
        "barra_sub":     "#90CAF9",
        # Barra estado
        "estado_bg":     "#E8EAF6",
        "estado_fg":     "#37474F",
        # Etiqueta de tema
        "nombre":        "☀ Tema Claro",
    },

    # ─── TEMA OSCURO ──────────────────────────────────────────────
    "oscuro": {
        "primario":      "#1E88E5",
        "primario_lt":   "#42A5F5",
        "primario_dk":   "#1565C0",
        "secundario":    "#43A047",
        "peligro":       "#EF5350",
        "advertencia":   "#FF7043",
        "neutro":        "#78909C",
        "excel":         "#2E7D32",
        "pdf":           "#C62828",
        "fondo":         "#1E1E2E",
        "fondo_frm":     "#2A2A3E",
        "fondo_entrada": "#313145",
        "fondo_tabla":   "#252538",
        "fila_par":      "#1A3A5C",
        "fila_impar":    "#252538",
        "texto":         "#E0E0E0",
        "texto_sec":     "#90A4AE",
        "texto_inv":     "#FFFFFF",
        "borde":         "#3D3D5C",
        "borde_frm":     "#4A4A6A",
        "barra_bg":      "#12122A",
        "barra_fg":      "#E0E0FF",
        "barra_sub":     "#5C6BC0",
        "estado_bg":     "#12122A",
        "estado_fg":     "#90A4AE",
        "nombre":        "🌙 Tema Oscuro",
    },

    # ─── TEMA ALTO CONTRASTE ──────────────────────────────────────
    "alto_contraste": {
        "primario":      "#FFFF00",
        "primario_lt":   "#FFFF66",
        "primario_dk":   "#CCCC00",
        "secundario":    "#00FF00",
        "peligro":       "#FF4444",
        "advertencia":   "#FF8800",
        "neutro":        "#AAAAAA",
        "excel":         "#00CC44",
        "pdf":           "#FF2222",
        "fondo":         "#000000",
        "fondo_frm":     "#111111",
        "fondo_entrada": "#1A1A1A",
        "fondo_tabla":   "#0A0A0A",
        "fila_par":      "#002244",
        "fila_impar":    "#0A0A0A",
        "texto":         "#FFFFFF",
        "texto_sec":     "#CCCCCC",
        "texto_inv":     "#000000",
        "borde":         "#FFFF00",
        "borde_frm":     "#FFFF00",
        "barra_bg":      "#000000",
        "barra_fg":      "#FFFF00",
        "barra_sub":     "#AAAAFF",
        "estado_bg":     "#111100",
        "estado_fg":     "#FFFF00",
        "nombre":        "⚡ Alto Contraste",
    },
}


# ══════════════════════════════════════════════════════════════════
#  SINGLETON THEME MANAGER
# ══════════════════════════════════════════════════════════════════

_PREFS_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "database", "preferencias.json"
)


class ThemeManager:
    """
    Singleton que gestiona el tema activo y notifica a los
    observers (callbacks) cuando el tema cambia.

    Uso básico
    ----------
    tm = ThemeManager.get_instance()
    tm.registrar_observer(mi_funcion_de_refresco)
    color = tm.color("fondo")
    tm.cambiar_tema("oscuro")
    """

    _instance = None

    @classmethod
    def get_instance(cls) -> "ThemeManager":
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._tema_actual: str = self._cargar_preferencia()
        self._observers:   List[Callable] = []
        self._root:        tk.Tk | None   = None
        self._estilo:      ttk.Style | None = None

    # ── Propiedades públicas ──────────────────────────────────────

    @property
    def tema_actual(self) -> str:
        return self._tema_actual

    @property
    def paleta(self) -> Dict[str, str]:
        return PALETAS[self._tema_actual]

    @property
    def temas_disponibles(self) -> List[str]:
        return list(PALETAS.keys())

    def color(self, clave: str) -> str:
        """Devuelve el color de la paleta activa para la clave dada."""
        return PALETAS[self._tema_actual].get(clave, "#FF00FF")  # magenta = clave faltante

    def nombre_tema(self) -> str:
        return PALETAS[self._tema_actual]["nombre"]

    # ── Observer pattern ─────────────────────────────────────────

    def registrar_observer(self, callback: Callable):
        """Registra una función que se llama cada vez que cambia el tema."""
        if callback not in self._observers:
            self._observers.append(callback)

    def _notificar(self):
        for cb in self._observers:
            try:
                cb()
            except Exception:
                pass

    # ── Cambio de tema ───────────────────────────────────────────

    def cambiar_tema(self, nombre: str):
        """Cambia el tema activo y notifica a todos los observers."""
        if nombre not in PALETAS:
            raise ValueError(f"Tema '{nombre}' no existe. Disponibles: {self.temas_disponibles}")
        self._tema_actual = nombre
        self._guardar_preferencia(nombre)
        if self._estilo:
            self._aplicar_ttk(self._estilo)
        self._notificar()

    def siguiente_tema(self):
        """Cicla al siguiente tema disponible."""
        temas = self.temas_disponibles
        idx = temas.index(self._tema_actual)
        self.cambiar_tema(temas[(idx + 1) % len(temas)])

    # ── Integración con tkinter ───────────────────────────────────

    def inicializar(self, root: tk.Tk):
        """Debe llamarse una sola vez, desde main(), con la ventana raíz."""
        self._root = root
        self._estilo = ttk.Style(root)
        try:
            self._estilo.theme_use("clam")
        except Exception:
            pass
        self._aplicar_ttk(self._estilo)

    def _aplicar_ttk(self, s: ttk.Style):
        """Reconfigura todos los widgets ttk con la paleta activa."""
        p = self.paleta

        # Notebook
        s.configure("TNotebook",
                    background=p["fondo"],
                    tabmargins=[2, 5, 2, 0])
        s.configure("TNotebook.Tab",
                    background=p["borde"],
                    foreground=p["texto"],
                    padding=[14, 6],
                    font=("Segoe UI", 9, "bold"))
        s.map("TNotebook.Tab",
              background=[("selected", p["primario"])],
              foreground=[("selected", p["texto_inv"])])

        # Treeview
        s.configure("Treeview",
                    background=p["fondo_tabla"],
                    foreground=p["texto"],
                    rowheight=26,
                    fieldbackground=p["fondo_tabla"],
                    font=("Segoe UI", 9))
        s.configure("Treeview.Heading",
                    background=p["primario"],
                    foreground=p["texto_inv"],
                    font=("Segoe UI", 9, "bold"),
                    relief="flat")
        s.map("Treeview",
              background=[("selected", p["primario_lt"])],
              foreground=[("selected", p["texto_inv"])])

        # Scrollbar
        s.configure("TScrollbar",
                    troughcolor=p["fondo"],
                    background=p["borde"],
                    arrowcolor=p["texto"])

        # LabelFrame
        s.configure("TLabelframe",
                    background=p["fondo_frm"],
                    bordercolor=p["borde_frm"],
                    relief="groove")
        s.configure("TLabelframe.Label",
                    font=("Segoe UI", 10, "bold"),
                    foreground=p["primario"],
                    background=p["fondo_frm"])

        # Combobox
        s.configure("TCombobox",
                    fieldbackground=p["fondo_entrada"],
                    background=p["fondo_entrada"],
                    foreground=p["texto"],
                    selectbackground=p["primario"],
                    selectforeground=p["texto_inv"],
                    arrowcolor=p["primario"])
        s.map("TCombobox",
              fieldbackground=[("readonly", p["fondo_entrada"])],
              foreground=[("readonly", p["texto"])],
              selectbackground=[("readonly", p["primario"])])

        # Entry (via Option DB)
        if self._root:
            self._root.option_add("*Entry.relief",           "flat")
            self._root.option_add("*Entry.highlightThickness", "1")

    def aplicar_a_widget(self, widget):
        """
        Aplica los colores del tema activo a un widget tk genérico.
        Llama recursivamente en todos los hijos.
        """
        p = self.paleta
        cls = widget.winfo_class()

        try:
            if cls in ("Frame", "Labelframe"):
                widget.configure(bg=p["fondo_frm"])
            elif cls == "Label":
                widget.configure(bg=p["fondo_frm"], fg=p["texto"])
            elif cls == "Entry":
                widget.configure(
                    bg=p["fondo_entrada"], fg=p["texto"],
                    insertbackground=p["texto"],
                    relief="flat",
                    highlightbackground=p["borde"],
                    highlightcolor=p["primario"],
                    highlightthickness=1
                )
            elif cls == "Button":
                # Los botones de acción mantienen su color propio;
                # solo actualizamos fondo neutro si no tienen color definido
                pass
        except Exception:
            pass

        # Recursión en hijos
        for hijo in widget.winfo_children():
            self.aplicar_a_widget(hijo)

    # ── Persistencia ─────────────────────────────────────────────

    def _cargar_preferencia(self) -> str:
        try:
            with open(_PREFS_PATH, "r") as f:
                data = json.load(f)
                t = data.get("tema", "claro")
                return t if t in PALETAS else "claro"
        except Exception:
            return "claro"

    def _guardar_preferencia(self, tema: str):
        try:
            os.makedirs(os.path.dirname(_PREFS_PATH), exist_ok=True)
            with open(_PREFS_PATH, "w") as f:
                json.dump({"tema": tema}, f, indent=2)
        except Exception:
            pass


# ── Acceso global conveniente ─────────────────────────────────────
def tm() -> ThemeManager:
    """Alias corto para ThemeManager.get_instance()"""
    return ThemeManager.get_instance()
