# 🏗 ConstruData — Sistema de Gestión de Construcción

Sistema de escritorio en **Python + Tkinter** con arquitectura **MVC + POO**, base de datos **MySQL/SQLite**, exportación a **Excel y PDF**, y 3 temas visuales intercambiables.

---

## ⚙ Instalación

```bash
pip install -r requirements.txt
python main.py
```

**Base de datos MySQL** (opcional — usa SQLite automáticamente si no hay MySQL):
```bash
mysql -u root -p < database/construdata_mysql.sql
```

---

## ✅ Funcionalidades

- **4 módulos:** Proyectos · Empleados · Materiales · Proveedores
- **CRUD completo** con búsqueda, filtros y confirmación antes de eliminar
- **Validaciones:** numérica en tiempo real, email con regex, longitud mín/máx, tkcalendar para fechas
- **Imágenes con Pillow** en 3 formularios (JPG, PNG, GIF · máx. 5 MB)
- **Exportación** a Excel (openpyxl) y PDF (reportlab) con filtros aplicados
- **3 temas visuales:** ☀ Claro · 🌙 Oscuro · ⚡ Alto Contraste

---

## 🛠 Tecnologías

`Python 3` · `Tkinter` · `MySQL / SQLite` · `Pillow` · `openpyxl` · `ReportLab` · `tkcalendar`
