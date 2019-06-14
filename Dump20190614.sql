-- MySQL dump 10.16  Distrib 10.1.40-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: coolbag
-- ------------------------------------------------------
-- Server version	10.1.40-MariaDB-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `tb_armario`
--

DROP TABLE IF EXISTS `tb_armario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_armario` (
  `id_armario` int(30) NOT NULL AUTO_INCREMENT,
  `classe` tinytext NOT NULL,
  `local` varchar(50) NOT NULL,
  `terminal` tinytext NOT NULL,
  `estado` tinytext,
  `coluna` text,
  `nivel` text,
  PRIMARY KEY (`id_armario`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_armario`
--

LOCK TABLES `tb_armario` WRITE;
/*!40000 ALTER TABLE `tb_armario` DISABLE KEYS */;
INSERT INTO `tb_armario` VALUES (1,'A','superior','1','LIVRE',NULL,NULL),(2,'A','superior','2','LIVRE',NULL,NULL);
/*!40000 ALTER TABLE `tb_armario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_locacao`
--

DROP TABLE IF EXISTS `tb_locacao`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_locacao` (
  `id_locacao` int(10) NOT NULL AUTO_INCREMENT,
  `data_locacao` datetime NOT NULL,
  `tempo_locado` datetime NOT NULL,
  `tempo_corrido` datetime DEFAULT NULL,
  `senha` text,
  `id_armario` int(10) DEFAULT '0',
  `id_usuario` int(10) DEFAULT '0',
  KEY `id_locacao` (`id_locacao`),
  KEY `FK__tb_armario` (`id_armario`),
  KEY `FK__tb_usuario` (`id_usuario`),
  CONSTRAINT `FK__tb_armario` FOREIGN KEY (`id_armario`) REFERENCES `tb_armario` (`id_armario`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FK__tb_usuario` FOREIGN KEY (`id_usuario`) REFERENCES `tb_usuario` (`id_usuario`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_locacao`
--

LOCK TABLES `tb_locacao` WRITE;
/*!40000 ALTER TABLE `tb_locacao` DISABLE KEYS */;
INSERT INTO `tb_locacao` VALUES (1,'2019-06-06 23:59:18','0000-00-00 00:00:00',NULL,'27yn',1,2),(3,'2019-06-10 16:44:37','2019-06-16 04:44:00',NULL,'om43',1,3);
/*!40000 ALTER TABLE `tb_locacao` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tb_usuario`
--

DROP TABLE IF EXISTS `tb_usuario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `tb_usuario` (
  `id_usuario` int(10) NOT NULL AUTO_INCREMENT,
  `nome` varchar(50) DEFAULT NULL,
  `email` varchar(80) NOT NULL,
  `telefone` text NOT NULL,
  PRIMARY KEY (`id_usuario`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tb_usuario`
--

LOCK TABLES `tb_usuario` WRITE;
/*!40000 ALTER TABLE `tb_usuario` DISABLE KEYS */;
INSERT INTO `tb_usuario` VALUES (1,'marcosviana','marcosviana@gmail.com','987546798'),(2,'marcos aurelio','maurelio@gmail.com','85967895667'),(3,'samara livia','samara@gmail.com','87522737');
/*!40000 ALTER TABLE `tb_usuario` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-06-14 12:09:40
