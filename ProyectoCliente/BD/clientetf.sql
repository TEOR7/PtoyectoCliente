-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 21-07-2022 a las 05:00:23
-- Versión del servidor: 10.4.24-MariaDB
-- Versión de PHP: 7.4.29

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `clientetf`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ct_direccion`
--

CREATE TABLE `ct_direccion` (
  `id_direccion` int(11) NOT NULL,
  `Pais` varchar(50) NOT NULL,
  `Departamento` varchar(50) NOT NULL,
  `Municipio` varchar(50) NOT NULL,
  `Direccion` varchar(100) NOT NULL,
  `cliente_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `info_cliente`
--

CREATE TABLE `info_cliente` (
  `id_cliente` int(11) NOT NULL,
  `Nombre` varchar(50) NOT NULL,
  `Apellido` varchar(50) NOT NULL,
  `Fechanacimiento` varchar(15) NOT NULL,
  `Sexo` varchar(15) NOT NULL,
  `Telefono` varchar(20) NOT NULL,
  `Correo` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tpdocumento`
--

CREATE TABLE `tpdocumento` (
  `id_documento` int(11) NOT NULL,
  `Tipodocumento` varchar(100) NOT NULL,
  `Numerodoc` varchar(100) NOT NULL,
  `Clientedoc_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `ct_direccion`
--
ALTER TABLE `ct_direccion`
  ADD PRIMARY KEY (`id_direccion`),
  ADD KEY `usuario_id` (`cliente_id`),
  ADD KEY `cliente_id` (`cliente_id`);

--
-- Indices de la tabla `info_cliente`
--
ALTER TABLE `info_cliente`
  ADD PRIMARY KEY (`id_cliente`);

--
-- Indices de la tabla `tpdocumento`
--
ALTER TABLE `tpdocumento`
  ADD PRIMARY KEY (`id_documento`),
  ADD KEY `Clientedoc_id` (`Clientedoc_id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `ct_direccion`
--
ALTER TABLE `ct_direccion`
  MODIFY `id_direccion` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `info_cliente`
--
ALTER TABLE `info_cliente`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tpdocumento`
--
ALTER TABLE `tpdocumento`
  MODIFY `id_documento` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ct_direccion`
--
ALTER TABLE `ct_direccion`
  ADD CONSTRAINT `ct_direccion_ibfk_1` FOREIGN KEY (`cliente_id`) REFERENCES `info_cliente` (`id_cliente`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `tpdocumento`
--
ALTER TABLE `tpdocumento`
  ADD CONSTRAINT `tpdocumento_ibfk_1` FOREIGN KEY (`Clientedoc_id`) REFERENCES `info_cliente` (`id_cliente`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
