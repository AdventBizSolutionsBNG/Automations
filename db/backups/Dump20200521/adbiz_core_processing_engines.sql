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
-- Table structure for table `processing_engines`
--

DROP TABLE IF EXISTS `processing_engines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `processing_engines` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `processing_engine_type` varchar(32) DEFAULT NULL,
  `processing_engine_code` varchar(64) NOT NULL,
  `activation_key` varchar(255) NOT NULL,
  `activation_dt` datetime(6) DEFAULT NULL,
  `validity_start_date` datetime(6) DEFAULT NULL,
  `validity_end_date` datetime(6) DEFAULT NULL,
  `is_activated` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `last_updated_on` datetime(6) NOT NULL,
  `last_updated_by` varchar(64) NOT NULL,
  `core_engine_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  `environment_id` int(11) NOT NULL,
  `site_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `processing_engine_code` (`processing_engine_code`),
  KEY `processing_engines_core_engine_id_e66d2d13_fk_engine_metadata_id` (`core_engine_id`),
  KEY `processing_engines_customer_id_673640b9_fk_customers_id` (`customer_id`),
  KEY `processing_engines_environment_id_c6a5ea42_fk_environments_id` (`environment_id`),
  KEY `processing_engines_site_id_e41ae58f_fk_sites_id` (`site_id`),
  CONSTRAINT `processing_engines_core_engine_id_e66d2d13_fk_engine_metadata_id` FOREIGN KEY (`core_engine_id`) REFERENCES `engine_metadata` (`id`),
  CONSTRAINT `processing_engines_customer_id_673640b9_fk_customers_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`),
  CONSTRAINT `processing_engines_environment_id_c6a5ea42_fk_environments_id` FOREIGN KEY (`environment_id`) REFERENCES `environments` (`id`),
  CONSTRAINT `processing_engines_site_id_e41ae58f_fk_sites_id` FOREIGN KEY (`site_id`) REFERENCES `sites` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `processing_engines`
--

LOCK TABLES `processing_engines` WRITE;
/*!40000 ALTER TABLE `processing_engines` DISABLE KEYS */;
INSERT INTO `processing_engines` VALUES (1,'EE','6e27b6f4-4bbf-4c19-bbd8-2ecc756caffa@dtl','339c6c26-4eed-4f01-9e76-97424194254e','2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','2021-04-30 00:00:00.000000',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','core_admin',1,1,1,1),(2,'KE','f8c2e7dc-4373-4e41-aab0-ce77ede7fc2f@dtl','2e5c781a-8094-451c-8f26-622e6350a0a1','2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','2021-04-30 00:00:00.000000',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','core_admin',1,1,1,1),(3,'QE','8c9ac3d5-bed3-4aa8-9839-a2425cf5539c@dtl','065719e6-e225-4e67-a734-9b9ab795833f','2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','2021-04-30 00:00:00.000000',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','core_admin',1,1,1,1),(4,'UI','5636f2a5-74dd-4c5a-b6dd-feddff325476@dtl','2d4dc699-b379-44e6-b472-4f2d8e8336b5','2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','2021-04-30 00:00:00.000000',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','core_admin',1,1,1,1);
/*!40000 ALTER TABLE `processing_engines` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-21  0:11:22
