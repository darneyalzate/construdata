"""
models/modelos.py
Clases de dominio (POO) para cada entidad del sistema
"""
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Proyecto:
    codigo: str
    nombre: str
    direccion: str = ""
    tipo_construccion: str = ""
    area_total: Optional[float] = None
    cantidad_pisos: Optional[int] = None
    estado: str = "Activo"
    presupuesto: Optional[float] = None
    gerente_proyecto: str = ""
    fecha_inicio: str = ""
    fecha_fin: str = ""
    imagen: str = ""
    id_proyecto: Optional[int] = None

    def es_valido(self):
        return bool(self.codigo.strip()) and bool(self.nombre.strip())

    def to_tuple(self):
        return (
            self.codigo, self.nombre, self.direccion, self.tipo_construccion,
            self.area_total, self.cantidad_pisos, self.estado,
            self.presupuesto, self.gerente_proyecto,
            self.fecha_inicio, self.fecha_fin, self.imagen
        )


@dataclass
class Empleado:
    dni: str
    nombres: str
    apellidos: str
    telefono: str = ""
    cargo: str = ""
    salario: Optional[float] = None
    tipo_contrato: str = ""
    email: str = ""
    fecha_ingreso: str = ""
    foto: str = ""
    id_empleado: Optional[int] = None

    def es_valido(self):
        return (bool(self.dni.strip()) and
                bool(self.nombres.strip()) and
                bool(self.apellidos.strip()))

    def to_tuple(self):
        return (
            self.dni, self.nombres, self.apellidos, self.telefono,
            self.cargo, self.salario, self.tipo_contrato,
            self.email, self.fecha_ingreso, self.foto
        )


@dataclass
class Material:
    codigo: str
    descripcion: str
    categoria: str = ""
    unidad_medida: str = ""
    precio_unitario: float = 0.0
    stock: float = 0.0
    proveedor_preferido: Optional[int] = None
    imagen: str = ""
    id_material: Optional[int] = None

    def es_valido(self):
        return bool(self.codigo.strip()) and bool(self.descripcion.strip())

    def to_tuple(self):
        return (
            self.codigo, self.descripcion, self.categoria,
            self.unidad_medida, self.precio_unitario, self.stock,
            self.proveedor_preferido, self.imagen
        )


@dataclass
class Proveedor:
    nombre: str
    telefono: str = ""
    direccion: str = ""
    email: str = ""
    contacto: str = ""
    categoria: str = ""
    id_proveedor: Optional[int] = None

    def es_valido(self):
        return bool(self.nombre.strip())

    def to_tuple(self):
        return (
            self.nombre, self.telefono, self.direccion,
            self.email, self.contacto, self.categoria
        )