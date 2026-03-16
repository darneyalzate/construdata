/*====================================================
CREAR BASE DE DATOS
====================================================*/

DROP DATABASE IF EXISTS construdata;

CREATE DATABASE construdata;

USE construdata;


/*====================================================
TABLA PROYECTOS
====================================================*/

CREATE TABLE proyectos(
id_proyecto INT AUTO_INCREMENT PRIMARY KEY,
codigo VARCHAR(20) UNIQUE,
nombre VARCHAR(100),
direccion VARCHAR(150),
tipo_construccion VARCHAR(50),
area_total DECIMAL(10,2),
cantidad_pisos INT,
fecha_inicio DATE,
fecha_fin_estimada DATE,
estado VARCHAR(50),
presupuesto DECIMAL(12,2),
gerente_proyecto VARCHAR(100)
);


/*====================================================
TABLA FASES
====================================================*/

CREATE TABLE fases(
id_fase INT AUTO_INCREMENT PRIMARY KEY,
codigo VARCHAR(20),
nombre VARCHAR(100),
fecha_inicio DATE,
fecha_fin DATE,
porcentaje_avance DECIMAL(5,2),
presupuesto DECIMAL(12,2),
id_proyecto INT,
FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto)
);


/*====================================================
TABLA PROVEEDORES
====================================================*/

CREATE TABLE proveedores(
id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
nombre VARCHAR(100),
telefono VARCHAR(20),
direccion VARCHAR(150),
email VARCHAR(100)
);


/*====================================================
TABLA MATERIALES
====================================================*/

CREATE TABLE materiales(
id_material INT AUTO_INCREMENT PRIMARY KEY,
codigo VARCHAR(20),
descripcion VARCHAR(150),
categoria VARCHAR(50),
unidad_medida VARCHAR(20),
especificaciones TEXT,
proveedor_preferido INT,
FOREIGN KEY (proveedor_preferido) REFERENCES proveedores(id_proveedor)
);


/*====================================================
TABLA INVENTARIO
====================================================*/

CREATE TABLE inventario(
id_inventario INT AUTO_INCREMENT PRIMARY KEY,
id_material INT,
cantidad_stock INT,
almacen VARCHAR(100),
ubicacion VARCHAR(100),
precio_unitario DECIMAL(10,2),
fecha_ultima_entrada DATE,
stock_minimo INT,
FOREIGN KEY (id_material) REFERENCES materiales(id_material)
);


/*====================================================
TABLA COMPRAS
====================================================*/

CREATE TABLE compras(
id_compra INT AUTO_INCREMENT PRIMARY KEY,
numero_orden VARCHAR(20),
fecha DATE,
proveedor INT,
condiciones_pago VARCHAR(100),
fecha_entrega DATE,
estado VARCHAR(50),
id_proyecto INT,
FOREIGN KEY (proveedor) REFERENCES proveedores(id_proveedor),
FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto)
);


/*====================================================
DETALLE COMPRA
====================================================*/

CREATE TABLE detalle_compra(
id_detalle INT AUTO_INCREMENT PRIMARY KEY,
id_compra INT,
id_material INT,
cantidad INT,
precio DECIMAL(10,2),
FOREIGN KEY (id_compra) REFERENCES compras(id_compra),
FOREIGN KEY (id_material) REFERENCES materiales(id_material)
);


/*====================================================
TABLA ESPECIALIDADES
====================================================*/

CREATE TABLE especialidades(
id_especialidad INT AUTO_INCREMENT PRIMARY KEY,
codigo VARCHAR(20),
nombre VARCHAR(100),
descripcion TEXT,
nivel_cualificacion VARCHAR(50)
);


/*====================================================
TABLA EMPLEADOS
====================================================*/

CREATE TABLE empleados(
id_empleado INT AUTO_INCREMENT PRIMARY KEY,
dni VARCHAR(20),
nombres VARCHAR(100),
apellidos VARCHAR(100),
fecha_nacimiento DATE,
direccion VARCHAR(150),
telefono VARCHAR(20),
id_especialidad INT,
certificaciones TEXT,
anios_experiencia INT,
fecha_contratacion DATE,
tipo_contrato VARCHAR(50),
salario DECIMAL(10,2),
cargo VARCHAR(50),
FOREIGN KEY (id_especialidad) REFERENCES especialidades(id_especialidad)
);


/*====================================================
TABLA PRESUPUESTO
====================================================*/

CREATE TABLE presupuesto(
id_presupuesto INT AUTO_INCREMENT PRIMARY KEY,
id_proyecto INT,
codigo VARCHAR(20),
descripcion VARCHAR(150),
unidad VARCHAR(20),
cantidad DECIMAL(10,2),
precio_unitario DECIMAL(10,2),
subtotal DECIMAL(12,2),
observaciones TEXT,
FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto)
);


/*====================================================
TABLA GASTOS
====================================================*/

CREATE TABLE gastos(
id_gasto INT AUTO_INCREMENT PRIMARY KEY,
fecha DATE,
tipo_gasto VARCHAR(50),
descripcion VARCHAR(150),
monto DECIMAL(10,2),
factura VARCHAR(50),
proveedor INT,
id_proyecto INT,
id_fase INT,
responsable_aprobacion VARCHAR(100),
FOREIGN KEY (proveedor) REFERENCES proveedores(id_proveedor),
FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto),
FOREIGN KEY (id_fase) REFERENCES fases(id_fase)
);


/*====================================================
TABLA PERMISOS
====================================================*/

CREATE TABLE permisos(
id_permiso INT AUTO_INCREMENT PRIMARY KEY,
codigo VARCHAR(20),
tipo_permiso VARCHAR(100),
id_proyecto INT,
entidad_emisora VARCHAR(100),
fecha_solicitud DATE,
fecha_emision DATE,
fecha_vencimiento DATE,
responsable VARCHAR(100),
estado VARCHAR(50),
FOREIGN KEY (id_proyecto) REFERENCES proyectos(id_proyecto)
);


/*====================================================
DATOS DE EJEMPLO
====================================================*/


/*====================================================
  PROYECTOS  (10 registros)
====================================================*/

INSERT INTO proyectos VALUES
(4,'PR004','Torres del Parque','Barranquilla','Residencial',2200,15,'2024-05-01','2026-05-01','En proceso',850000000,'Maria Lopez'),
(5,'PR005','Hospital Regional','Manizales','Institucional',4500,6,'2024-06-15','2027-06-15','Planeacion',2000000000,'Pedro Sanchez'),
(6,'PR006','Puente Vehicular Norte','Pereira','Infraestructura',800,1,'2023-11-01','2025-11-01','En proceso',600000000,'Jorge Torres'),
(7,'PR007','Parque Empresarial Oriente','Bucaramanga','Comercial',6000,8,'2024-07-01','2027-07-01','Planeacion',1200000000,'Claudia Rios'),
(8,'PR008','Urbanizacion Los Pinos','Cartagena','Residencial',9000,3,'2024-02-01','2026-02-01','En proceso',750000000,'Felipe Castro'),
(9,'PR009','Centro Logistico Sur','Cucuta','Industrial',7500,1,'2023-07-01','2025-07-01','En proceso',480000000,'Andrés Morales'),
(10,'PR010','Colegio Nuevo Horizonte','Armenia','Institucional',3200,4,'2024-09-01','2026-09-01','Planeacion',430000000,'Sandra Vargas');


/*====================================================
  FASES  (10 registros adicionales)
====================================================*/

INSERT INTO fases VALUES
-- Proyecto 2 – Centro Comercial Norte
(4,'F001','Estudios y diseno','2024-03-01','2024-05-01',100,40000000,2),
(5,'F002','Excavacion','2024-05-02','2024-07-01',75,60000000,2),
(6,'F003','Cimentacion','2024-07-05','2024-10-01',30,90000000,2),
-- Proyecto 3 – Bodega Industrial Sur
(7,'F001','Nivelacion terreno','2023-09-01','2023-10-15',100,35000000,3),
(8,'F002','Losa industrial','2023-10-20','2024-01-20',100,95000000,3),
(9,'F003','Estructura metalica','2024-01-25','2024-05-01',80,120000000,3),
-- Proyecto 4 – Torres del Parque
(10,'F001','Movimiento de tierra','2024-05-01','2024-06-15',100,45000000,4),
(11,'F002','Cimentacion profunda','2024-06-20','2024-09-30',55,100000000,4),
(12,'F003','Estructura en concreto','2024-10-01','2025-04-30',10,200000000,4),
-- Proyecto 6 – Puente Vehicular
(13,'F001','Pilas y estribos','2023-11-01','2024-03-01',100,180000000,6);


/*====================================================
  PROVEEDORES  (7 registros adicionales → total 10)
====================================================*/

INSERT INTO proveedores VALUES
(4,'Ferreterias Unidas','3012223344','Medellin','info@ferreteriasunidas.com'),
(5,'Pinturas Tito','3023334455','Cali','ventas@tito.com'),
(6,'Vidrios y Aluminios SA','3034445566','Bogota','vidrios@aluminios.com'),
(7,'Electricos del Norte','3045556677','Barranquilla','norte@electricos.com'),
(8,'Maderas del Pacifico','3056667788','Buenaventura','info@maderas.com'),
(9,'Impermeabilizantes CR','3067778899','Medellin','cr@impermea.com'),
(10,'Equipos Pesados SAS','3078889900','Bogota','equipos@pesados.com');


/*====================================================
  MATERIALES  (6 registros adicionales → total 10)
====================================================*/

INSERT INTO materiales VALUES
(5,'MAT005','Concreto premezclado 3000 PSI','Construccion','Metro cubico','Resistencia minima 3000 PSI a 28 dias',1),
(6,'MAT006','Tuberia PVC 4"','Fontaneria','Metro','Presion nominal 6 bar',4),
(7,'MAT007','Cable electrico THHN #12','Electrico','Metro','Calibre 12 AWG',7),
(8,'MAT008','Pintura vinilica blanca','Acabados','Galon','Exterior e interior',5),
(9,'MAT009','Vidrio templado 8mm','Acabados','Metro cuadrado','Doble templado',6),
(10,'MAT010','Malla electrosoldada','Metal','Rollo','Calibre 4-15x15',3);


/*====================================================
  INVENTARIO  (7 registros adicionales → total 10)
====================================================*/

INSERT INTO inventario VALUES
(4,4,'Ladrillo','Almacen Central','Zona D',950,'2025-03-10',500),
(5,5,80,'Almacen Concreto','Zona E',320000,'2025-03-05',10),
(6,6,300,'Almacen PVC','Estante B',12000,'2025-02-28',50),
(7,7,1500,'Almacen Electrico','Estante C',3500,'2025-03-12',200),
(8,8,60,'Almacen Acabados','Estante D',45000,'2025-03-01',10),
(9,9,40,'Almacen Vidrio','Zona F',85000,'2025-02-20',5),
(10,10,25,'Almacen Hierro','Zona G',95000,'2025-03-08',5);


/*====================================================
  COMPRAS  (8 registros adicionales → total 10)
====================================================*/

INSERT INTO compras VALUES
(3,'OC003','2025-01-15',3,'Contado','2025-01-20','Entregado',3),
(4,'OC004','2025-02-01',4,'Credito 15 dias','2025-02-10','Entregado',1),
(5,'OC005','2025-02-18',5,'Contado','2025-02-22','Entregado',4),
(6,'OC006','2025-03-05',6,'Credito 30 dias','2025-03-12','Pendiente',2),
(7,'OC007','2025-03-10',7,'Contado','2025-03-15','Pendiente',4),
(8,'OC008','2025-03-12',1,'Credito 60 dias','2025-03-25','Pendiente',3),
(9,'OC009','2025-03-14',2,'Contado','2025-03-18','Entregado',2),
(10,'OC010','2025-03-15',10,'Credito 30 dias','2025-03-28','Pendiente',1);


/*====================================================
  DETALLE COMPRA  (10 registros adicionales)
====================================================*/

INSERT INTO detalle_compra VALUES
(4,3,3,300,17500),
(5,3,10,15,90000),
(6,4,1,200,34000),
(7,4,4,5000,900),
(8,5,8,30,44000),
(9,6,9,20,84000),
(10,7,7,500,3400),
(11,8,5,50,315000),
(12,9,2,80,46000),
(13,10,6,200,11500);


/*====================================================
  ESPECIALIDADES  (7 registros adicionales → total 10)
====================================================*/

INSERT INTO especialidades VALUES
(4,'ESP04','Electricista','Instalaciones electricas','Media'),
(5,'ESP05','Plomero','Instalaciones hidraulicas','Media'),
(6,'ESP06','Soldador','Soldadura estructural','Media'),
(7,'ESP07','Residente de obra','Coordinacion tecnica en sitio','Alta'),
(8,'ESP08','Topografo','Levantamientos y replanteos','Alta'),
(9,'ESP09','Seguridad y Salud','HSEQ y prevencion de accidentes','Media'),
(10,'ESP10','Dibujante CAD','Planos arquitectonicos y estructurales','Media');


/*====================================================
  EMPLEADOS  (7 registros adicionales → total 10)
====================================================*/

INSERT INTO empleados VALUES
(4,'11223344','Carlos','Ramirez','1982-09-15','Medellin','3006667788',7,'PMP, PMBOK',15,'2019-03-01','Indefinido',6500000,'Gerente proyecto'),
(5,'22334455','Sofia','Reyes','1992-04-03','Cali','3017778899',8,'CAD, GIS',7,'2023-01-10','Termino fijo',3200000,'Topografa'),
(6,'33445566','Ricardo','Mora','1987-11-28','Bogota','3028889900',4,'RETIE',9,'2021-08-20','Indefinido',3000000,'Electricista'),
(7,'44556677','Natalia','Cruz','1994-06-17','Barranquilla','3039990011',5,'Sena fontaneria',5,'2022-05-05','Termino fijo',2800000,'Plomera'),
(8,'55668899','Hector','Vargas','1980-01-22','Bucaramanga','3050001122',6,'AWS Soldadura',18,'2018-07-15','Indefinido',3500000,'Soldador'),
(9,'66779900','Valentina','Ospina','1996-03-30','Pereira','3061112233',9,'HSEQ nivel 2',4,'2023-06-01','Termino fijo',2600000,'HSEQ'),
(10,'77880011','Daniel','Gutierrez','1991-08-14','Manizales','3072223344',10,'AutoCAD 2D/3D',8,'2020-11-01','Indefinido',3100000,'Dibujante CAD');


/*====================================================
  PRESUPUESTO  (7 registros adicionales → total 10)
====================================================*/

INSERT INTO presupuesto VALUES
(4,1,'P004','Mamposteria muros','m2',800,45000,36000000,'Muros divisorios y fachada'),
(5,1,'P005','Instalaciones electricas','GL',1,45000000,45000000,'Red electrica completa'),
(6,2,'P001','Movimiento de tierra','m3',500,55000,27500000,'Excavacion y lleno'),
(7,2,'P002','Cimentacion zapatas','m3',200,210000,42000000,'Zapatas aisladas'),
(8,3,'P001','Losa de piso industrial','m2',5000,120000,600000000,'Concreto reforzado e=20cm'),
(9,3,'P002','Estructura metalica cubierta','kg',80000,8500,680000000,'Perfiles IPE y canal'),
(10,4,'P001','Pilotes de cimentacion','Unidad',40,950000,38000000,'Pilotes preexcavados D=60cm');


/*====================================================
  GASTOS  (8 registros adicionales → total 10)
====================================================*/

INSERT INTO gastos VALUES
(3,'2025-01-20','Material','Compra varilla corrugada',5250000,'FAC003',3,3,7,'Luis Herrera'),
(4,'2025-02-05','Mano de obra','Pago cuadrilla excavacion',4800000,'FAC004',NULL,1,2,'Carlos Ramirez'),
(5,'2025-02-12','Equipos','Alquiler retroexcavadora',3200000,'FAC005',10,1,2,'Carlos Ramirez'),
(6,'2025-02-25','Material','Compra concreto premezclado',16000000,'FAC006',1,4,11,'Maria Lopez'),
(7,'2025-03-02','Administracion','Papeleria y oficina',350000,'FAC007',NULL,2,4,'Ana Martinez'),
(8,'2025-03-08','Material','Compra pintura vinilica',2700000,'FAC008',5,1,3,'Carlos Ramirez'),
(9,'2025-03-10','Seguridad','Dotacion EPP personal',1200000,'FAC009',4,3,9,'Luis Herrera'),
(10,'2025-03-15','Mano de obra','Pago maestros de obra',9600000,'FAC010',NULL,4,11,'Maria Lopez');


/*====================================================
  PERMISOS  (8 registros adicionales → total 10)
====================================================*/

INSERT INTO permisos VALUES
(3,'PER003','Licencia construccion',2,'Alcaldia Bogota','2024-03-01','2024-04-15','2026-04-15','Ana Martinez','Aprobado'),
(4,'PER004','Permiso ambiental',2,'CAR Bogota','2024-03-05','2024-05-01','2026-05-01','Ana Martinez','En tramite'),
(5,'PER005','Licencia construccion',3,'Alcaldia Cali','2023-08-01','2023-09-10','2025-09-10','Luis Herrera','Aprobado'),
(6,'PER006','Uso del suelo',3,'Planeacion Cali','2023-07-15','2023-08-20','2025-08-20','Luis Herrera','Aprobado'),
(7,'PER007','Licencia construccion',4,'Alcaldia Barranquilla','2024-04-01','2024-05-20','2026-05-20','Maria Lopez','Aprobado'),
(8,'PER008','Permiso vertimientos',3,'Ministerio Ambiente','2023-08-10','2023-10-01','2025-10-01','Luis Herrera','Aprobado'),
(9,'PER009','Permiso ocupacion via',6,'INVIAS Pereira','2023-10-15','2023-11-01','2025-11-01','Jorge Torres','Aprobado'),
(10,'PER010','NSR-10 Diseno sismico',5,'Curaduria Manizales','2024-06-01','2024-08-15','2026-08-15','Pedro Sanchez','En tramite');

/*====================================================
PROCEDIMIENTOS ALMACENADOS
====================================================*/

DELIMITER $$


CREATE PROCEDURE sp_registrar_proyecto(
IN p_codigo VARCHAR(20),
IN p_nombre VARCHAR(100),
IN p_direccion VARCHAR(150),
IN p_tipo VARCHAR(50),
IN p_area DECIMAL(10,2),
IN p_pisos INT,
IN p_inicio DATE,
IN p_fin DATE,
IN p_estado VARCHAR(50),
IN p_presupuesto DECIMAL(12,2),
IN p_gerente VARCHAR(100)
)
BEGIN

INSERT INTO proyectos(
codigo,
nombre,
direccion,
tipo_construccion,
area_total,
cantidad_pisos,
fecha_inicio,
fecha_fin_estimada,
estado,
presupuesto,
gerente_proyecto
)

VALUES(
p_codigo,
p_nombre,
p_direccion,
p_tipo,
p_area,
p_pisos,
p_inicio,
p_fin,
p_estado,
p_presupuesto,
p_gerente
);

END$$



CREATE PROCEDURE sp_registrar_empleado(
IN p_dni VARCHAR(20),
IN p_nombres VARCHAR(100),
IN p_apellidos VARCHAR(100),
IN p_nacimiento DATE,
IN p_direccion VARCHAR(150),
IN p_telefono VARCHAR(20),
IN p_especialidad INT,
IN p_certificaciones TEXT,
IN p_experiencia INT,
IN p_contratacion DATE,
IN p_tipo_contrato VARCHAR(50),
IN p_salario DECIMAL(10,2),
IN p_cargo VARCHAR(50)
)
BEGIN

INSERT INTO empleados(
dni,
nombres,
apellidos,
fecha_nacimiento,
direccion,
telefono,
id_especialidad,
certificaciones,
anios_experiencia,
fecha_contratacion,
tipo_contrato,
salario,
cargo
)

VALUES(
p_dni,
p_nombres,
p_apellidos,
p_nacimiento,
p_direccion,
p_telefono,
p_especialidad,
p_certificaciones,
p_experiencia,
p_contratacion,
p_tipo_contrato,
p_salario,
p_cargo
);

END$$



CREATE PROCEDURE sp_registrar_material(
IN p_codigo VARCHAR(20),
IN p_descripcion VARCHAR(150),
IN p_categoria VARCHAR(50),
IN p_unidad VARCHAR(20),
IN p_especificaciones TEXT,
IN p_proveedor INT
)
BEGIN

INSERT INTO materiales(
codigo,
descripcion,
categoria,
unidad_medida,
especificaciones,
proveedor_preferido
)

VALUES(
p_codigo,
p_descripcion,
p_categoria,
p_unidad,
p_especificaciones,
p_proveedor
);

END$$



CREATE PROCEDURE sp_registrar_compra(
IN p_orden VARCHAR(20),
IN p_fecha DATE,
IN p_proveedor INT,
IN p_condiciones VARCHAR(100),
IN p_entrega DATE,
IN p_estado VARCHAR(50),
IN p_proyecto INT
)
BEGIN

INSERT INTO compras(
numero_orden,
fecha,
proveedor,
condiciones_pago,
fecha_entrega,
estado,
id_proyecto
)

VALUES(
p_orden,
p_fecha,
p_proveedor,
p_condiciones,
p_entrega,
p_estado,
p_proyecto
);

END$$



CREATE PROCEDURE sp_registrar_gasto(
IN p_fecha DATE,
IN p_tipo VARCHAR(50),
IN p_descripcion VARCHAR(150),
IN p_monto DECIMAL(10,2),
IN p_factura VARCHAR(50),
IN p_proveedor INT,
IN p_proyecto INT,
IN p_fase INT,
IN p_responsable VARCHAR(100)
)
BEGIN

INSERT INTO gastos(
fecha,
tipo_gasto,
descripcion,
monto,
factura,
proveedor,
id_proyecto,
id_fase,
responsable_aprobacion
)

VALUES(
p_fecha,
p_tipo,
p_descripcion,
p_monto,
p_factura,
p_proveedor,
p_proyecto,
p_fase,
p_responsable
);

END$$



CREATE PROCEDURE sp_ver_proyectos()
BEGIN

SELECT
codigo,
nombre,
tipo_construccion,
presupuesto,
estado
FROM proyectos;

END$$



CREATE PROCEDURE sp_ver_empleados()
BEGIN

SELECT
e.nombres,
e.apellidos,
s.nombre AS especialidad,
e.cargo,
e.salario

FROM empleados e
JOIN especialidades s
ON e.id_especialidad = s.id_especialidad;

END$$


DELIMITER ;

/*====================================================
CONSULTAS DE PRUEBA
====================================================*/

SELECT * FROM proyectos;
SELECT * FROM empleados;
CALL ver_proyectos();
CALL ver_empleados();

/*====================================================
  VERIFICACION — contar registros por tabla
====================================================*/

SELECT 'proyectos'    AS tabla, COUNT(*) AS total FROM proyectos    UNION ALL
SELECT 'fases',              COUNT(*) FROM fases              UNION ALL
SELECT 'proveedores',        COUNT(*) FROM proveedores        UNION ALL
SELECT 'materiales',         COUNT(*) FROM materiales         UNION ALL
SELECT 'inventario',         COUNT(*) FROM inventario         UNION ALL
SELECT 'compras',            COUNT(*) FROM compras            UNION ALL
SELECT 'detalle_compra',     COUNT(*) FROM detalle_compra     UNION ALL
SELECT 'especialidades',     COUNT(*) FROM especialidades     UNION ALL
SELECT 'empleados',          COUNT(*) FROM empleados          UNION ALL
SELECT 'presupuesto',        COUNT(*) FROM presupuesto        UNION ALL
SELECT 'gastos',             COUNT(*) FROM gastos             UNION ALL
SELECT 'permisos',           COUNT(*) FROM permisos;