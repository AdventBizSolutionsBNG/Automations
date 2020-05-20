CREATE DATABASE  IF NOT EXISTS `adbiz_core` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `adbiz_core`;
-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: adbiz_core
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
-- Table structure for table `engine_metadata`
--

DROP TABLE IF EXISTS `engine_metadata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_metadata` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `core_engine_code` varchar(64) NOT NULL,
  `product_engine_code` varchar(64) NOT NULL,
  `activation_file_location` varchar(128) NOT NULL,
  `activation_key` varchar(255) NOT NULL,
  `activation_dt` datetime(6) NOT NULL,
  `host_name` varchar(128) NOT NULL,
  `host_ip_address` char(39) NOT NULL,
  `os_release` varchar(32) DEFAULT NULL,
  `release_info` varchar(255) DEFAULT NULL,
  `validity_start_date` datetime(6) DEFAULT NULL,
  `validity_end_date` datetime(6) DEFAULT NULL,
  `is_activated` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `last_updated_on` datetime(6) NOT NULL,
  `last_updated_by` varchar(64) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `core_engine_code` (`core_engine_code`),
  KEY `engine_metadata_customer_id_9e68e8c1_fk_customers_id` (`customer_id`),
  CONSTRAINT `engine_metadata_customer_id_9e68e8c1_fk_customers_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `engine_metadata`
--

LOCK TABLES `engine_metadata` WRITE;
/*!40000 ALTER TABLE `engine_metadata` DISABLE KEYS */;
INSERT INTO `engine_metadata` VALUES (1,'0777da1b-b6b9-480e-a7ef-0939467a25cb@dtl','61b9a376-96d9-11ea-bb37-0242ac130002@adbiz','/home/setupadmin/core_engine_activation.key','892d7083-f0d3-4dde-8c93-ea2466e0f0ad','2020-05-01 00:00:00.000000','home','127.0.0,1','','','2020-05-01 00:00:00.000000','2020-04-30 00:00:00.000000',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','product_admin',1);
/*!40000 ALTER TABLE `engine_metadata` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-21  0:11:21
