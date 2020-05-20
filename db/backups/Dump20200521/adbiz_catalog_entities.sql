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
-- Table structure for table `entities`
--

DROP TABLE IF EXISTS `entities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `entities` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `entity_code` varchar(64) NOT NULL,
  `customer_code` varchar(64) NOT NULL,
  `site_code` varchar(64) NOT NULL,
  `entity_name` varchar(128) NOT NULL,
  `entity_type` varchar(32) NOT NULL,
  `entity_sub_type` varchar(32) DEFAULT NULL,
  `parent_entity` int(10) unsigned DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `last_updated_on` datetime(6) NOT NULL,
  `last_updated_by` varchar(64) NOT NULL,
  `hierarchy_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `entity_code` (`entity_code`),
  KEY `entities_hierarchy_id_c1113a2e_fk_org_hierarchies_id` (`hierarchy_id`),
  CONSTRAINT `entities_hierarchy_id_c1113a2e_fk_org_hierarchies_id` FOREIGN KEY (`hierarchy_id`) REFERENCES `org_hierarchies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `entities`
--

LOCK TABLES `entities` WRITE;
/*!40000 ALTER TABLE `entities` DISABLE KEYS */;
INSERT INTO `entities` VALUES (1,'419258870883@dtl.entity','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','Dynamatic Technologies Ltd','LE','HO',NULL,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1),(2,'706588775663@dtl.entity','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','Dynamatic Hydraulics India','BU','DIV',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',2),(3,'578562064060@dtl.entity','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','Dynamatic Hydraulics UK','BU','DIV',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',2),(4,'835488960834@dtl.entity','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','EISENWERK ERLA GmbH, Germany','BU','DIV',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',2),(5,'269341777847@dtl.entity','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','JKM FERROTECH LIMITED, India','BU','DIV',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',2),(6,'303363513906@dtl.entity','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','DYNAMETAL India','BU','DIV',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',2),(7,'904579665694@dtl.entity','328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','DYNAMATIC-OLDLAND AEROSPACE, India','BU','DIV',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',2);
/*!40000 ALTER TABLE `entities` ENABLE KEYS */;
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
