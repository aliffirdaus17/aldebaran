-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 04, 2026 at 03:59 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_raport_m_alif`
--

-- --------------------------------------------------------

--
-- Table structure for table `absensi_alif`
--

CREATE TABLE `absensi_alif` (
  `id_absen` varchar(10) NOT NULL,
  `nis` int(11) NOT NULL,
  `Tanggal` date NOT NULL,
  `Status` enum('Hadir','Izin','Sakit','Alfa') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `absensi_alif`
--

INSERT INTO `absensi_alif` (`id_absen`, `nis`, `Tanggal`, `Status`) VALUES
('15', 1024329, '2026-01-15', 'Alfa'),
('16', 10243300, '2026-01-15', 'Hadir'),
('17', 10243301, '2026-01-15', 'Hadir'),
('18', 10243302, '2026-01-15', 'Hadir');

-- --------------------------------------------------------

--
-- Table structure for table `kelas_alif`
--

CREATE TABLE `kelas_alif` (
  `id_kelas` varchar(10) NOT NULL,
  `nama_kelas` varchar(20) NOT NULL,
  `id_walikelas` varchar(18) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `kelas_alif`
--

INSERT INTO `kelas_alif` (`id_kelas`, `nama_kelas`, `id_walikelas`) VALUES
('IK001', 'XI PPLG B', 'IW001'),
('IK002', 'XI PPLG A', 'IW002'),
('IK003', 'X PPLG B', 'IW003'),
('IK004', 'X PPLG A', 'IW004');

-- --------------------------------------------------------

--
-- Table structure for table `mapel_alif`
--

CREATE TABLE `mapel_alif` (
  `id_mapel` varchar(10) NOT NULL,
  `nama_mapel` varchar(15) NOT NULL,
  `kkm` decimal(10,0) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `mapel_alif`
--

INSERT INTO `mapel_alif` (`id_mapel`, `nama_mapel`, `kkm`) VALUES
('IMP001', 'Matematika', 75),
('IMP002', 'Olahraga', 75),
('IMP003', 'PPLG', 75),
('IMP004', 'Sejarah', 75);

-- --------------------------------------------------------

--
-- Table structure for table `nilai_alif`
--

CREATE TABLE `nilai_alif` (
  `id_nilai` varchar(10) NOT NULL,
  `nis` int(11) NOT NULL,
  `id_mapel` varchar(10) NOT NULL,
  `nilai_tugas` int(11) NOT NULL,
  `nilai_uts` int(11) NOT NULL,
  `nilai_uas` int(11) NOT NULL,
  `nilai_akhir` int(11) NOT NULL,
  `Deskripsi` varchar(50) NOT NULL,
  `Semester` enum('Ganjil','Genap') NOT NULL,
  `tahun_ajaran` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `nilai_alif`
--

INSERT INTO `nilai_alif` (`id_nilai`, `nis`, `id_mapel`, `nilai_tugas`, `nilai_uts`, `nilai_uas`, `nilai_akhir`, `Deskripsi`, `Semester`, `tahun_ajaran`) VALUES
('NP001', 1024329, 'IMP001', 90, 90, 80, 87, 'nice', 'Genap', 2025),
('NP002', 10243300, 'IMP002', 80, 85, 80, 82, 'Baik', 'Genap', 2025),
('NP003', 10243301, 'IMP003', 91, 90, 90, 90, 'Mantul', 'Genap', 2025),
('NP004', 10243302, 'IMP004', 75, 99, 99, 91, 'Mantap\r\n', 'Ganjil', 2025),
('NP005', 10243301, 'IMP002', 90, 90, 90, 90, 'Mantap Betul', 'Genap', 2025),
('NP006', 10243301, 'IMP001', 90, 90, 90, 90, 'Bagus Sekali', 'Ganjil', 2025);

-- --------------------------------------------------------

--
-- Table structure for table `siswa_alif`
--

CREATE TABLE `siswa_alif` (
  `nis` int(11) NOT NULL,
  `Nama` varchar(25) NOT NULL,
  `tempat_lahir` varchar(15) NOT NULL,
  `tgl_lahir` date NOT NULL,
  `Alamat` varchar(50) NOT NULL,
  `id_kelas` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `siswa_alif`
--

INSERT INTO `siswa_alif` (`nis`, `Nama`, `tempat_lahir`, `tgl_lahir`, `Alamat`, `id_kelas`) VALUES
(1024329, 'Rizki', 'Cimahi', '2008-04-11', 'Paku Haji', 'IK004'),
(10243300, 'Akbar', 'Cimahi', '2008-05-11', 'Padasuka', 'IK002'),
(10243301, 'Alif', 'Cimahi', '2008-07-17', 'Jl. Kebon Kopi', 'IK001'),
(10243302, 'Azam', 'Cimahi', '2008-04-25', 'Citeureup', 'IK003');

-- --------------------------------------------------------

--
-- Table structure for table `user_alif`
--

CREATE TABLE `user_alif` (
  `id` varchar(10) NOT NULL,
  `Username` varchar(25) NOT NULL,
  `Password` varchar(25) NOT NULL,
  `Role` enum('admin','guru','walikelas','') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `user_alif`
--

INSERT INTO `user_alif` (`id`, `Username`, `Password`, `Role`) VALUES
('ID001', 'wali123', 'wali123', 'walikelas'),
('ID002', 'admin123', 'admin123', 'admin'),
('ID003', 'guru123', 'guru123', 'guru'),
('ID004', 'wali1234', 'wali1234', 'walikelas');

-- --------------------------------------------------------

--
-- Table structure for table `walikelas_alif`
--

CREATE TABLE `walikelas_alif` (
  `id_walikelas` varchar(10) NOT NULL,
  `nip` varchar(18) NOT NULL,
  `nama_walikelas` varchar(25) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `walikelas_alif`
--

INSERT INTO `walikelas_alif` (`id_walikelas`, `nip`, `nama_walikelas`) VALUES
('IW001', '123456', 'Bu Kiki'),
('IW002', '1234567', 'Bu Gigin'),
('IW003', '12345678', 'Pak Gani'),
('IW004', '123456789', 'Pak Irfan');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `absensi_alif`
--
ALTER TABLE `absensi_alif`
  ADD PRIMARY KEY (`id_absen`),
  ADD KEY `nis` (`nis`);

--
-- Indexes for table `kelas_alif`
--
ALTER TABLE `kelas_alif`
  ADD PRIMARY KEY (`id_kelas`),
  ADD KEY `id_guru` (`id_walikelas`);

--
-- Indexes for table `mapel_alif`
--
ALTER TABLE `mapel_alif`
  ADD PRIMARY KEY (`id_mapel`);

--
-- Indexes for table `nilai_alif`
--
ALTER TABLE `nilai_alif`
  ADD PRIMARY KEY (`id_nilai`),
  ADD KEY `nis` (`nis`,`id_mapel`),
  ADD KEY `id_mapel` (`id_mapel`);

--
-- Indexes for table `siswa_alif`
--
ALTER TABLE `siswa_alif`
  ADD PRIMARY KEY (`nis`),
  ADD KEY `id_kelas` (`id_kelas`);

--
-- Indexes for table `user_alif`
--
ALTER TABLE `user_alif`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `walikelas_alif`
--
ALTER TABLE `walikelas_alif`
  ADD PRIMARY KEY (`id_walikelas`),
  ADD UNIQUE KEY `nip` (`nip`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `absensi_alif`
--
ALTER TABLE `absensi_alif`
  ADD CONSTRAINT `absensi_alif_ibfk_1` FOREIGN KEY (`nis`) REFERENCES `siswa_alif` (`nis`);

--
-- Constraints for table `kelas_alif`
--
ALTER TABLE `kelas_alif`
  ADD CONSTRAINT `kelas_alif_ibfk_1` FOREIGN KEY (`id_walikelas`) REFERENCES `walikelas_alif` (`id_walikelas`);

--
-- Constraints for table `siswa_alif`
--
ALTER TABLE `siswa_alif`
  ADD CONSTRAINT `siswa_alif_ibfk_1` FOREIGN KEY (`id_kelas`) REFERENCES `kelas_alif` (`id_kelas`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
