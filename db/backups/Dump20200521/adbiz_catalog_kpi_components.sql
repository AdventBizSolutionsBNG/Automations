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
-- Table structure for table `kpi_components`
--

DROP TABLE IF EXISTS `kpi_components`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `kpi_components` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `component_code` varchar(64) NOT NULL,
  `component_class` varchar(255) DEFAULT NULL,
  `component_type` varchar(255) NOT NULL,
  `component_display_type` varchar(255) NOT NULL,
  `display_properties` longtext NOT NULL,
  `data_filter` longtext NOT NULL,
  `date_filter` longtext NOT NULL,
  `sort_by` longtext,
  `indicators` longtext,
  `indicator_class` varchar(255) DEFAULT NULL,
  `component_name` varchar(255) NOT NULL,
  `component_description` longtext,
  `sequence` smallint(5) unsigned NOT NULL,
  `is_incremental` tinyint(1) NOT NULL,
  `is_rebuild` tinyint(1) NOT NULL,
  `refresh_interval` smallint(5) unsigned NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_on` datetime(6) NOT NULL,
  `last_updated_on` datetime(6) NOT NULL,
  `last_updated_by` varchar(64) NOT NULL,
  `aggregate_id` int(11) NOT NULL,
  `container_id` int(11) NOT NULL,
  `kpi_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `kpi_components_aggregate_id_f7825f88_fk_aggregates_id` (`aggregate_id`),
  KEY `kpi_components_container_id_0821b0c9_fk_containers_id` (`container_id`),
  KEY `kpi_components_kpi_id_815fc3d8_fk_kpis_id` (`kpi_id`),
  CONSTRAINT `kpi_components_aggregate_id_f7825f88_fk_aggregates_id` FOREIGN KEY (`aggregate_id`) REFERENCES `aggregates` (`id`),
  CONSTRAINT `kpi_components_container_id_0821b0c9_fk_containers_id` FOREIGN KEY (`container_id`) REFERENCES `containers` (`id`),
  CONSTRAINT `kpi_components_kpi_id_815fc3d8_fk_kpis_id` FOREIGN KEY (`kpi_id`) REFERENCES `kpis` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kpi_components`
--

LOCK TABLES `kpi_components` WRITE;
/*!40000 ALTER TABLE `kpi_components` DISABLE KEYS */;
/*!40000 ALTER TABLE `kpi_components` ENABLE KEYS */;
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
