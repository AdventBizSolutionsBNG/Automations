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
-- Table structure for table `datasets`
--

DROP TABLE IF EXISTS `datasets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `datasets` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `dataset_code` varchar(128) NOT NULL,
  `customer_code` varchar(64) NOT NULL,
  `site_code` varchar(64) NOT NULL,
  `module` varchar(32) NOT NULL,
  `dataset_name` varchar(128) NOT NULL,
  `dataset_description` varchar(255) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `last_updated_on` datetime(6) NOT NULL,
  `last_updated_by` varchar(64) NOT NULL,
  `catalog_id` int(11) NOT NULL,
  `datamodel_id` int(11) NOT NULL,
  `object_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `dataset_code` (`dataset_code`),
  KEY `datasets_object_id_c10d5768_fk_objects_id` (`object_id`),
  KEY `datasets_catalog_id_a09e5159_fk_catalogs_id` (`catalog_id`),
  KEY `datasets_datamodel_id_eb3400a9_fk_datamodels_id` (`datamodel_id`),
  CONSTRAINT `datasets_catalog_id_a09e5159_fk_catalogs_id` FOREIGN KEY (`catalog_id`) REFERENCES `catalogs` (`id`),
  CONSTRAINT `datasets_datamodel_id_eb3400a9_fk_datamodels_id` FOREIGN KEY (`datamodel_id`) REFERENCES `datamodels` (`id`),
  CONSTRAINT `datasets_object_id_c10d5768_fk_objects_id` FOREIGN KEY (`object_id`) REFERENCES `objects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `datasets`
--

LOCK TABLES `datasets` WRITE;
/*!40000 ALTER TABLE `datasets` DISABLE KEYS */;
INSERT INTO `datasets` VALUES (1,'d4ed6dde-d8cb-49bc-84e5-5c441049ede5@dtl.site.catalog.datamodel.dataset','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','ACTRBL','Import Sales Data for a Division','',1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1,1),(2,'e67f660a-369d-477d-b498-8c6d4ba99b6a@dtl.site.catalog.datamodel.dataset','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','ACTRBL','Import Payment Advice Data for a Division','',1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1,2),(3,'1fb33dc9-a183-422d-84e4-53bbb34a4462@dtl.site.catalog.datamodel.dataset','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','ACTRBL','Customer Master Data for a Division','',1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1,3),(4,'cbe8b2a1-c80a-4d61-96eb-e5546b95cf2d@dtl.site.catalog.datamodel.dataset','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','ACTRBL','Product Master Data for a Division','',1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1,4),(5,'67f03a3b-4014-4452-98dd-79c186b80d75@dtl.site.catalog.datamodel.dataset','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','ACTRBL','Sales Forecast Data for a Division','',1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1,5);
/*!40000 ALTER TABLE `datasets` ENABLE KEYS */;
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
