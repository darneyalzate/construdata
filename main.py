"""
main.py — ConstruData
Punto de entrada. Configura el sys.path antes de cualquier import.
"""
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
os.chdir(BASE_DIR)

import tkinter as tk
from tkinter import ttk

from utils.temas import ThemeManager, tm, PALETAS
from views.vista_base import aplicar_estilo_ttk, FUENTE_TITULO
from views.vista_proyectos   import VistaProyectos
from views.vista_empleados   import VistaEmpleados
from views.vista_materiales  import VistaMateriales
from views.vista_proveedores import VistaProveedores


def crear_favicon(root: tk.Tk):
    try:
        from PIL import Image, ImageDraw, ImageFont, ImageTk
        size = 32
        img  = Image.new("RGBA", (size, size), (255, 255, 255, 0))
        draw = ImageDraw.Draw(img)
        draw.ellipse([0, 0, size-1, size-1], fill=tm().color("primario"))
        try:
            font = ImageFont.truetype("arial.ttf", 20)
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


class BarraTitulo:
    NOMBRES = {
        "claro":          "☀  Claro",
        "oscuro":         "🌙  Oscuro",
        "alto_contraste": "⚡  Contraste",
    }

    def __init__(self, root: tk.Tk):
        self._root  = root
        self._barra = tk.Frame(root, height=60)
        self._barra.pack(fill="x", side="top")
        self._barra.pack_propagate(False)
        self._widgets = []
        self._construir()
        tm().registrar_observer(self._refrescar)
        self._refrescar()

    def _construir(self):
        self._lbl_icono = tk.Label(self._barra, text="🏗", font=("Segoe UI", 24))
        self._lbl_icono.pack(side="left", padx=(16, 4))
        self._widgets.append(self._lbl_icono)

        self._lbl_titulo = tk.Label(
            self._barra,
            text="ConstruData  —  Sistema de Gestión de Construcción",
            font=FUENTE_TITULO)
        self._lbl_titulo.pack(side="left", padx=4)
        self._widgets.append(self._lbl_titulo)

        frm_tema = tk.Frame(self._barra)
        frm_tema.pack(side="right", padx=16, pady=10)
        self._widgets.append(frm_tema)

        lbl_t = tk.Label(frm_tema, text="🎨 Tema:", font=("Segoe UI", 9, "bold"))
        lbl_t.pack(side="left", padx=(0, 6))
        self._widgets.append(lbl_t)

        self._botones_tema = {}
        for nombre in ["claro", "oscuro", "alto_contraste"]:
            btn = tk.Button(
                frm_tema, text=self.NOMBRES[nombre],
                font=("Segoe UI", 9, "bold"),
                relief="flat", cursor="hand2", bd=0, padx=10, pady=4,
                command=lambda n=nombre: tm().cambiar_tema(n)
            )
            btn.pack(side="left", padx=3)
            self._botones_tema[nombre] = btn

        self._lbl_ver = tk.Label(self._barra, text="v2.0 | MySQL", font=("Segoe UI", 9))
        self._lbl_ver.pack(side="right", padx=(0, 10))
        self._widgets.append(self._lbl_ver)

    def _refrescar(self):
        bg  = tm().color("barra_bg")
        fg  = tm().color("barra_fg")
        sub = tm().color("barra_sub")
        self._barra.configure(bg=bg)
        for w in self._widgets:
            try: w.configure(bg=bg, fg=fg)
            except Exception: pass
        self._lbl_ver.configure(fg=sub)
        self._root.configure(bg=tm().color("fondo"))
        activo = tm().tema_actual
        for nombre, btn in self._botones_tema.items():
            if nombre == activo:
                btn.configure(bg=tm().color("primario_lt"),
                              fg=tm().color("texto_inv"), relief="solid")
            else:
                btn.configure(bg=tm().color("primario_dk"), fg=sub, relief="flat")


class BarraEstado:
    def __init__(self, root: tk.Tk):
        self._barra = tk.Frame(root, height=28)
        self._barra.pack(fill="x", side="bottom")
        self._barra.pack_propagate(False)
        self._lbl = tk.Label(
            self._barra,
            text="ConstruData  |  Base de datos: MySQL  |  "
                 "Módulos: 🏗 Proyectos · 👷 Empleados · 🧱 Materiales · 🏭 Proveedores",
            font=("Segoe UI", 9))
        self._lbl.pack(side="left", padx=12)
        self._lbl_tema = tk.Label(self._barra, font=("Segoe UI", 9, "bold"))
        self._lbl_tema.pack(side="right", padx=12)
        tm().registrar_observer(self._refrescar)
        self._refrescar()

    def _refrescar(self):
        bg = tm().color("estado_bg")
        fg = tm().color("estado_fg")
        self._barra.configure(bg=bg)
        self._lbl.configure(bg=bg, fg=fg)
        self._lbl_tema.configure(bg=bg, fg=tm().color("primario"),
                                 text=f"Tema activo: {tm().nombre_tema()}")


def main():
    root = tk.Tk()
    root.title("ConstruData — Sistema de Gestión de Construcción")
    root.geometry("1280x780")       # ← ventana más grande
    root.minsize(1100, 680)         # ← mínimo más generoso

    aplicar_estilo_ttk(root)
    crear_favicon(root)
    BarraTitulo(root)

    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True, padx=10, pady=(8, 0))

    VistaProyectos(notebook)
    VistaEmpleados(notebook)
    VistaMateriales(notebook)
    VistaProveedores(notebook)

    BarraEstado(root)

    root.update_idletasks()
    w, h = root.winfo_width(), root.winfo_height()
    x = (root.winfo_screenwidth()  - w) // 2
    y = (root.winfo_screenheight() - h) // 2
    root.geometry(f"{w}x{h}+{x}+{y}")

    root.mainloop()


if __name__ == "__main__":
    main()