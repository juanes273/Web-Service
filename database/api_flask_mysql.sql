-- SQLite SQL Dump
-- Fecha de generación: 25-07-2021 a las 07:47:26

PRAGMA foreign_keys = OFF;

BEGIN TRANSACTION;

-- Estructura de tabla para la tabla `curso`
CREATE TABLE IF NOT EXISTS `curso` (
  `codigo` char(6) NOT NULL,
  `nombre` varchar(30) NOT NULL,
  `creditos` tinyint(1) NOT NULL,
  PRIMARY KEY (`codigo`)
);

-- Volcado de datos para la tabla `curso`
INSERT INTO `curso` (`codigo`, `nombre`, `creditos`) VALUES
('325817', 'Matemática Avanzada', 7),
('587194', 'Analítica de Datos', 6),
('834785', 'Geometría Analítica', 5),
('918415', 'Lógica', 4),
('992514', 'Física Nuclear', 5);

COMMIT;

PRAGMA foreign_keys = ON;
