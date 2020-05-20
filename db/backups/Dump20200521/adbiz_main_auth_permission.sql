CREATE DATABASE  IF NOT EXISTS `adbiz_main` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `adbiz_main`;
-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: adbiz_main
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
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add users',6,'add_users'),(22,'Can change users',6,'change_users'),(23,'Can delete users',6,'delete_users'),(24,'Can view users',6,'view_users'),(25,'Can add adbiz engine metadata',7,'add_adbizenginemetadata'),(26,'Can change adbiz engine metadata',7,'change_adbizenginemetadata'),(27,'Can delete adbiz engine metadata',7,'delete_adbizenginemetadata'),(28,'Can view adbiz engine metadata',7,'view_adbizenginemetadata'),(29,'Can add adbiz preferences',8,'add_adbizpreferences'),(30,'Can change adbiz preferences',8,'change_adbizpreferences'),(31,'Can delete adbiz preferences',8,'delete_adbizpreferences'),(32,'Can view adbiz preferences',8,'view_adbizpreferences'),(33,'Can add adbiz privileges',9,'add_adbizprivileges'),(34,'Can change adbiz privileges',9,'change_adbizprivileges'),(35,'Can delete adbiz privileges',9,'delete_adbizprivileges'),(36,'Can view adbiz privileges',9,'view_adbizprivileges'),(37,'Can add adbiz roles',10,'add_adbizroles'),(38,'Can change adbiz roles',10,'change_adbizroles'),(39,'Can delete adbiz roles',10,'delete_adbizroles'),(40,'Can view adbiz roles',10,'view_adbizroles'),(41,'Can add user preferences',11,'add_userpreferences'),(42,'Can change user preferences',11,'change_userpreferences'),(43,'Can delete user preferences',11,'delete_userpreferences'),(44,'Can view user preferences',11,'view_userpreferences'),(45,'Can add user access',12,'add_useraccess'),(46,'Can change user access',12,'change_useraccess'),(47,'Can delete user access',12,'delete_useraccess'),(48,'Can view user access',12,'view_useraccess'),(49,'Can add adbiz module activations',13,'add_adbizmoduleactivations'),(50,'Can change adbiz module activations',13,'change_adbizmoduleactivations'),(51,'Can delete adbiz module activations',13,'delete_adbizmoduleactivations'),(52,'Can view adbiz module activations',13,'view_adbizmoduleactivations'),(53,'Can add adbiz menu items',14,'add_adbizmenuitems'),(54,'Can change adbiz menu items',14,'change_adbizmenuitems'),(55,'Can delete adbiz menu items',14,'delete_adbizmenuitems'),(56,'Can view adbiz menu items',14,'view_adbizmenuitems'),(57,'Can add adbiz engine activation details',15,'add_adbizengineactivationdetails'),(58,'Can change adbiz engine activation details',15,'change_adbizengineactivationdetails'),(59,'Can delete adbiz engine activation details',15,'delete_adbizengineactivationdetails'),(60,'Can view adbiz engine activation details',15,'view_adbizengineactivationdetails');
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

-- Dump completed on 2020-05-21  0:11:18
