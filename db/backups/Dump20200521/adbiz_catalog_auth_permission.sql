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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=105 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add entity locations',7,'add_entitylocations'),(26,'Can change entity locations',7,'change_entitylocations'),(27,'Can delete entity locations',7,'delete_entitylocations'),(28,'Can view entity locations',7,'view_entitylocations'),(29,'Can add entity contacts',8,'add_entitycontacts'),(30,'Can change entity contacts',8,'change_entitycontacts'),(31,'Can delete entity contacts',8,'delete_entitycontacts'),(32,'Can view entity contacts',8,'view_entitycontacts'),(33,'Can add entities',9,'add_entities'),(34,'Can change entities',9,'change_entities'),(35,'Can delete entities',9,'delete_entities'),(36,'Can view entities',9,'view_entities'),(37,'Can add data targets',10,'add_datatargets'),(38,'Can change data targets',10,'change_datatargets'),(39,'Can delete data targets',10,'delete_datatargets'),(40,'Can view data targets',10,'view_datatargets'),(41,'Can add data models',11,'add_datamodels'),(42,'Can change data models',11,'change_datamodels'),(43,'Can delete data models',11,'delete_datamodels'),(44,'Can view data models',11,'view_datamodels'),(45,'Can add catalogs',12,'add_catalogs'),(46,'Can change catalogs',12,'change_catalogs'),(47,'Can delete catalogs',12,'delete_catalogs'),(48,'Can view catalogs',12,'view_catalogs'),(49,'Can add datasets',13,'add_datasets'),(50,'Can change datasets',13,'change_datasets'),(51,'Can delete datasets',13,'delete_datasets'),(52,'Can view datasets',13,'view_datasets'),(53,'Can add data sources',14,'add_datasources'),(54,'Can change data sources',14,'change_datasources'),(55,'Can delete data sources',14,'delete_datasources'),(56,'Can view data sources',14,'view_datasources'),(57,'Can add containers',15,'add_containers'),(58,'Can change containers',15,'change_containers'),(59,'Can delete containers',15,'delete_containers'),(60,'Can view containers',15,'view_containers'),(61,'Can add objects',16,'add_objects'),(62,'Can change objects',16,'change_objects'),(63,'Can delete objects',16,'delete_objects'),(64,'Can view objects',16,'view_objects'),(65,'Can add kpi components',17,'add_kpicomponents'),(66,'Can change kpi components',17,'change_kpicomponents'),(67,'Can delete kpi components',17,'delete_kpicomponents'),(68,'Can view kpi components',17,'view_kpicomponents'),(69,'Can add attributes',18,'add_attributes'),(70,'Can change attributes',18,'change_attributes'),(71,'Can delete attributes',18,'delete_attributes'),(72,'Can view attributes',18,'view_attributes'),(73,'Can add measures',19,'add_measures'),(74,'Can change measures',19,'change_measures'),(75,'Can delete measures',19,'delete_measures'),(76,'Can view measures',19,'view_measures'),(77,'Can add aggregate measures',20,'add_aggregatemeasures'),(78,'Can change aggregate measures',20,'change_aggregatemeasures'),(79,'Can delete aggregate measures',20,'delete_aggregatemeasures'),(80,'Can view aggregate measures',20,'view_aggregatemeasures'),(81,'Can add dimensions',21,'add_dimensions'),(82,'Can change dimensions',21,'change_dimensions'),(83,'Can delete dimensions',21,'delete_dimensions'),(84,'Can view dimensions',21,'view_dimensions'),(85,'Can add aggregates',22,'add_aggregates'),(86,'Can change aggregates',22,'change_aggregates'),(87,'Can delete aggregates',22,'delete_aggregates'),(88,'Can view aggregates',22,'view_aggregates'),(89,'Can add aggregate dimensions',23,'add_aggregatedimensions'),(90,'Can change aggregate dimensions',23,'change_aggregatedimensions'),(91,'Can delete aggregate dimensions',23,'delete_aggregatedimensions'),(92,'Can view aggregate dimensions',23,'view_aggregatedimensions'),(93,'Can add kp is',24,'add_kpis'),(94,'Can change kp is',24,'change_kpis'),(95,'Can delete kp is',24,'delete_kpis'),(96,'Can view kp is',24,'view_kpis'),(97,'Can add org hierarchy types',25,'add_orghierarchytypes'),(98,'Can change org hierarchy types',25,'change_orghierarchytypes'),(99,'Can delete org hierarchy types',25,'delete_orghierarchytypes'),(100,'Can view org hierarchy types',25,'view_orghierarchytypes'),(101,'Can add org hierarchy',26,'add_orghierarchy'),(102,'Can change org hierarchy',26,'change_orghierarchy'),(103,'Can delete org hierarchy',26,'delete_orghierarchy'),(104,'Can view org hierarchy',26,'view_orghierarchy');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-21  0:11:24
