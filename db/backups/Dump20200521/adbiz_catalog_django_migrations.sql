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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2020-05-15 15:06:02.134275'),(2,'auth','0001_initial','2020-05-15 15:06:04.344749'),(3,'admin','0001_initial','2020-05-15 15:06:12.765922'),(4,'admin','0002_logentry_remove_auto_add','2020-05-15 15:06:14.693309'),(5,'admin','0003_logentry_add_action_flag_choices','2020-05-15 15:06:14.752324'),(6,'contenttypes','0002_remove_content_type_name','2020-05-15 15:06:16.534458'),(7,'auth','0002_alter_permission_name_max_length','2020-05-15 15:06:16.701644'),(8,'auth','0003_alter_user_email_max_length','2020-05-15 15:06:16.916378'),(9,'auth','0004_alter_user_username_opts','2020-05-15 15:06:17.014249'),(10,'auth','0005_alter_user_last_login_null','2020-05-15 15:06:17.781111'),(11,'auth','0006_require_contenttypes_0002','2020-05-15 15:06:17.837470'),(12,'auth','0007_alter_validators_add_error_messages','2020-05-15 15:06:17.906847'),(13,'auth','0008_alter_user_username_max_length','2020-05-15 15:06:18.081106'),(14,'auth','0009_alter_user_last_name_max_length','2020-05-15 15:06:18.237050'),(15,'auth','0010_alter_group_name_max_length','2020-05-15 15:06:18.382803'),(16,'auth','0011_update_proxy_permissions','2020-05-15 15:06:18.447054'),(17,'sessions','0001_initial','2020-05-15 15:06:18.794003'),(18,'adbizCatalogService','0001_initial','2020-05-15 18:05:31.007511'),(19,'adbizCatalogService','0002_auto_20200518_1544','2020-05-18 15:45:28.002339'),(20,'adbizCatalogService','0003_entities_hierarchy','2020-05-18 18:08:47.727838'),(21,'adbizCatalogService','0004_remove_catalogs_module','2020-05-18 18:15:26.321874');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
