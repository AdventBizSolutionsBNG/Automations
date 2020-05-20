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
-- Table structure for table `objects`
--

DROP TABLE IF EXISTS `objects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `objects` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `object_code` varchar(128) NOT NULL,
  `customer_code` varchar(64) NOT NULL,
  `site_code` varchar(64) NOT NULL,
  `module` varchar(32) NOT NULL,
  `object_name` varchar(64) NOT NULL,
  `object_reference_class` varchar(128) NOT NULL,
  `object_description` varchar(255) NOT NULL,
  `object_class` varchar(32) NOT NULL,
  `is_validate_data` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `last_updated_on` datetime(6) NOT NULL,
  `last_updated_by` varchar(64) NOT NULL,
  `catalog_id` int(11) NOT NULL,
  `datamodel_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `object_code` (`object_code`),
  KEY `objects_catalog_id_57cfed53_fk_catalogs_id` (`catalog_id`),
  KEY `objects_datamodel_id_db778bac_fk_datamodels_id` (`datamodel_id`),
  CONSTRAINT `objects_catalog_id_57cfed53_fk_catalogs_id` FOREIGN KEY (`catalog_id`) REFERENCES `catalogs` (`id`),
  CONSTRAINT `objects_datamodel_id_db778bac_fk_datamodels_id` FOREIGN KEY (`datamodel_id`) REFERENCES `datamodels` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `objects`
--

LOCK TABLES `objects` WRITE;
/*!40000 ALTER TABLE `objects` DISABLE KEYS */;
INSERT INTO `objects` VALUES (1,'48d63ab2-c38f-41b2-af03-f849da4fae71@dtl.site.catalog.datamodel.object','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','ACTRBL','INVOICE','adbiz.actrbl.object.invoice','Invoice/Sales Data for a Division','E',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1),(2,'e8dc116f-c943-4c00-a177-b7d96393653e@dtl.site.catalog.datamodel.object','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','ACTRBL','PAYMENT ADVICE','adbiz.actrbl.object.payment_advice','Payment Advices data or a Division','E',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1),(3,'3132ed34-3f68-47c9-bed0-f9d624cddf06@dtl.site.catalog.datamodel.object','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','ACTRBL','CUSTOMER MASTER','adbiz.actrbl.object.customer_master','Customer Master Data for a Division','P',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1),(4,'d7a453f2-6605-4852-b612-5e5251c25ada@dtl.site.catalog.datamodel.object','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','ACTRBL','PRODUCT MASTER','adbiz.actrbl.object.product_master','Product Master Data for a Division','M',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1),(5,'283815e6-67f0-4ca2-ba94-67aecfad9ae6@dtl.site.catalog.datamodel.object','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','ACTRBL','SALES FORECAST','adbiz.actrbl.object.sales_forecast','Sales Forecast Data for a Division','E',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1);
/*!40000 ALTER TABLE `objects` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-21  0:11:27
