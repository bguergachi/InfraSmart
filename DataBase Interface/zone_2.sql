-- phpMyAdmin SQL Dump
-- version 4.8.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Apr 11, 2019 at 12:39 AM
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
-- Database: `zone_2`
--

-- --------------------------------------------------------

--
-- Table structure for table `markers`
--

DROP TABLE IF EXISTS `markers`;
CREATE TABLE IF NOT EXISTS `markers` (
  `id` int(3) NOT NULL AUTO_INCREMENT,
  `priority` int(11) NOT NULL,
  `date` varchar(20) NOT NULL,
  `time` varchar(20) NOT NULL,
  `address` varchar(80) NOT NULL,
  `lat` float(10,6) NOT NULL,
  `lng` float(10,6) NOT NULL,
  `availability` float NOT NULL,
  `DayOfTheWeek` varchar(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `markers`
--

INSERT INTO `markers` (`id`, `priority`, `date`, `time`, `address`, `lat`, `lng`, `availability`, `DayOfTheWeek`) VALUES
(1, 9, '2019-04-04 10:10:50', '36650.0', '', 43.668907, -79.384209, 0.305337, 'th'),
(2, 5, '2019-04-04 10:10:48', '36648.0', '', 43.679993, -79.370865, 0.0222792, 'th'),
(3, 4, '2019-04-04 10:10:45', '36645.0', '', 43.674049, -79.368492, 0.0878759, 'th'),
(4, 3, '2019-04-04 10:10:43', '36643.0', '', 43.660378, -79.371010, 0.020903, 'th'),
(5, 10, '2019-04-04 10:10:40', '36640.0', '', 43.667458, -79.390732, 0.0655217, 'th'),
(6, 11, '2019-04-04 10:10:38', '36638.0', '', 43.662563, -79.391487, 0.154777, 'th'),
(7, 7, '2019-04-04 10:10:36', '36636.0', '', 43.684078, -79.383957, 0.251256, 'th'),
(8, 6, '2019-04-04 10:10:33', '36633.0', '', 43.683990, -79.374504, 0.0501924, 'th'),
(9, 8, '2019-04-04 10:10:31', '36631.0', '', 43.668324, -79.382248, 0.0459405, 'th'),
(10, 2, '2019-04-04 10:10:28', '36628.0', '', 43.657784, -79.376404, 0.075339, 'th'),
(11, 1, '2019-04-10 13:23:05', 'nan', 'nan', 43.652042, -79.403610, 0, 'th');

-- --------------------------------------------------------

--
-- Table structure for table `meta`
--

DROP TABLE IF EXISTS `meta`;
CREATE TABLE IF NOT EXISTS `meta` (
  `id` int(1) NOT NULL AUTO_INCREMENT,
  `lat` double NOT NULL,
  `lng` double NOT NULL,
  `accuracy` float DEFAULT NULL,
  `scheduled` varchar(5) DEFAULT NULL,
  `threshold` float DEFAULT NULL,
  `day` varchar(2) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `meta`
--

INSERT INTO `meta` (`id`, `lat`, `lng`, `accuracy`, `scheduled`, `threshold`, `day`) VALUES
(1, 43.652042, -79.40361, NULL, NULL, NULL, 'na');

-- --------------------------------------------------------

--
-- Table structure for table `sensordata`
--

DROP TABLE IF EXISTS `sensordata`;
CREATE TABLE IF NOT EXISTS `sensordata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `DeviceNumber` int(11) NOT NULL,
  `Lat` double NOT NULL,
  `Lng` double NOT NULL,
  `Address` varchar(256) NOT NULL,
  `DataType` varchar(20) NOT NULL,
  `Data` float NOT NULL,
  `CollectTime` timestamp NOT NULL,
  `Processed` int(11) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=20 DEFAULT CHARSET=utf8;

--
-- Dumping data for table `sensordata`
--

INSERT INTO `sensordata` (`id`, `DeviceNumber`, `Lat`, `Lng`, `Address`, `DataType`, `Data`, `CollectTime`, `Processed`) VALUES
(10, 1021, 43.65481893, -79.41391841, '2-6 Gore St, Toronto ON', 'Dumpster', 0.064099, '2019-04-04 14:16:56', 0),
(11, 1022, 43.65357923, -79.41163007, '283-303 Manning Ave, Toronto ON M6J 2K8', 'Dumpster', 0.329259, '2019-04-04 14:16:58', 0),
(12, 1023, 43.65969656, -79.41818315, 'Bickford Park, Toronto ON', 'Dumpster', 0.697545, '2019-04-04 14:17:01', 0),
(13, 1024, 43.659742, -79.418657, '329 Harbord Street, Toronto ON', 'Dumpster', 0.212136, '2019-04-04 14:17:03', 0),
(14, 1025, 43.64711035, -79.42194525, '51 Foxley St, Toronto ON M6J 1P9', 'Dumpster', 0.0461074, '2019-04-04 14:17:06', 0),
(15, 1026, 43.66154549, -79.42243635, '717 Shaw St, Toronto ON M6G 3L8', 'Dumpster', 0.0475418, '2019-04-04 14:17:08', 0),
(16, 1027, 43.646018, -79.416847, 'Shaw St, Toronto ON', 'Dumpster', 0.00699301, '2019-04-04 14:17:11', 0),
(17, 1028, 43.650426, -79.417219, '261-267 Crawford Street, Toronto ON', 'Dumpster', 0.0530371, '2019-04-04 14:17:13', 0),
(18, 1029, 43.42768897, -79.65243354, '70-62 Rusholme Rd, Toronto ON', 'Dumpster', 0.265511, '2019-04-04 14:17:15', 0),
(19, 1030, 43.402172, -79.653216, '19-1 Whales Ave, Toronto ON', 'Dumpster', 0.203638, '2019-04-04 14:17:18', 0);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
