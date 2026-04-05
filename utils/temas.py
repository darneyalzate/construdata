import json
import os

CONFIG_FILE = "tema_config.json"

PALETAS = {
    "claro": {
        # Estructura general
        "fondo":          "#F5F5F5",
        "fondo_frm":      "#FFFFFF",
        "fondo_entrada":  "#FFFFFF",
        "fondo_tabla":    "#FFFFFF",
        "borde":          "#BBDEFB",
        # Texto
        "texto":          "#212121",
        "texto_sec":      "#757575",
        "texto_inv":      "#FFFFFF",
        # Barra de título
        "barra_bg":       "#1565C0",
        "barra_fg":       "#FFFFFF",
        "barra_sub":      "#90CAF9",
        # Barra de estado
        "estado_bg":      "#E3F2FD",
        "estado_fg":      "#1565C0",
        # Colores primarios
        "primario":       "#1565C0",
        "primario_lt":    "#1976D2",
        "primario_dk":    "#0D47A1",
        # Tabs
        "tab_bg":         "#E3F2FD",
        "tab_fg":         "#1565C0",
        # Filas de tabla alternas
        "fila_par":       "#E3F2FD",
        "fila_impar":     "#FFFFFF",
    },
    "oscuro": {
        # Estructura general
        "fondo":          "#1E1E1E",
        "fondo_frm":      "#2B2B2B",
        "fondo_entrada":  "#3C3F41",
        "fondo_tabla":    "#2B2B2B",
        "borde":          "#555555",
        # Texto
        "texto":          "#E0E0E0",
        "texto_sec":      "#AAAAAA",
        "texto_inv":      "#FFFFFF",
        # Barra de título
        "barra_bg":       "#1F1F1F",
        "barra_fg":       "#FFFFFF",
        "barra_sub":      "#BBBBBB",
        # Barra de estado
        "estado_bg":      "#1F1F1F",
        "estado_fg":      "#FFFFFF",
        # Colores primarios
        "primario":       "#4CAF50",
        "primario_lt":    "#81C784",
        "primario_dk":    "#1B5E20",
        # Tabs
        "tab_bg":         "#2B2B2B",
        "tab_fg":         "#BBBBBB",
        # Filas de tabla alternas
        "fila_par":       "#2B3B2B",
        "fila_impar":     "#2B2B2B",
    },
    "alto_contraste": {
        # Estructura general
        "fondo":          "#000000",
        "fondo_frm":      "#000000",
        "fondo_entrada":  "#1A1A1A",
        "fondo_tabla":    "#000000",
        "borde":          "#FFFF00",
        # Texto
        "texto":          "#FFFFFF",
        "texto_sec":      "#FFFF00",
        "texto_inv":      "#000000",
        # Barra de título
        "barra_bg":       "#000000",
        "barra_fg":       "#FFFFFF",
        "barra_sub":      "#FFFF00",
        # Barra de estado
        "estado_bg":      "#000000",
        "estado_fg":      "#FFFFFF",
        # Colores primarios
        "primario":       "#FFFF00",
        "primario_lt":    "#FFFF99",
        "primario_dk":    "#CCCC00",
        # Tabs
        "tab_bg":         "#1A1A1A",
        "tab_fg":         "#FFFF00",
        # Filas de tabla alternas
        "fila_par":       "#1A1A00",
        "fila_impar":     "#000000",
    },
}


class ThemeManager:
    def __init__(self):
        self.tema_actual = "claro"
        self.observers = []
        self.cargar()

    def color(self, clave: str) -> str:
        return PALETAS[self.tema_actual].get(clave, "#000000")

    def cambiar_tema(self, nombre: str):
        if nombre in PALETAS:
            self.tema_actual = nombre
            self.guardar()
            self.notificar()

    def registrar_observer(self, func):
        if func not in self.observers:
            self.observers.append(func)

    def notificar(self):
        for obs in self.observers:
            try:
                obs()
            except Exception:
                pass

    def guardar(self):
        try:
            with open(CONFIG_FILE, "w") as f:
                json.dump({"tema": self.tema_actual}, f)
        except Exception:
            pass

    def cargar(self):
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE) as f:
                    self.tema_actual = json.load(f).get("tema", "claro")
        except Exception:
            self.tema_actual = "claro"

    def nombre_tema(self) -> str:
        nombres = {
            "claro":          "☀ Claro",
            "oscuro":         "🌙 Oscuro",
            "alto_contraste": "⚡ Contraste",
        }
        return nombres.get(self.tema_actual, self.tema_actual)


_tm = ThemeManager()

def tm() -> ThemeManager:
    return _tm