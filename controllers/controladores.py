import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)
"""
controllers/controladores.py
Lógica de negocio y acceso a datos — Patrón MVC
"""

from models.database import Database
from models.modelos import Proyecto, Empleado, Material, Proveedor


db = Database.get_instance()


# ─────────────────────────── PROYECTOS ───────────────────────────

class ProyectoController:

    @staticmethod
    def existe(codigo: str) -> bool:
        return db.consultar_uno(
            "SELECT id_proyecto FROM proyectos WHERE codigo=?", (codigo,)
        ) is not None

    @staticmethod
    def registrar(p: Proyecto) -> int:
        return db.ejecutar("""
            INSERT INTO proyectos
                (codigo, nombre, direccion, tipo_construccion,
                 area_total, cantidad_pisos, estado, presupuesto,
                 gerente_proyecto, fecha_inicio, fecha_fin, imagen)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """, p.to_tuple())

    @staticmethod
    def actualizar(p: Proyecto) -> None:
        db.ejecutar("""
            UPDATE proyectos SET
                nombre=?, direccion=?, tipo_construccion=?,
                area_total=?, cantidad_pisos=?, estado=?,
                presupuesto=?, gerente_proyecto=?,
                fecha_inicio=?, fecha_fin=?, imagen=?
            WHERE id_proyecto=?
        """, (
            p.nombre, p.direccion, p.tipo_construccion,
            p.area_total, p.cantidad_pisos, p.estado,
            p.presupuesto, p.gerente_proyecto,
            p.fecha_inicio, p.fecha_fin, p.imagen, p.id_proyecto
        ))

    @staticmethod
    def eliminar(id_proyecto: int) -> None:
        db.ejecutar("DELETE FROM proyectos WHERE id_proyecto=?", (id_proyecto,))

    @staticmethod
    def listar(filtro_estado: str = "", fecha_ini: str = "", fecha_fin: str = ""):
        sql = """
        SELECT
            id_proyecto,
            codigo,
            nombre,
            direccion,
            tipo_construccion,
            area_total,
            cantidad_pisos,
            estado,
            presupuesto,
            gerente_proyecto,
            fecha_inicio,
            fecha_fin,
            imagen
        FROM proyectos WHERE 1=1"""
        params = []
        if filtro_estado:
            sql += " AND estado=?"
            params.append(filtro_estado)
        if fecha_ini:
            sql += " AND fecha_inicio >= ?"
            params.append(fecha_ini)
        if fecha_fin:
            sql += " AND fecha_fin <= ?"
            params.append(fecha_fin)
        sql += " ORDER BY id_proyecto DESC"
        return db.consultar(sql, params)

    @staticmethod
    def buscar(termino: str):
        t = f"%{termino}%"
        return db.consultar("""
            SELECT id_proyecto, codigo, nombre, direccion, tipo_construccion,
                   area_total, cantidad_pisos, estado, presupuesto,
                   gerente_proyecto, fecha_inicio, fecha_fin
            FROM proyectos
            WHERE codigo LIKE ? OR nombre LIKE ? OR gerente_proyecto LIKE ?
            ORDER BY nombre
        """, (t, t, t))


# ─────────────────────────── EMPLEADOS ───────────────────────────

class EmpleadoController:

    @staticmethod
    def existe(dni: str) -> bool:
        return db.consultar_uno(
            "SELECT id_empleado FROM empleados WHERE dni=?", (dni,)
        ) is not None

    @staticmethod
    def registrar(e: Empleado) -> int:
        return db.ejecutar("""
            INSERT INTO empleados
                (dni, nombres, apellidos, telefono, cargo,
                 salario, tipo_contrato, email, fecha_ingreso, foto)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, e.to_tuple())

    @staticmethod
    def actualizar(e: Empleado) -> None:
        db.ejecutar("""
            UPDATE empleados SET
                nombres=?, apellidos=?, telefono=?, cargo=?,
                salario=?, tipo_contrato=?, email=?, fecha_ingreso=?, foto=?
            WHERE id_empleado=?
        """, (
            e.nombres, e.apellidos, e.telefono, e.cargo,
            e.salario, e.tipo_contrato, e.email, e.fecha_ingreso,
            e.foto, e.id_empleado
        ))

    @staticmethod
    def eliminar(id_empleado: int) -> None:
        db.ejecutar("DELETE FROM empleados WHERE id_empleado=?", (id_empleado,))

    @staticmethod
    def listar(filtro_cargo: str = "", fecha_ini: str = "", fecha_fin: str = ""):
        sql = """SELECT id_empleado, dni, nombres, apellidos, telefono,
                        cargo, salario, tipo_contrato, email, fecha_ingreso, foto
                 FROM empleados WHERE 1=1"""
        params = []
        if filtro_cargo:
            sql += " AND cargo LIKE ?"
            params.append(f"%{filtro_cargo}%")
        if fecha_ini:
            sql += " AND fecha_ingreso >= ?"
            params.append(fecha_ini)
        if fecha_fin:
            sql += " AND fecha_ingreso <= ?"
            params.append(fecha_fin)
        sql += " ORDER BY apellidos, nombres"
        return db.consultar(sql, params)

    @staticmethod
    def buscar(termino: str):
        t = f"%{termino}%"
        return db.consultar("""
            SELECT id_empleado, dni, nombres, apellidos, telefono,
                   cargo, salario, tipo_contrato, email, fecha_ingreso
            FROM empleados
            WHERE dni LIKE ? OR nombres LIKE ? OR apellidos LIKE ? OR cargo LIKE ?
            ORDER BY apellidos
        """, (t, t, t, t))


# ─────────────────────────── MATERIALES ───────────────────────────

class MaterialController:

    @staticmethod
    def existe(codigo: str) -> bool:
        return db.consultar_uno(
            "SELECT id_material FROM materiales WHERE codigo=?", (codigo,)
        ) is not None

    @staticmethod
    def registrar(m: Material) -> int:
        return db.ejecutar("""
            INSERT INTO materiales
                (codigo, descripcion, categoria, unidad_medida,
                 precio_unitario, stock, proveedor_preferido, imagen)
            VALUES (?,?,?,?,?,?,?,?)
        """, m.to_tuple())

    @staticmethod
    def actualizar(m: Material) -> None:
        db.ejecutar("""
            UPDATE materiales SET
                descripcion=?, categoria=?, unidad_medida=?,
                precio_unitario=?, stock=?, proveedor_preferido=?, imagen=?
            WHERE id_material=?
        """, (
            m.descripcion, m.categoria, m.unidad_medida,
            m.precio_unitario, m.stock, m.proveedor_preferido,
            m.imagen, m.id_material
        ))

    @staticmethod
    def eliminar(id_material: int) -> None:
        db.ejecutar("DELETE FROM materiales WHERE id_material=?", (id_material,))

    @staticmethod
    def listar(filtro_cat: str = ""):
        sql = """SELECT id_material, codigo, descripcion, categoria,
                        unidad_medida, precio_unitario, stock, proveedor_preferido
                 FROM materiales WHERE 1=1"""
        params = []
        if filtro_cat:
            sql += " AND categoria LIKE ?"
            params.append(f"%{filtro_cat}%")
        sql += " ORDER BY descripcion"
        return db.consultar(sql, params)

    @staticmethod
    def buscar(termino: str):
        t = f"%{termino}%"
        return db.consultar("""
            SELECT id_material, codigo, descripcion, categoria,
                   unidad_medida, precio_unitario, stock
            FROM materiales
            WHERE codigo LIKE ? OR descripcion LIKE ? OR categoria LIKE ?
            ORDER BY descripcion
        """, (t, t, t))


# ─────────────────────────── PROVEEDORES ───────────────────────────

class ProveedorController:

    @staticmethod
    def existe(nombre: str, telefono: str) -> bool:
        return db.consultar_uno(
            "SELECT id_proveedor FROM proveedores WHERE nombre=? AND telefono=?",
            (nombre, telefono)
        ) is not None

    @staticmethod
    def registrar(p: Proveedor) -> int:
        return db.ejecutar("""
            INSERT INTO proveedores
                (nombre, telefono, direccion, email, contacto, categoria)
            VALUES (?,?,?,?,?,?)
        """, p.to_tuple())

    @staticmethod
    def actualizar(p: Proveedor) -> None:
        db.ejecutar("""
            UPDATE proveedores SET
                nombre=?, telefono=?, direccion=?,
                email=?, contacto=?, categoria=?
            WHERE id_proveedor=?
        """, (
            p.nombre, p.telefono, p.direccion,
            p.email, p.contacto, p.categoria, p.id_proveedor
        ))

    @staticmethod
    def eliminar(id_proveedor: int) -> None:
        db.ejecutar("DELETE FROM proveedores WHERE id_proveedor=?", (id_proveedor,))

    @staticmethod
    def listar(filtro_cat: str = ""):
        sql = """SELECT id_proveedor, nombre, telefono, direccion,
                        email, contacto, categoria
                 FROM proveedores WHERE 1=1"""
        params = []
        if filtro_cat:
            sql += " AND categoria LIKE ?"
            params.append(f"%{filtro_cat}%")
        sql += " ORDER BY nombre"
        return db.consultar(sql, params)

    @staticmethod
    def buscar(termino: str):
        t = f"%{termino}%"
        return db.consultar("""
            SELECT id_proveedor, nombre, telefono, direccion, email, contacto, categoria
            FROM proveedores
            WHERE nombre LIKE ? OR email LIKE ? OR categoria LIKE ?
            ORDER BY nombre
        """, (t, t, t))

    @staticmethod
    def lista_nombres():
        """Devuelve [(id, nombre)] para combos."""
        return db.consultar(
            "SELECT id_proveedor, nombre FROM proveedores ORDER BY nombre"
        )