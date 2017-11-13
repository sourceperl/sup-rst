-- MySQL dump 10.13  Distrib 5.5.43, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: sup_rst
-- ------------------------------------------------------
-- Server version	5.5.43-0+deb7u1

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
-- Table structure for table `alarms`
--

DROP TABLE IF EXISTS `alarms`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `alarms` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_host` int(10) unsigned NOT NULL DEFAULT '0',
  `daemon` varchar(6) NOT NULL DEFAULT '',
  `date_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ack` char(1) NOT NULL DEFAULT 'N',
  `message` varchar(80) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`),
  KEY `date_time` (`date_time`)
) ENGINE=MyISAM AUTO_INCREMENT=2917627 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `hosts`
--

DROP TABLE IF EXISTS `hosts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `hosts` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_subnet` int(10) unsigned NOT NULL DEFAULT '0',
  `name` varchar(30) NOT NULL DEFAULT '',
  `hostname` varchar(30) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=410 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `icmp`
--

DROP TABLE IF EXISTS `icmp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `icmp` (
  `id_host` int(10) unsigned NOT NULL DEFAULT '0',
  `icmp_inhibition` tinyint(1) NOT NULL DEFAULT '0',
  `icmp_timeout` smallint(6) unsigned NOT NULL DEFAULT '4',
  `icmp_good_threshold` int(10) unsigned NOT NULL DEFAULT '2',
  `icmp_good_count` int(10) unsigned NOT NULL DEFAULT '0',
  `icmp_fail_threshold` int(11) unsigned NOT NULL DEFAULT '4',
  `icmp_fail_count` int(11) unsigned NOT NULL DEFAULT '0',
  `icmp_log_rtt` char(1) NOT NULL DEFAULT 'N',
  `icmp_state` char(1) NOT NULL DEFAULT 'D',
  `icmp_chg_state` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `icmp_rtt` int(10) unsigned NOT NULL DEFAULT '0',
  `icmp_up_index` int(10) unsigned NOT NULL DEFAULT '0',
  `icmp_down_index` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id_host`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `icmp_history`
--

DROP TABLE IF EXISTS `icmp_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `icmp_history` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_host` int(10) unsigned NOT NULL DEFAULT '0',
  `event_type` char(1) NOT NULL DEFAULT '',
  `event_date` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `host_id` (`id_host`)
) ENGINE=MyISAM AUTO_INCREMENT=135549 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `icmp_index`
--

DROP TABLE IF EXISTS `icmp_index`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `icmp_index` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_host` int(10) unsigned NOT NULL DEFAULT '0',
  `date_time` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  `up_index` int(10) unsigned NOT NULL DEFAULT '0',
  `down_index` int(10) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=1208917 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `icmp_rtt_log`
--

DROP TABLE IF EXISTS `icmp_rtt_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `icmp_rtt_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_host` int(10) unsigned NOT NULL DEFAULT '0',
  `rtt` int(10) unsigned NOT NULL DEFAULT '0',
  `rtt_datetime` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=270974084 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus`
--

DROP TABLE IF EXISTS `mbus`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus` (
  `id_host` int(10) unsigned NOT NULL DEFAULT '0',
  `mbus_inhibition` tinyint(1) NOT NULL DEFAULT '0',
  `mbus_timeout` smallint(3) unsigned NOT NULL DEFAULT '4',
  `mbus_port` int(6) unsigned NOT NULL DEFAULT '502',
  PRIMARY KEY (`id_host`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_tables`
--

DROP TABLE IF EXISTS `mbus_tables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_tables` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_host` int(10) unsigned NOT NULL DEFAULT '0',
  `unit_id` smallint(5) unsigned NOT NULL DEFAULT '255',
  `type` varchar(16) NOT NULL DEFAULT 'word',
  `address` smallint(5) unsigned NOT NULL DEFAULT '20610',
  `size` smallint(5) unsigned NOT NULL DEFAULT '87',
  `status` char(1) NOT NULL DEFAULT 'E',
  `update` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=73 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_tg`
--

DROP TABLE IF EXISTS `mbus_tg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_tg` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_table` int(10) unsigned NOT NULL DEFAULT '0',
  `use` tinyint(1) NOT NULL DEFAULT '1',
  `error` tinyint(2) NOT NULL DEFAULT '1',
  `index` smallint(5) unsigned NOT NULL DEFAULT '0',
  `tag` varchar(15) NOT NULL DEFAULT '',
  `label` varchar(25) NOT NULL DEFAULT '',
  `tg` int(1) unsigned NOT NULL DEFAULT '0',
  `last_tg` smallint(5) unsigned NOT NULL DEFAULT '0',
  `last_tg_h` int(10) unsigned NOT NULL DEFAULT '0',
  `unit` varchar(8) NOT NULL DEFAULT '',
  `weight` int(10) unsigned NOT NULL DEFAULT '0',
  `info` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=MyISAM AUTO_INCREMENT=36 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_tg_log`
--

DROP TABLE IF EXISTS `mbus_tg_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_tg_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_tg` int(10) unsigned NOT NULL DEFAULT '0',
  `type` char(1) NOT NULL DEFAULT 'H',
  `tg` int(10) unsigned NOT NULL DEFAULT '0',
  `update` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `id_tm` (`id_tg`)
) ENGINE=MyISAM AUTO_INCREMENT=2806309 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_tm`
--

DROP TABLE IF EXISTS `mbus_tm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_tm` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_table` int(10) unsigned NOT NULL DEFAULT '0',
  `use` tinyint(1) NOT NULL DEFAULT '1',
  `error` tinyint(2) NOT NULL DEFAULT '1',
  `index` smallint(5) unsigned NOT NULL DEFAULT '0',
  `tag` varchar(15) NOT NULL DEFAULT '',
  `label` varchar(25) NOT NULL DEFAULT '',
  `tm` float NOT NULL DEFAULT '0',
  `unit` varchar(8) NOT NULL DEFAULT '',
  `info` varchar(30) NOT NULL DEFAULT '',
  `can_min` int(11) NOT NULL DEFAULT '0',
  `can_max` int(11) NOT NULL DEFAULT '1000',
  `gaz_min` int(11) NOT NULL DEFAULT '0',
  `gaz_max` int(11) NOT NULL DEFAULT '1000',
  `signed` tinyint(1) NOT NULL DEFAULT '1',
  `log` tinyint(1) NOT NULL DEFAULT '1',
  `al` tinyint(1) NOT NULL DEFAULT '0',
  `al_min` tinyint(1) NOT NULL DEFAULT '0',
  `tm_min` float NOT NULL DEFAULT '0',
  `al_max` tinyint(1) NOT NULL DEFAULT '0',
  `tm_max` float NOT NULL DEFAULT '1000',
  `tm_hist` float NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=MyISAM AUTO_INCREMENT=1139 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_tm_log`
--

DROP TABLE IF EXISTS `mbus_tm_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_tm_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_tm` int(10) unsigned NOT NULL DEFAULT '0',
  `tm` float NOT NULL DEFAULT '0',
  `update` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `id_tm` (`id_tm`),
  KEY `update` (`update`),
  KEY `graph` (`id_tm`,`update`)
) ENGINE=MyISAM AUTO_INCREMENT=310269817 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_ts`
--

DROP TABLE IF EXISTS `mbus_ts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_ts` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_table` int(10) unsigned NOT NULL DEFAULT '0',
  `use` tinyint(1) NOT NULL DEFAULT '1',
  `error` tinyint(2) NOT NULL DEFAULT '1',
  `index` smallint(5) unsigned NOT NULL DEFAULT '0',
  `bit` smallint(2) unsigned NOT NULL DEFAULT '0',
  `tag` varchar(15) NOT NULL DEFAULT '',
  `label` varchar(25) NOT NULL DEFAULT '',
  `ts` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `label_0` varchar(15) NOT NULL DEFAULT '',
  `label_1` varchar(15) NOT NULL DEFAULT '',
  `not` tinyint(1) unsigned NOT NULL DEFAULT '0',
  `info` text NOT NULL,
  `al` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `tag` (`tag`)
) ENGINE=MyISAM AUTO_INCREMENT=2122 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_ts_log`
--

DROP TABLE IF EXISTS `mbus_ts_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_ts_log` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `id_ts` int(10) unsigned NOT NULL DEFAULT '0',
  `ts` tinyint(1) NOT NULL DEFAULT '0',
  `update` datetime NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`id`),
  KEY `id_ts` (`id_ts`),
  KEY `update` (`update`)
) ENGINE=MyISAM AUTO_INCREMENT=1150250 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_v_grad`
--

DROP TABLE IF EXISTS `mbus_v_grad`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_v_grad` (
  `id_tm` int(10) unsigned NOT NULL DEFAULT '0',
  `use` tinyint(1) NOT NULL DEFAULT '1',
  `last_tm` float NOT NULL DEFAULT '0',
  `max_grad` float NOT NULL DEFAULT '0',
  `comment` text NOT NULL,
  PRIMARY KEY (`id_tm`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_v_tg`
--

DROP TABLE IF EXISTS `mbus_v_tg`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_v_tg` (
  `id_tg` int(10) unsigned NOT NULL DEFAULT '0',
  `id_host` int(10) unsigned NOT NULL DEFAULT '0',
  `script` text NOT NULL,
  `i_time` int(10) unsigned NOT NULL DEFAULT '3600',
  `c_time` int(10) unsigned NOT NULL DEFAULT '0',
  `comment` text NOT NULL,
  PRIMARY KEY (`id_tg`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_v_tm`
--

DROP TABLE IF EXISTS `mbus_v_tm`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_v_tm` (
  `id_tm` int(10) unsigned NOT NULL DEFAULT '0',
  `id_host` int(10) unsigned NOT NULL DEFAULT '0',
  `script` text NOT NULL,
  `comment` text NOT NULL,
  PRIMARY KEY (`id_tm`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `mbus_v_ts`
--

DROP TABLE IF EXISTS `mbus_v_ts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mbus_v_ts` (
  `id_ts` int(10) unsigned NOT NULL DEFAULT '0',
  `id_host` int(10) unsigned NOT NULL DEFAULT '0',
  `script` text NOT NULL,
  PRIMARY KEY (`id_ts`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `subnets`
--

DROP TABLE IF EXISTS `subnets`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `subnets` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(30) NOT NULL DEFAULT '',
  `gateway_tag` varchar(15) NOT NULL DEFAULT '',
  `gateway_code` varchar(30) NOT NULL DEFAULT '',
  `link_type` varchar(20) NOT NULL DEFAULT 'P',
  `link_backup` char(1) NOT NULL DEFAULT 'N',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=67 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `variables`
--

DROP TABLE IF EXISTS `variables`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `variables` (
  `name` varchar(30) NOT NULL,
  `value` varchar(255) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping events for database 'sup_rst'
--

--
-- Dumping routines for database 'sup_rst'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-13 14:41:27
