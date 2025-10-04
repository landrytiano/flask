-- Table: university
CREATE TABLE university (
  id_universitas VARCHAR(50) PRIMARY KEY,
  nama_universitas VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table: peserta
CREATE TABLE peserta (
  id_peserta VARCHAR(50) PRIMARY KEY,
  nama VARCHAR(255) NOT NULL,
  universitas VARCHAR(50) NOT NULL,
  email VARCHAR(255) UNIQUE NOT NULL,
  no_telp VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (universitas) REFERENCES university(id_universitas)
);

-- Table: lokasi_osce
CREATE TABLE lokasi_osce (
  id_lokasi_osce VARCHAR(50) PRIMARY KEY,
  nama_lokasi VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table: osce
CREATE TABLE osce (
  id_osce VARCHAR(50) PRIMARY KEY,
  id_lokasi_osce VARCHAR(50) NOT NULL,
  tanggal_osce DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (id_lokasi_osce) REFERENCES lokasi_osce(id_lokasi_osce)
);

-- Table: osce_peserta
CREATE TABLE osce_peserta (
  id_osce VARCHAR(50),
  id_peserta VARCHAR(50),
  score DECIMAL(5,2),
  result VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_osce, id_peserta),
  FOREIGN KEY (id_osce) REFERENCES osce(id_osce),
  FOREIGN KEY (id_peserta) REFERENCES peserta(id_peserta)
);

-- Table: cbt
CREATE TABLE cbt (
  id_cbt VARCHAR(50) PRIMARY KEY,
  tanggal_cbt DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Table: cbt_peserta
CREATE TABLE cbt_peserta (
  id_cbt VARCHAR(50),
  id_peserta VARCHAR(50),
  score DECIMAL(5,2),
  result VARCHAR(50),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (id_cbt, id_peserta),
  FOREIGN KEY (id_cbt) REFERENCES cbt(id_cbt),
  FOREIGN KEY (id_peserta) REFERENCES peserta(id_peserta)
);


-- Dummy data for all tables
-- phpMyAdmin SQL Dump
-- version 4.4.15.7
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: Jan 30, 2017 at 10:34 AM
-- Server version: 5.7.17-0ubuntu0.16.04.1
-- PHP Version: 7.0.13-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `crud_flask`
--

-- --------------------------------------------------------

--
-- Table structure for table `phone_book`
--

CREATE TABLE IF NOT EXISTS `phone_book` (
  `id` int(5) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `address` varchar(255) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `phone_book`
--

INSERT INTO `phone_book` (`id`, `name`, `phone`, `address`) VALUES
(16, 'Muhammad Hanif', '0123456789', 'Github');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `phone_book`
--
ALTER TABLE `phone_book`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `phone_book`
--
ALTER TABLE `phone_book`
  MODIFY `id` int(5) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=21;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;


-- Dummy data for all tables
INSERT INTO university (id_universitas, nama_universitas) VALUES ('dummy_uni', 'Dummy University');
INSERT INTO university (id_universitas, nama_universitas) VALUES ('UNIV01', 'Universitas Indonesia');
INSERT INTO university (id_universitas, nama_universitas) VALUES ('UNIV02', 'Universitas Gadjah Mada');
INSERT INTO university (id_universitas, nama_universitas) VALUES ('UNIV03', 'Institut Teknologi Bandung');
INSERT INTO peserta (id_peserta, nama, universitas, email, no_telp) VALUES ('dummy_peserta', 'Dummy Peserta', 'dummy_uni', 'dummy@dummy.com', '08123456789');
INSERT INTO lokasi_osce (id_lokasi_osce, nama_lokasi) VALUES ('dummy_lokasi', 'Dummy Lokasi');
INSERT INTO osce (id_osce, id_lokasi_osce, tanggal_osce) VALUES ('dummy_osce', 'dummy_lokasi', '2025-10-04');
INSERT INTO osce_peserta (id_osce, id_peserta, score, result) VALUES ('dummy_osce', 'dummy_peserta', 80.00, 'Lulus');
INSERT INTO cbt (id_cbt, tanggal_cbt) VALUES ('dummy_cbt', '2025-10-04');
INSERT INTO cbt_peserta (id_cbt, id_peserta, score, result) VALUES ('dummy_cbt', 'dummy_peserta', 75.00, 'Lulus');
-- Dummy data for all tables