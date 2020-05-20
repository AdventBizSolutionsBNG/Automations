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
-- Table structure for table `org_hierarchies`
--

DROP TABLE IF EXISTS `org_hierarchies`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `org_hierarchies` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_code` varchar(64) NOT NULL,
  `site_code` varchar(64) NOT NULL,
  `hierarchy_name` varchar(32) NOT NULL,
  `hierarchy_description` varchar(255) DEFAULT NULL,
  `level` smallint(5) unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `last_updated_on` datetime(6) NOT NULL,
  `last_updated_by` varchar(64) NOT NULL,
  `hierarchy_type_id` int(11) NOT NULL,
  `parent_hierarchy_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `org_hierarchies_hierarchy_type_id_1d4eb59a_fk_org_hiera` (`hierarchy_type_id`),
  KEY `org_hierarchies_parent_hierarchy_id_9bb3dd8c_fk_org_hiera` (`parent_hierarchy_id`),
  CONSTRAINT `org_hierarchies_hierarchy_type_id_1d4eb59a_fk_org_hiera` FOREIGN KEY (`hierarchy_type_id`) REFERENCES `org_hierarchy_types` (`id`),
  CONSTRAINT `org_hierarchies_parent_hierarchy_id_9bb3dd8c_fk_org_hiera` FOREIGN KEY (`parent_hierarchy_id`) REFERENCES `org_hierarchies` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `org_hierarchies`
--

LOCK TABLES `org_hierarchies` WRITE;
/*!40000 ALTER TABLE `org_hierarchies` DISABLE KEYS */;
INSERT INTO `org_hierarchies` VALUES (1,'328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','Legal Entity','',1,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,NULL),(2,'328984960484@dtl','02b65237-dcf8-4e48-9fec-b6db90afdfd4@dtl.site','Division','',2,1,'2020-05-01 00:00:00.000000','2020-05-01 00:00:00.000000','site_admin',1,1);
/*!40000 ALTER TABLE `org_hierarchies` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-21  0:11:25
