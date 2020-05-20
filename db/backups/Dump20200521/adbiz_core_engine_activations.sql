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
-- Table structure for table `engine_activations`
--

DROP TABLE IF EXISTS `engine_activations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `engine_activations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `product_engine_code` varchar(64) NOT NULL,
  `activation_file_location` varchar(128) NOT NULL,
  `activation_key` varchar(64) NOT NULL,
  `validity_start_date` datetime(6) DEFAULT NULL,
  `validity_end_date` datetime(6) DEFAULT NULL,
  `activation_dt` datetime(6) NOT NULL,
  `deactivation_dt` datetime(6) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `last_updated_on` datetime(6) NOT NULL,
  `last_updated_by` varchar(64) NOT NULL,
  `core_engine_id` int(11) NOT NULL,
  `customer_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `engine_activations_core_engine_id_6d8b4df0_fk_engine_metadata_id` (`core_engine_id`),
  KEY `engine_activations_customer_id_e0585224_fk_customers_id` (`customer_id`),
  CONSTRAINT `engine_activations_core_engine_id_6d8b4df0_fk_engine_metadata_id` FOREIGN KEY (`core_engine_id`) REFERENCES `engine_metadata` (`id`),
  CONSTRAINT `engine_activations_customer_id_e0585224_fk_customers_id` FOREIGN KEY (`customer_id`) REFERENCES `customers` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `engine_activations`
--

LOCK TABLES `engine_activations` WRITE;
/*!40000 ALTER TABLE `engine_activations` DISABLE KEYS */;
/*!40000 ALTER TABLE `engine_activations` ENABLE KEYS */;
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
