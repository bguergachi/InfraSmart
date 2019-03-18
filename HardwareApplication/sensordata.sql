-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Mar 18, 2019 at 06:48 AM
-- Server version: 5.7.24
-- PHP Version: 7.2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `smartcityresource_sample`
--

-- --------------------------------------------------------

--
-- Table structure for table `sensordata`
--

DROP TABLE IF EXISTS `sensordata`;
CREATE TABLE IF NOT EXISTS `sensordata` (
  `Id` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceNumber` int(11) NOT NULL,
  `Lat` double NOT NULL,
  `Lng` double NOT NULL,
  `DataType` varchar(20) NOT NULL,
  `Data` float NOT NULL,
  `CollectTime` timestamp NOT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=MyISAM AUTO_INCREMENT=75 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `sensordata`
--

INSERT INTO `sensordata` (`Id`, `DeviceNumber`, `Lat`, `Lng`, `DataType`, `Data`, `CollectTime`) VALUES
(74, 1009, -79.3652141, 43.64631791, 'Grabage(ultrasonic)', 0.0567608, '2019-03-18 06:17:26'),
(73, 1008, -79.38645152, 43.65184241, 'Grabage(ultrasonic)', 0.336134, '2019-03-18 06:17:24'),
(72, 1007, -79.3708487, 43.66110569, 'Grabage(ultrasonic)', 0.13034, '2019-03-18 06:17:21'),
(71, 1006, -79.38603076, 43.67209961, 'Grabage(ultrasonic)', 0.0818915, '2019-03-18 06:17:19'),
(70, 1005, -79.36808013, 43.67084828, 'Grabage(ultrasonic)', 0.027373, '2019-03-18 06:17:17'),
(69, 1004, -79.39342123, 43.65591903, 'Grabage(ultrasonic)', 0.650954, '2019-03-18 06:17:14'),
(68, 1003, -79.38909398, 43.67188004, 'Grabage(ultrasonic)', 0.100942, '2019-03-18 06:17:12'),
(67, 1002, -79.46744499, 42.64582615, 'Grabage(ultrasonic)', 0.0483478, '2019-03-18 06:17:09'),
(66, 1001, -79.40361049, 43.65204426, 'Grabage(ultrasonic)', 0.210704, '2019-03-18 06:17:07');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;