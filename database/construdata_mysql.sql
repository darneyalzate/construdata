-- ============================================================
--  ConstruData — Base de datos MySQL
--  Módulo: Profundización y Aplicaciones en Bases de Datos
--  Compatible con: MySQL 5.7+ / MariaDB 10+
-- ============================================================

DROP DATABASE IF EXISTS construdata;

CREATE DATABASE construdata
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_spanish_ci;

USE construdata;

-- ─────────────────────────────────────────────
--  TABLA: proveedores
-- ─────────────────────────────────────────────
CREATE TABLE proveedores (
    id_proveedor   INT AUTO_INCREMENT PRIMARY KEY,
    nombre         VARCHAR(100) NOT NULL,
    telefono       VARCHAR(20)  DEFAULT '',
    direccion      VARCHAR(200) DEFAULT '',
    email          VARCHAR(100) DEFAULT '',
    contacto       VARCHAR(100) DEFAULT '',
    categoria      VARCHAR(60)  DEFAULT '',
    fecha_registro DATETIME     DEFAULT NOW()
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
--  TABLA: proyectos
-- ─────────────────────────────────────────────
CREATE TABLE proyectos (
    id_proyecto       INT AUTO_INCREMENT PRIMARY KEY,
    codigo            VARCHAR(30)   NOT NULL UNIQUE,
    nombre            VARCHAR(150)  NOT NULL,
    direccion         VARCHAR(200)  DEFAULT '',
    tipo_construccion VARCHAR(80)   DEFAULT '',
    area_total        DECIMAL(12,2),
    cantidad_pisos    INT,
    estado            VARCHAR(30)   DEFAULT 'Activo',
    presupuesto       DECIMAL(15,2),
    gerente_proyecto  VARCHAR(100)  DEFAULT '',
    fecha_inicio      DATE,
    fecha_fin         DATE,
    imagen            VARCHAR(300)  DEFAULT '',
    fecha_registro    DATETIME      DEFAULT NOW()
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
--  TABLA: empleados
-- ─────────────────────────────────────────────
CREATE TABLE empleados (
    id_empleado    INT AUTO_INCREMENT PRIMARY KEY,
    dni            VARCHAR(20)  NOT NULL UNIQUE,
    nombres        VARCHAR(80)  NOT NULL,
    apellidos      VARCHAR(80)  NOT NULL,
    telefono       VARCHAR(20)  DEFAULT '',
    cargo          VARCHAR(80)  DEFAULT '',
    salario        DECIMAL(12,2),
    tipo_contrato  VARCHAR(50)  DEFAULT '',
    email          VARCHAR(100) DEFAULT '',
    fecha_ingreso  DATE,
    foto           VARCHAR(300) DEFAULT '',
    fecha_registro DATETIME     DEFAULT NOW()
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
--  TABLA: materiales
-- ─────────────────────────────────────────────
CREATE TABLE materiales (
    id_material         INT AUTO_INCREMENT PRIMARY KEY,
    codigo              VARCHAR(30)   NOT NULL UNIQUE,
    descripcion         VARCHAR(150)  NOT NULL,
    categoria           VARCHAR(60)   DEFAULT '',
    unidad_medida       VARCHAR(20)   DEFAULT '',
    precio_unitario     DECIMAL(12,2) DEFAULT 0,
    stock               DECIMAL(12,2) DEFAULT 0,
    proveedor_preferido INT,
    imagen              VARCHAR(300)  DEFAULT '',
    fecha_registro      DATETIME      DEFAULT NOW(),
    FOREIGN KEY (proveedor_preferido)
        REFERENCES proveedores(id_proveedor)
        ON DELETE SET NULL
) ENGINE=InnoDB;

-- ─────────────────────────────────────────────
--  DATOS DE EJEMPLO
-- ─────────────────────────────────────────────

-- 6 Proveedores
INSERT INTO proveedores (nombre, telefono, email, contacto, categoria) VALUES
('Aceros del Valle S.A.',     '3001234567', 'ventas@acerosvalle.com',      'Jorge Méndez',    'Acero'),
('CemenTec Colombia',         '3119876543', 'pedidos@cementec.com.co',     'Ana Ríos',        'Cementos'),
('Maderas El Pino',           '3204567890', 'info@maderaselpino.com',      'Luis Herrera',    'Madera'),
('Eléctricos San José',       '3157654321', 'contacto@electricossj.com',   'Marta Ospina',    'Eléctrico'),
('Pinturas y Acabados León',  '3112345678', 'ventas@pinturesleon.com',     'Pedro León',      'Pintura'),
('Agregados del Río S.A.S.',  '3189876541', 'info@agregadosrio.com',       'Sandra Vargas',   'Agregados');

-- 5 Proyectos
INSERT INTO proyectos
    (codigo, nombre, direccion, tipo_construccion, area_total,
     cantidad_pisos, estado, presupuesto, gerente_proyecto,
     fecha_inicio, fecha_fin) VALUES
('PRY-001', 'Torre Empresarial Norte',
    'Calle 80 # 45-23, Bogotá',           'Comercial',    4500.00, 12, 'Activo',     8500000000.00, 'Ing. Carlos Ruiz',     '2024-03-01', '2025-12-31'),
('PRY-002', 'Conjunto Residencial Los Pinos',
    'Carrera 15 # 102-45, Medellín',      'Residencial', 12000.00,  5, 'En pausa',  15200000000.00, 'Arq. Laura Gómez',     '2024-01-15', '2026-06-30'),
('PRY-003', 'Centro Comercial Plaza Sur',
    'Av. 68 # 23-10, Bogotá',             'Comercial',    8200.00,  3, 'Activo',    22000000000.00, 'Ing. Roberto Pardo',   '2024-06-01', '2026-03-31'),
('PRY-004', 'Bodega Industrial Zona Franca',
    'Km 5 Vía Cali-Palmira, Cali',        'Industrial',   6000.00,  2, 'Finalizado', 4800000000.00, 'Ing. Mónica Suárez',   '2023-02-01', '2024-08-30'),
('PRY-005', 'Urbanización Villa del Campo',
    'Carrera 9 # 55-80, Bucaramanga',     'Residencial',  9500.00,  4, 'Activo',    11300000000.00, 'Arq. Felipe Torres',   '2024-09-01', '2026-12-15');

-- 6 Empleados
INSERT INTO empleados
    (dni, nombres, apellidos, telefono, cargo,
     salario, tipo_contrato, email, fecha_ingreso) VALUES
('1020345678', 'Carlos Andrés',   'Ruiz Martínez',   '3156789012', 'Ingeniero Civil',      6500000.00, 'Indefinido',   'c.ruiz@construdata.com',      '2023-06-01'),
('1098765432', 'Laura Valentina', 'Gómez Torres',    '3209876543', 'Arquitecta',           5800000.00, 'Término fijo', 'l.gomez@construdata.com',     '2023-09-15'),
('1122334455', 'Miguel Ángel',    'Pedroza López',   '3001234567', 'Maestro de Obra',      3200000.00, 'Obra o labor', 'm.pedroza@construdata.com',   '2024-01-10'),
('1035678901', 'Diana Marcela',   'Herrera Cano',    '3174561230', 'Residente de Obra',    4100000.00, 'Término fijo', 'd.herrera@construdata.com',   '2023-11-01'),
('1067890123', 'Roberto',         'Pardo Quintero',  '3123456789', 'Director de Proyecto', 8200000.00, 'Indefinido',   'r.pardo@construdata.com',     '2022-03-15'),
('1089012345', 'Mónica Patricia', 'Suárez Villalba', '3198765432', 'Ingeniera Eléctrica',  5500000.00, 'Indefinido',   'm.suarez@construdata.com',    '2023-07-20');

-- 8 Materiales
INSERT INTO materiales
    (codigo, descripcion, categoria, unidad_medida,
     precio_unitario, stock, proveedor_preferido) VALUES
('MAT-001', 'Cemento Portland tipo I x 50kg',    'Cementos',   'bolsa',   28500.00,  500.00, 2),
('MAT-002', 'Varilla corrugada 1/2" x 6m',       'Acero',      'unidad',  18900.00, 1200.00, 1),
('MAT-003', 'Tablón pino 1" x 12" x 3m',         'Madera',     'unidad',  22000.00,   80.00, 3),
('MAT-004', 'Cable THHN calibre 12',              'Eléctrico',  'ml',       1800.00,  600.00, 4),
('MAT-005', 'Pintura vinilo interior blanco 4L',  'Pintura',    'galón',   38000.00,  150.00, 5),
('MAT-006', 'Arena de río lavada',                'Agregados',  'm³',      85000.00,  200.00, 6),
('MAT-007', 'Gravilla triturada 3/4"',            'Agregados',  'm³',      95000.00,  180.00, 6),
('MAT-008', 'Ladrillo tolete estándar x 1000 u',  'Mampostería','millar', 420000.00,   60.00, 2);


-- ─────────────────────────────────────────────
--  VERIFICACIÓN FINAL
-- ─────────────────────────────────────────────
DESCRIBE proyectos;

SELECT 'proveedores' AS tabla, COUNT(*) AS registros FROM proveedores
UNION ALL
SELECT 'proyectos',  COUNT(*) FROM proyectos
UNION ALL
SELECT 'empleados',  COUNT(*) FROM empleados
UNION ALL
SELECT 'materiales', COUNT(*) FROM materiales;