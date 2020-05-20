CREATE DATABASE  IF NOT EXISTS `adbiz_product` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `adbiz_product`;
-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: adbiz_product
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
) ENGINE=InnoDB AUTO_INCREMENT=65 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add contact us',7,'add_contactus'),(26,'Can change contact us',7,'change_contactus'),(27,'Can delete contact us',7,'delete_contactus'),(28,'Can view contact us',7,'view_contactus'),(29,'Can add customers',8,'add_customers'),(30,'Can change customers',8,'change_customers'),(31,'Can delete customers',8,'delete_customers'),(32,'Can view customers',8,'view_customers'),(33,'Can add product engine',9,'add_productengine'),(34,'Can change product engine',9,'change_productengine'),(35,'Can delete product engine',9,'delete_productengine'),(36,'Can view product engine',9,'view_productengine'),(37,'Can add licensing info',10,'add_licensinginfo'),(38,'Can change licensing info',10,'change_licensinginfo'),(39,'Can delete licensing info',10,'delete_licensinginfo'),(40,'Can view licensing info',10,'view_licensinginfo'),(41,'Can add license site activations',11,'add_licensesiteactivations'),(42,'Can change license site activations',11,'change_licensesiteactivations'),(43,'Can delete license site activations',11,'delete_licensesiteactivations'),(44,'Can view license site activations',11,'view_licensesiteactivations'),(45,'Can add license module activations',12,'add_licensemoduleactivations'),(46,'Can change license module activations',12,'change_licensemoduleactivations'),(47,'Can delete license module activations',12,'delete_licensemoduleactivations'),(48,'Can view license module activations',12,'view_licensemoduleactivations'),(49,'Can add license env activations',13,'add_licenseenvactivations'),(50,'Can change license env activations',13,'change_licenseenvactivations'),(51,'Can delete license env activations',13,'delete_licenseenvactivations'),(52,'Can view license env activations',13,'view_licenseenvactivations'),(53,'Can add license engine activations',14,'add_licenseengineactivations'),(54,'Can change license engine activations',14,'change_licenseengineactivations'),(55,'Can delete license engine activations',14,'delete_licenseengineactivations'),(56,'Can view license engine activations',14,'view_licenseengineactivations'),(57,'Can add customer locations',15,'add_customerlocations'),(58,'Can change customer locations',15,'change_customerlocations'),(59,'Can delete customer locations',15,'delete_customerlocations'),(60,'Can view customer locations',15,'view_customerlocations'),(61,'Can add customer contact details',16,'add_customercontactdetails'),(62,'Can change customer contact details',16,'change_customercontactdetails'),(63,'Can delete customer contact details',16,'delete_customercontactdetails'),(64,'Can view customer contact details',16,'view_customercontactdetails');
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

-- Dump completed on 2020-05-21  0:11:22
