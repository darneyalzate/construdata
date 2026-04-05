import sys as _sys, os as _os
_ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
_sys.path.insert(0, _ROOT)

import os
import sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQLITE_PATH = os.path.join(BASE_DIR, "database", "construdata.db")

MYSQL_CONFIG = {
    "host":     "localhost",
    "user":     "root",
    "password": "",
    "database": "construdata",
    "port":     3306,
}

try:
    import mysql.connector
    MYSQL_DISPONIBLE = True
except ImportError:
    MYSQL_DISPONIBLE = False


class Database:
    """Singleton — detecta MySQL o usa SQLite automáticamente."""
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def __init__(self):
        self._motor = self._detectar_motor()
        if self._motor == "sqlite":
            os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
            self._crear_tablas_sqlite()

    def _detectar_motor(self):
        if MYSQL_DISPONIBLE:
            try:
                con = mysql.connector.connect(**MYSQL_CONFIG)
                con.close()
                return "mysql"
            except Exception:
                pass
        return "sqlite"

    @property
    def motor(self):
        return self._motor

    def conectar(self):
        if self._motor == "mysql":
            return mysql.connector.connect(**MYSQL_CONFIG)
        return sqlite3.connect(SQLITE_PATH)

    def _adaptar_sql(self, sql: str) -> str:
        """
        Los controladores escriben SQL con '?' (estilo SQLite).
        Si el motor es MySQL, convertimos '?' → '%s'.
        Si el motor es SQLite, dejamos '?' tal cual.
        """
        if self._motor == "mysql":
            return sql.replace("?", "%s")
        return sql  # SQLite ya usa '?'

    def ejecutar(self, sql, params=()):
        sql = self._adaptar_sql(sql)
        con = self.conectar()
        try:
            cur = con.cursor()
            cur.execute(sql, params)
            con.commit()
            return cur.lastrowid
        finally:
            con.close()

    def consultar(self, sql, params=()):
        sql = self._adaptar_sql(sql)
        con = self.conectar()
        try:
            cur = con.cursor()
            cur.execute(sql, params)
            return cur.fetchall()
        finally:
            con.close()

    def consultar_uno(self, sql, params=()):
        r = self.consultar(sql, params)
        return r[0] if r else None

    def _crear_tablas_sqlite(self):
        con = sqlite3.connect(SQLITE_PATH)
        cur = con.cursor()
        cur.executescript("""
            CREATE TABLE IF NOT EXISTS proveedores (
                id_proveedor   INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre         TEXT NOT NULL,
                telefono       TEXT DEFAULT '',
                direccion      TEXT DEFAULT '',
                email          TEXT DEFAULT '',
                contacto       TEXT DEFAULT '',
                categoria      TEXT DEFAULT '',
                fecha_registro TEXT DEFAULT (datetime('now','localtime'))
            );
            CREATE TABLE IF NOT EXISTS proyectos (
                id_proyecto        INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo             TEXT NOT NULL UNIQUE,
                nombre             TEXT NOT NULL,
                direccion          TEXT DEFAULT '',
                tipo_construccion  TEXT DEFAULT '',
                area_total         REAL,
                cantidad_pisos     INTEGER,
                estado             TEXT DEFAULT 'Activo',
                presupuesto        REAL,
                gerente_proyecto   TEXT DEFAULT '',
                fecha_inicio       TEXT DEFAULT '',
                fecha_fin          TEXT DEFAULT '',
                imagen             TEXT DEFAULT '',
                fecha_registro     TEXT DEFAULT (datetime('now','localtime'))
            );
            CREATE TABLE IF NOT EXISTS empleados (
                id_empleado    INTEGER PRIMARY KEY AUTOINCREMENT,
                dni            TEXT NOT NULL UNIQUE,
                nombres        TEXT NOT NULL,
                apellidos      TEXT NOT NULL,
                telefono       TEXT DEFAULT '',
                cargo          TEXT DEFAULT '',
                salario        REAL,
                tipo_contrato  TEXT DEFAULT '',
                email          TEXT DEFAULT '',
                fecha_ingreso  TEXT DEFAULT '',
                foto           TEXT DEFAULT '',
                fecha_registro TEXT DEFAULT (datetime('now','localtime'))
            );
            CREATE TABLE IF NOT EXISTS materiales (
                id_material         INTEGER PRIMARY KEY AUTOINCREMENT,
                codigo              TEXT NOT NULL UNIQUE,
                descripcion         TEXT NOT NULL,
                categoria           TEXT DEFAULT '',
                unidad_medida       TEXT DEFAULT '',
                precio_unitario     REAL DEFAULT 0,
                stock               REAL DEFAULT 0,
                proveedor_preferido INTEGER,
                imagen              TEXT DEFAULT '',
                fecha_registro      TEXT DEFAULT (datetime('now','localtime'))
            );
        """)
        con.commit()
        con.close()