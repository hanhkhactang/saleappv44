-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: localhost    Database: bookstoredb
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `book`
--

DROP TABLE IF EXISTS `book`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `soluong` int DEFAULT NULL,
  `image` varchar(100) DEFAULT NULL,
  `gia` float DEFAULT NULL,
  `descrip` varchar(255) DEFAULT NULL,
  `tacgia_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `tacgia_id` (`tacgia_id`),
  CONSTRAINT `book_ibfk_1` FOREIGN KEY (`tacgia_id`) REFERENCES `tacgia` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `category`
--

DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `category` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hoadon`
--

DROP TABLE IF EXISTS `hoadon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoadon` (
  `Book_id` int NOT NULL,
  `KhachHang_id` int NOT NULL,
  `SoLuongBan` int DEFAULT NULL,
  `DonGia` float DEFAULT NULL,
  `TongTien` float DEFAULT NULL,
  PRIMARY KEY (`Book_id`,`KhachHang_id`),
  KEY `KhachHang_id` (`KhachHang_id`),
  CONSTRAINT `hoadon_ibfk_1` FOREIGN KEY (`Book_id`) REFERENCES `book` (`id`),
  CONSTRAINT `hoadon_ibfk_2` FOREIGN KEY (`KhachHang_id`) REFERENCES `khachhang` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hoadonsach`
--

DROP TABLE IF EXISTS `hoadonsach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `hoadonsach` (
  `id` int NOT NULL AUTO_INCREMENT,
  `decreption` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `khachhang`
--

DROP TABLE IF EXISTS `khachhang`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `khachhang` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `DiaChi` varchar(255) DEFAULT NULL,
  `SDT` int DEFAULT NULL,
  `Email` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phieunhapsach`
--

DROP TABLE IF EXISTS `phieunhapsach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieunhapsach` (
  `Book_id` int NOT NULL,
  `HoadonSach_id` int NOT NULL,
  `SoLuongNhap` int DEFAULT NULL,
  `NgayNhap` datetime DEFAULT NULL,
  PRIMARY KEY (`Book_id`,`HoadonSach_id`),
  KEY `HoadonSach_id` (`HoadonSach_id`),
  CONSTRAINT `phieunhapsach_ibfk_1` FOREIGN KEY (`Book_id`) REFERENCES `book` (`id`),
  CONSTRAINT `phieunhapsach_ibfk_2` FOREIGN KEY (`HoadonSach_id`) REFERENCES `hoadonsach` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `phieuthu`
--

DROP TABLE IF EXISTS `phieuthu`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `phieuthu` (
  `PhieuThu_id` int NOT NULL AUTO_INCREMENT,
  `NgayLap` datetime DEFAULT NULL,
  `SoTienThu` float DEFAULT NULL,
  `KhachHang_id` int NOT NULL,
  PRIMARY KEY (`PhieuThu_id`),
  KEY `KhachHang_id` (`KhachHang_id`),
  CONSTRAINT `phieuthu_ibfk_1` FOREIGN KEY (`KhachHang_id`) REFERENCES `khachhang` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `tacgia`
--

DROP TABLE IF EXISTS `tacgia`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tacgia` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `theloaisach`
--

DROP TABLE IF EXISTS `theloaisach`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `theloaisach` (
  `Book_id` int NOT NULL,
  `Cat_id` int NOT NULL,
  PRIMARY KEY (`Book_id`,`Cat_id`),
  KEY `Cat_id` (`Cat_id`),
  CONSTRAINT `theloaisach_ibfk_1` FOREIGN KEY (`Book_id`) REFERENCES `book` (`id`),
  CONSTRAINT `theloaisach_ibfk_2` FOREIGN KEY (`Cat_id`) REFERENCES `category` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `username` varchar(50) NOT NULL,
  `password` varchar(100) NOT NULL,
  `active` tinyint(1) DEFAULT NULL,
  `user_role` enum('USER','ADMIN') DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`),
  CONSTRAINT `user_chk_1` CHECK ((`active` in (0,1)))
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-12-11 15:43:52
