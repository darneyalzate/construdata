"""
main.py
═══════════════════════════════════════════════════════════════════
ConstruData — Sistema de Gestión de Construcción
Arquitectura MVC + POO | Python 3 + Tkinter + SQLite
  · 3 temas intercambiables: Claro · Oscuro · Alto Contraste
  · ThemeManager con patrón Observer (propagación reactiva)
  · Persistencia de preferencia de tema en JSON
═══════════════════════════════════════════════════════════════════
"""
import os
import sys
import tkinter as tk
from tkinter import ttk

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from utils.temas import tm, PALETAS
from views.vista_base import aplicar_estilo_ttk, FUENTE_TITULO
from views.vista_proyectos   import VistaProyectos
from views.vista_empleados   import VistaEmpleados
from views.vista_materiales  import VistaMateriales
from views.vista_proveedores import VistaProveedores


# ══════════════════════════════════════════════════════════════════
#  FAVICON  (generado con Pillow)
# ══════════════════════════════════════════════════════════════════

def crear_favicon(root: tk.Tk):
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageTk
        size = 32
        img = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([0, 0, size-1, size-1], fill=tm().color("primario"))
        try:
            font = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except Exception:
            font = ImageFont.load_default()
        draw.text((7, 5), "C", fill="white", font=font)
        ico_path = os.path.join(BASE_DIR, "assets", "favicon.png")
        os.makedirs(os.path.dirname(ico_path), exist_ok=True)
        img.save(ico_path)
        foto = ImageTk.PhotoImage(img)
        root.iconphoto(True, foto)
        root._favicon = foto
    except Exception:
        pass


# ══════════════════════════════════════════════════════════════════
#  BARRA DE TÍTULO  con selector de temas
# ══════════════════════════════════════════════════════════════════

class BarraTitulo:
    """
    Barra superior con logo, título, selector de tema y botón ciclar.
    Se auto-actualiza al cambiar el tema.
    """
    NOMBRES_TEMA = {
        "claro":         "☀  Claro",
        "oscuro":        "🌙  Oscuro",
        "alto_contraste":"⚡  Contraste",
    }

    def __init__(self, root: tk.Tk):
        self._root = root
        self._barra = tk.Frame(root, height=56)
        self._barra.pack(fill="x", side="top")
        self._barra.pack_propagate(False)
        self._widgets = []
        self._construir()
        tm().registrar_observer(self._refrescar)
        self._refrescar()

    def _construir(self):
        # Ícono
        self._lbl_icono = tk.Label(self._barra, text="🏗",
                                   font=("Segoe UI", 22))
        self._lbl_icono.pack(side="left", padx=(14, 4))
        self._widgets.append(self._lbl_icono)

        # Título
        self._lbl_titulo = tk.Label(
            self._barra,
            text="ConstruData  —  Sistema de Gestión de Construcción",
            font=FUENTE_TITULO)
        self._lbl_titulo.pack(side="left", padx=4)
        self._widgets.append(self._lbl_titulo)

        # ── Selector de tema (lado derecho) ──────────────────────
        frm_tema = tk.Frame(self._barra)
        frm_tema.pack(side="right", padx=14, pady=8)
        self._widgets.append(frm_tema)

        lbl_t = tk.Label(frm_tema, text="🎨 Tema:", font=("Segoe UI", 8, "bold"))
        lbl_t.pack(side="left", padx=(0, 4))
        self._widgets.append(lbl_t)

        # Botón por cada tema disponible
        self._botones_tema = {}
        for nombre in ["claro", "oscuro", "alto_contraste"]:
            btn = tk.Button(
                frm_tema,
                text=self.NOMBRES_TEMA[nombre],
                font=("Segoe UI", 8, "bold"),
                relief="flat", cursor="hand2", bd=0,
                padx=8, pady=3,
                command=lambda n=nombre: tm().cambiar_tema(n)
            )
            btn.pack(side="left", padx=2)
            self._botones_tema[nombre] = btn

        # Versión
        self._lbl_ver = tk.Label(self._barra, text="v2.0 | SQLite",
                                 font=("Segoe UI", 8))
        self._lbl_ver.pack(side="right", padx=(0, 8))
        self._widgets.append(self._lbl_ver)

    def _refrescar(self):
        """Actualiza colores de la barra según el tema activo."""
        bg  = tm().color("barra_bg")
        fg  = tm().color("barra_fg")
        sub = tm().color("barra_sub")

        self._barra.configure(bg=bg)
        for w in self._widgets:
            try:
                w.configure(bg=bg, fg=fg)
            except Exception:
                pass

        self._lbl_ver.configure(fg=sub)
        self._root.configure(bg=tm().color("fondo"))

        # Resaltar botón del tema activo
        activo = tm().tema_actual
        for nombre, btn in self._botones_tema.items():
            if nombre == activo:
                btn.configure(
                    bg=tm().color("primario_lt"),
                    fg=tm().color("texto_inv"),
                    relief="solid"
                )
            else:
                btn.configure(
                    bg=tm().color("primario_dk"),
                    fg=sub,
                    relief="flat"
                )


# ══════════════════════════════════════════════════════════════════
#  BARRA DE ESTADO
# ══════════════════════════════════════════════════════════════════

class BarraEstado:
    """Barra inferior con info del sistema. Se actualiza con el tema."""

    def __init__(self, root: tk.Tk):
        self._barra = tk.Frame(root, height=24)
        self._barra.pack(fill="x", side="bottom")
        self._barra.pack_propagate(False)
        self._lbl = tk.Label(
            self._barra,
            text="ConstruData  |  Base de datos: SQLite  |  "
                 "Módulos: 🏗 Proyectos · 👷 Empleados · 🧱 Materiales · 🏭 Proveedores",
            font=("Segoe UI", 8)
        )
        self._lbl.pack(side="left", padx=10)
        self._lbl_tema = tk.Label(self._barra, font=("Segoe UI", 8, "bold"))
        self._lbl_tema.pack(side="right", padx=10)
        tm().registrar_observer(self._refrescar)
        self._refrescar()

    def _refrescar(self):
        bg = tm().color("estado_bg")
        fg = tm().color("estado_fg")
        self._barra.configure(bg=bg)
        self._lbl.configure(bg=bg, fg=fg)
        self._lbl_tema.configure(
            bg=bg,
            fg=tm().color("primario"),
            text=f"Tema activo: {tm().nombre_tema()}"
        )


# ══════════════════════════════════════════════════════════════════
#  APLICACIÓN PRINCIPAL
# ══════════════════════════════════════════════════════════════════

def main():
    root = tk.Tk()
    root.title("ConstruData — Sistema de Gestión de Construcción")
    root.geometry("1150x720")
    root.minsize(950, 620)

    # 1. Inicializar ThemeManager (PRIMERO, antes de cualquier widget)
    aplicar_estilo_ttk(root)

    # 2. Favicon
    crear_favicon(root)

    # 3. Barra de título con selector de temas
    BarraTitulo(root)

    # 4. Notebook principal
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=8, pady=(6, 0))

    # 5. Las cuatro vistas — cada una se registra como observer del tema
    VistaProyectos(notebook)
    VistaEmpleados(notebook)
    VistaMateriales(notebook)
    VistaProveedores(notebook)

    # 6. Barra de estado
    BarraEstado(root)

    # 7. Centrar ventana
    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth()  - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()
