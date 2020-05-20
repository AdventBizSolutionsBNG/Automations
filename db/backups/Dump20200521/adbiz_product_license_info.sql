CREATE DATABASE  IF NOT EXISTS `adbiz_product` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `adbiz_product`;
-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: adbiz_product
-- ------------------------------------------------------
-- Server version	5.7.30-0ubuntu0.18.04.1

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
-- Table structure for table `license_info`
--

DROP TABLE IF EXISTS `license_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `license_info` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `license_type` varchar(48) NOT NULL,
  `license_key` varchar(64) NOT NULL,
  `duration_days` int(10) unsigned NOT NULL,
  `active_modules` varchar(255) NOT NULL,
  `active_engines` varchar(255) NOT NULL,
  `active_envs` varchar(255) NOT NULL,
  `active_from_dt` datetime(6) NOT NULL,
  `active_end_dt` datetime(6) DEFAULT NULL,
  `activated_on_dt` datetime(6) DEFAULT NULL,
  `deactivated_on_dt` datetime(6) DEFAULT NULL,
  `is_activated` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `last_updated_on` datetime(6) NOT NULL,
  `last_updated_by` varchar(64) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `product_engine_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `license_key` (`license_key`),
  KEY `license_info_customer_id_5afc5922_fk_customers_id` (`customer_id`),
  KEY `license_info_product_engine_id_f6ed8a01_fk_engine_metadata_id` (`product_engine_id`),
  CONSTRAINT `license_info_customer_id_5afc5922_fk_customers_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),
  CONSTRAINT `license_info_product_engine_id_f6ed8a01_fk_engine_metadata_id` FOREIGN KEY (`product_engine_id`) REFERENCES `engine_metadata` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `license_info`
--

LOCK TABLES `license_info` WRITE;
/*!40000 ALTER TABLE `license_info` DISABLE KEYS */;
INSERT INTO `license_info` VALUES (1,'SUBCRPTN','d4ac5b47-23e1-4669-8699-0cb303d5e862',365,'ACTPBL, ACTRBL, RECO','CE, EE, KE, QE, UI','DEV, PROD','2020-05-01 00:00:00.000000','2021-04-30 00:00:00.000000','2020-05-01 00:00:00.000000',NULL,1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','product_admin',1,1);
/*!40000 ALTER TABLE `license_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-21  0:11:23
