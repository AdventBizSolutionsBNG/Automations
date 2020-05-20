CREATE DATABASE  IF NOT EXISTS `adbiz_catalog` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `adbiz_catalog`;
-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: adbiz_catalog
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
-- Table structure for table `dimensions`
--

DROP TABLE IF EXISTS `dimensions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dimensions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_code` varchar(64) NOT NULL,
  `site_code` varchar(64) NOT NULL,
  `module` varchar(32) NOT NULL,
  `dimension_code` varchar(6) NOT NULL,
  `dimension_description` varchar(255) DEFAULT NULL,
  `dimension_type` varchar(32) NOT NULL,
  `is_hierarchy` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `last_updated_on` datetime(6) NOT NULL,
  `last_updated_by` varchar(64) NOT NULL,
  `attribute_id` int(11) NOT NULL,
  `catalog_id` int(11) NOT NULL,
  `datamodel_id` int(11) NOT NULL,
  `object_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `dimensions_attribute_id_cc59cb45_fk_attributes_id` (`attribute_id`),
  KEY `dimensions_catalog_id_483fc671_fk_catalogs_id` (`catalog_id`),
  KEY `dimensions_datamodel_id_018fbc23_fk_datamodels_id` (`datamodel_id`),
  KEY `dimensions_object_id_205d0834_fk_objects_id` (`object_id`),
  CONSTRAINT `dimensions_attribute_id_cc59cb45_fk_attributes_id` FOREIGN KEY (`attribute_id`) REFERENCES `attributes` (`id`),
  CONSTRAINT `dimensions_catalog_id_483fc671_fk_catalogs_id` FOREIGN KEY (`catalog_id`) REFERENCES `catalogs` (`id`),
  CONSTRAINT `dimensions_datamodel_id_018fbc23_fk_datamodels_id` FOREIGN KEY (`datamodel_id`) REFERENCES `datamodels` (`id`),
  CONSTRAINT `dimensions_object_id_205d0834_fk_objects_id` FOREIGN KEY (`object_id`) REFERENCES `objects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dimensions`
--

LOCK TABLES `dimensions` WRITE;
/*!40000 ALTER TABLE `dimensions` DISABLE KEYS */;
/*!40000 ALTER TABLE `dimensions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-21  0:11:26
