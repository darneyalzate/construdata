import json
import os

CONFIG_FILE = "tema_config.json"

PALETAS = {
    "claro": {
        "fondo": "#f0f0f0",
        "barra_bg": "#ffffff",
        "barra_fg": "#000000",
        "barra_sub": "#555",
        "estado_bg": "#dddddd",
        "estado_fg": "#000",
        "primario": "#1976d2",
        "primario_lt": "#42a5f5",
        "primario_dk": "#0d47a1",
        "texto_inv": "#ffffff"
    },
    "oscuro": {
        "fondo": "#2b2b2b",
        "barra_bg": "#1f1f1f",
        "barra_fg": "#ffffff",
        "barra_sub": "#bbbbbb",
        "estado_bg": "#1f1f1f",
        "estado_fg": "#ffffff",
        "primario": "#4caf50",
        "primario_lt": "#81c784",
        "primario_dk": "#1b5e20",
        "texto_inv": "#ffffff"
    },
    "alto_contraste": {
        "fondo": "#000000",
        "barra_bg": "#000000",
        "barra_fg": "#ffffff",
        "barra_sub": "#ffff00",
        "estado_bg": "#000000",
        "estado_fg": "#ffffff",
        "primario": "#ffff00",
        "primario_lt": "#ffff99",
        "primario_dk": "#cccc00",
        "texto_inv": "#000000"
    }
}


class ThemeManager:
    def __init__(self):
        self.tema_actual = "claro"
        self.observers = []
        self.cargar()

    def color(self, clave):
        return PALETAS[self.tema_actual].get(clave, "#000")

    def cambiar_tema(self, nombre):
        self.tema_actual = nombre
        self.guardar()
        self.notificar()

    def registrar_observer(self, func):
        self.observers.append(func)

    def notificar(self):
        for obs in self.observers:
            obs()

    def guardar(self):
        with open(CONFIG_FILE, "w") as f:
            json.dump({"tema": self.tema_actual}, f)

    def cargar(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE) as f:
                self.tema_actual = json.load(f).get("tema", "claro")

    def nombre_tema(self):
        return self.tema_actual


_tm = ThemeManager()

def tm():
    return _tm