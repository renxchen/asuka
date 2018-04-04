# Host: 127.0.0.1  (Version 5.6.21-log)
# Date: 2018-04-04 10:40:31
# Generator: MySQL-Front 5.4  (Build 3.48)
# Internet: http://www.mysqlfront.de/

/*!40101 SET NAMES utf8 */;

#
# Structure for table "apolo_user"
#

CREATE TABLE `apolo_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(32) NOT NULL,
  `password` varchar(32) NOT NULL,
  `token` varchar(500) NOT NULL,
  `mail` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "apolo_user"
#


#
# Structure for table "auth_group"
#

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "auth_group"
#


#
# Structure for table "auth_user"
#

CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

#
# Data for table "auth_user"
#

INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$36000$ahmciRXINg0H$cCXS9jifKRzeWhF7zI3rko3Ap0n3fG0XnO2HHozQ1ZQ=','2018-03-27 06:31:06.634000',1,'admin',' ',' ','kk@cisco.com',1,1,'2018-01-24 01:42:39.273434');

#
# Structure for table "auth_user_groups"
#

CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "auth_user_groups"
#


#
# Structure for table "devices_tmp"
#

CREATE TABLE `devices_tmp` (
  `operation_id` int(11) NOT NULL,
  `device_id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(256) DEFAULT NULL,
  `ip` varchar(30) NOT NULL,
  `telnet_port` int(11) DEFAULT NULL,
  `snmp_port` int(11) DEFAULT NULL,
  `snmp_community` varchar(30) DEFAULT NULL,
  `snmp_version` varchar(5) DEFAULT NULL,
  `login_expect` varchar(1000) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `telnet_status` varchar(200) DEFAULT NULL,
  `snmp_status` varchar(200) DEFAULT NULL,
  `device_type` varchar(255) DEFAULT NULL,
  `ostype_id` int(11) NOT NULL,
  `group_name` varchar(2000) DEFAULT NULL,
  PRIMARY KEY (`device_id`)
) ENGINE=InnoDB AUTO_INCREMENT=1331 DEFAULT CHARSET=utf8;

#
# Data for table "devices_tmp"
#


#
# Structure for table "django_content_type"
#

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8;

#
# Data for table "django_content_type"
#

INSERT INTO `django_content_type` VALUES (1,'apolo','collpolicy'),(2,'apolo','mapping'),(3,'apolo','historycliint'),(4,'apolo','event'),(5,'apolo','triggerdetail'),(6,'apolo','collpolicyruletree'),(7,'apolo','historysnmptext'),(8,'apolo','historysnmpint'),(9,'apolo','collpolicygroups'),(10,'apolo','items'),(11,'apolo','datatableitems'),(12,'apolo','policysgroups'),(13,'apolo','historysnmpstr'),(14,'apolo','user'),(15,'apolo','devices'),(16,'apolo','triggers'),(17,'apolo','historysnmpfloat'),(18,'apolo','datatable'),(19,'apolo','historyclistr'),(20,'apolo','historyclifloat'),(21,'apolo','devicesgroups'),(22,'apolo','collpolicyclirule'),(23,'apolo','groups'),(24,'apolo','historyclitext'),(25,'apolo','actions'),(26,'apolo','ostype'),(27,'apolo','functions'),(28,'apolo','schedules'),(29,'auth','group'),(30,'auth','permission'),(31,'auth','user'),(32,'contenttypes','contenttype');

#
# Structure for table "auth_permission"
#

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8;

#
# Data for table "auth_permission"
#

INSERT INTO `auth_permission` VALUES (1,'Can add coll policy',1,'add_collpolicy'),(2,'Can change coll policy',1,'change_collpolicy'),(3,'Can delete coll policy',1,'delete_collpolicy'),(4,'Can add mapping',2,'add_mapping'),(5,'Can change mapping',2,'change_mapping'),(6,'Can delete mapping',2,'delete_mapping'),(7,'Can add history cli int',3,'add_historycliint'),(8,'Can change history cli int',3,'change_historycliint'),(9,'Can delete history cli int',3,'delete_historycliint'),(10,'Can add event',4,'add_event'),(11,'Can change event',4,'change_event'),(12,'Can delete event',4,'delete_event'),(13,'Can add trigger detail',5,'add_triggerdetail'),(14,'Can change trigger detail',5,'change_triggerdetail'),(15,'Can delete trigger detail',5,'delete_triggerdetail'),(16,'Can add coll policy rule tree',6,'add_collpolicyruletree'),(17,'Can change coll policy rule tree',6,'change_collpolicyruletree'),(18,'Can delete coll policy rule tree',6,'delete_collpolicyruletree'),(19,'Can add history snmp text',7,'add_historysnmptext'),(20,'Can change history snmp text',7,'change_historysnmptext'),(21,'Can delete history snmp text',7,'delete_historysnmptext'),(22,'Can add history snmp int',8,'add_historysnmpint'),(23,'Can change history snmp int',8,'change_historysnmpint'),(24,'Can delete history snmp int',8,'delete_historysnmpint'),(25,'Can add coll policy groups',9,'add_collpolicygroups'),(26,'Can change coll policy groups',9,'change_collpolicygroups'),(27,'Can delete coll policy groups',9,'delete_collpolicygroups'),(28,'Can add items',10,'add_items'),(29,'Can change items',10,'change_items'),(30,'Can delete items',10,'delete_items'),(31,'Can add data table items',11,'add_datatableitems'),(32,'Can change data table items',11,'change_datatableitems'),(33,'Can delete data table items',11,'delete_datatableitems'),(34,'Can add policys groups',12,'add_policysgroups'),(35,'Can change policys groups',12,'change_policysgroups'),(36,'Can delete policys groups',12,'delete_policysgroups'),(37,'Can add history snmp str',13,'add_historysnmpstr'),(38,'Can change history snmp str',13,'change_historysnmpstr'),(39,'Can delete history snmp str',13,'delete_historysnmpstr'),(40,'Can add user',14,'add_user'),(41,'Can change user',14,'change_user'),(42,'Can delete user',14,'delete_user'),(43,'Can add devices',15,'add_devices'),(44,'Can change devices',15,'change_devices'),(45,'Can delete devices',15,'delete_devices'),(46,'Can add triggers',16,'add_triggers'),(47,'Can change triggers',16,'change_triggers'),(48,'Can delete triggers',16,'delete_triggers'),(49,'Can add history snmp float',17,'add_historysnmpfloat'),(50,'Can change history snmp float',17,'change_historysnmpfloat'),(51,'Can delete history snmp float',17,'delete_historysnmpfloat'),(52,'Can add data table',18,'add_datatable'),(53,'Can change data table',18,'change_datatable'),(54,'Can delete data table',18,'delete_datatable'),(55,'Can add history cli str',19,'add_historyclistr'),(56,'Can change history cli str',19,'change_historyclistr'),(57,'Can delete history cli str',19,'delete_historyclistr'),(58,'Can add history cli float',20,'add_historyclifloat'),(59,'Can change history cli float',20,'change_historyclifloat'),(60,'Can delete history cli float',20,'delete_historyclifloat'),(61,'Can add devices groups',21,'add_devicesgroups'),(62,'Can change devices groups',21,'change_devicesgroups'),(63,'Can delete devices groups',21,'delete_devicesgroups'),(64,'Can add coll policy cli rule',22,'add_collpolicyclirule'),(65,'Can change coll policy cli rule',22,'change_collpolicyclirule'),(66,'Can delete coll policy cli rule',22,'delete_collpolicyclirule'),(67,'Can add groups',23,'add_groups'),(68,'Can change groups',23,'change_groups'),(69,'Can delete groups',23,'delete_groups'),(70,'Can add history cli text',24,'add_historyclitext'),(71,'Can change history cli text',24,'change_historyclitext'),(72,'Can delete history cli text',24,'delete_historyclitext'),(73,'Can add actions',25,'add_actions'),(74,'Can change actions',25,'change_actions'),(75,'Can delete actions',25,'delete_actions'),(76,'Can add ostype',26,'add_ostype'),(77,'Can change ostype',26,'change_ostype'),(78,'Can delete ostype',26,'delete_ostype'),(79,'Can add functions',27,'add_functions'),(80,'Can change functions',27,'change_functions'),(81,'Can delete functions',27,'delete_functions'),(82,'Can add schedules',28,'add_schedules'),(83,'Can change schedules',28,'change_schedules'),(84,'Can delete schedules',28,'delete_schedules'),(85,'Can add group',29,'add_group'),(86,'Can change group',29,'change_group'),(87,'Can delete group',29,'delete_group'),(88,'Can add permission',30,'add_permission'),(89,'Can change permission',30,'change_permission'),(90,'Can delete permission',30,'delete_permission'),(91,'Can add user',31,'add_user'),(92,'Can change user',31,'change_user'),(93,'Can delete user',31,'delete_user'),(94,'Can add content type',32,'add_contenttype'),(95,'Can change content type',32,'change_contenttype'),(96,'Can delete content type',32,'delete_contenttype');

#
# Structure for table "auth_user_user_permissions"
#

CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "auth_user_user_permissions"
#


#
# Structure for table "auth_group_permissions"
#

CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "auth_group_permissions"
#


#
# Structure for table "django_migrations"
#

CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;

#
# Data for table "django_migrations"
#

INSERT INTO `django_migrations` VALUES (1,'apolo','0001_initial','2018-01-04 02:06:40.847000'),(2,'contenttypes','0001_initial','2018-01-04 02:06:50.222000'),(3,'auth','0001_initial','2018-01-04 02:06:51.252000'),(4,'contenttypes','0002_remove_content_type_name','2018-01-04 02:06:51.521000'),(5,'auth','0002_alter_permission_name_max_length','2018-01-04 02:06:51.598000'),(6,'auth','0003_alter_user_email_max_length','2018-01-04 02:06:51.685000'),(7,'auth','0004_alter_user_username_opts','2018-01-04 02:06:51.722000'),(8,'auth','0005_alter_user_last_login_null','2018-01-04 02:06:51.828000'),(9,'auth','0006_require_contenttypes_0002','2018-01-04 02:06:51.847000'),(10,'auth','0007_alter_validators_add_error_messages','2018-01-04 02:06:51.878000'),(11,'auth','0008_alter_user_username_max_length','2018-01-04 02:06:51.961000');

#
# Structure for table "django_session"
#

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "django_session"
#

INSERT INTO `django_session` VALUES ('02bqxi59lqjcmhzmr3luw7zlzzffc8sf','MjBkNjJjNjJlNDY2N2Q0Y2MwNDI0N2M4NTA1ODBjMWNlODE0ZWM4Mjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFd09EQXpOemNzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRFd016YzNmUS5LbUpSOXBYUEd6RGZtT1BRejdSRkhTRWV6ODRzeXJOM3lfVlRyYk1zVThVIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-29 02:19:37.623461'),('0gv9vfyhvzlr6nqune8bmcfmj6k4jazm','YTdmYjA3NDBjZTE0MjI4MDlmNzlhODFjYjAzYzJmNzYwNzc1YTVhYzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFd01EWXpORGtzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TURNMk16UTVmUS5PSUl6clZzRnFIZWZ2SDRfTjJrV05pbWdQenZxNGQzZU1ScnJ6STlESElzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-28 05:45:49.979780'),('0ib91uwl4dysbvx38fepj3awai5ha26k','NTRmZDdiMjFjNDUwMjIzOWRiZjQ3MmJmNTI0NTZmYWZjNWMxZjllYTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNE1ERTJORElzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1T0RNeE5qUXlmUS53ekJDWmNlejhJay1lemFzejcyN2xuV0ZEMnotN2xETkZLTEUtOHhTallVIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-14 07:07:22.270000'),('10c1wd2vnvkr6bowy7mxanuwkjc8uhlh','MDg5Y2Y0ZTlmYTFhZGNiYTBkYWUyMzZmYzVlMGVkMzcyNmMzMDg4MDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNU9UVTJOVElzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TURJMU5qVXlmUS5COE1ORFpaSVBZUGJ5Mmk2ZjBOb05pbzdveGU3eWxuMkFmWlVlVDZKemEwIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-28 02:47:32.591217'),('1xx6dyy0rxpwsdz8yjefkto70hmg3t41','N2Y1MTIxNTY1OWM4ZThhNGQ3NmQwZDk2ZGEyMTk2NjZhYTEzNGZiYjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBeU9UazFPVEFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TXpJNU5Ua3dmUS5YQVBOb1hHR0hGWDRNTmdBbG51MGd0Z3hDSUxEZmY5cjQ3Y3FVTUplUUhBIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-20 01:26:30.060963'),('2xcrwmq9m2j1s0hz7vehadsz1d6nodwf','NzAwZmZmYmVkMzNjNGQyZWQyOTRiZWRmYzEyMWJlZjNmMGIwNWY0Mjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFeE1UQTJORE1zSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRRd05qUXpmUS5KM2RZYTcyWGltNERTRFNsUENPMFMzMDFkcGRBNkkyT0FIWlNoV2ViNm9RIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-29 10:44:03.265923'),('3pqxh1wdht5gjpbotdoeohe55xqb2tkg','MGIyY2MxMjZiMjcyN2MyOTY0Y2Y3ZmEwOTQzMjhjYzExOTE4NTRhODp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBek9URTNNakFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TkRJeE56SXdmUS4yeFBBVVZLVjhjd1I5WEdXNVhvNzVCaDJ4VmJDY3J0bG5XakpHVlhkaW1zIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-21 03:02:00.999465'),('3q9mbw5yfhk9m94e6u5m2028ar84audj','MDE1MjgxZWIwZmRlYmNiYmY5MmIxMDQ4YjY4YzRmZDZlMDdmODcwMjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRnME1ETTROek1zSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU0TkRNek9EY3pmUS5DX1FjcVVsUmlSbVJuYW1yNGhwVlpCRnpzX2gwY25MaUkteXI5OHV1S1NnIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-02-26 02:51:13.780344'),('3wqp84xls51d8jnki0ir54q3kc859htf','YTdhODU5ZTBmNTE2YzlmOTU5YTJhYThkZGJkMTNjMWE4ZmUyZWQzMjp7Il91c2VybmFtZSI6ImFkbWluIiwiYWRtaW5fdG9rZW4iOiJleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKMWMyVnlibUZ0WlNJNkltRmtiV2x1SWl3aWIzSnBaMTlwWVhRaU9qRTFNVGd3TlRjeE5ESXNJblZ6WlhKZmFXUWlPakVzSW1WdFlXbHNJam9pYTJ0QVkybHpZMjh1WTI5dElpd2laWGh3SWpveE5URTRNRGczTVRReWZRLmtlaEhXakl1c085X3ZZcHJyQTZHdjdQT0hNU3ZQek5TdmV3YWJhRDY0aVUiLCJfYXV0aF91c2VyX2lkIjoiMSIsImFkbWluIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2lkWE5sY2w5cFpDSTZNU3dpYjNKcFoxOXBZWFFpT2pFMU1UZ3dPRGN3T1Rrc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU0TVRFM01EazVmUS5LRndIdWxocUxrM1M3ZnFUQ1FiNEhoRkt1UmFrSE9NZ2U0M3Y1UC16Y3BNIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiJhNDlkOWM5ODY0ZTgwYTU1NjQ3Y2FhYzgwZTc2NDU1NGM1NmY5M2Y4In0=','2018-02-22 10:51:39.735420'),('4peg7v60kj097f3kovfp2kcfburfa89j','MDI5YmI3OGU3MmI5MTdiMWY3MzVhNzFkMWY5MDVmODM2NzRjNTk1Yzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNU1qazNOeklzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T1RVNU56Y3lmUS5jY0dUakNPRHRmbzlXSTlURW1tMlVQUmI3UE1EYXptVUhCMlp3RGVIRG1BIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-27 08:29:32.166227'),('4uwi5orvsxwryjmys3vcnfep61e153ua','ODcyZDcyZjNjODNjZGUwNGIzMTRmM2FlNDUzNDE3NTMxNzVlZWQzOTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME5EUTJNVGtzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRjME5qRTVmUS42WnJSODVraXVtYU5qYnJ2WFk0STdTdG1LWURQdGNtcWNLeU80WkkySVVNIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 07:30:19.561000'),('4zgnr8hw481pw98jrqfs0e1z6q9ir5wm','MTIxMzczMTk3MzNjOTJiYTc5OTUxZjEzNzA3MDkyNTkyODY4OTJhMjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRjNU56Y3dNRFFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU0TURBM01EQTBmUS45cEE4TmhOSXFlZkJWOVlUSkd1b0tqajR5Y1RhNy1zWDI4akQ2Y1E1WFNvIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-02-21 04:16:44.571514'),('5b9jg5xw464240axy5twr7t2xswvmdw4','MzJiY2E5Nzg5Njg3MWYwZWQ2ZmE0N2QyNDdhMDFhNTlkZTEyYTVlNDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME1qVXdNelVzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRVMU1ETTFmUS5DQ1RMQzJaOUdULW1oUmp1ZU1ZY3NLZEFEUkJoSHVMQTJOYlFraU9VOGo0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 02:03:55.947906'),('5sqcpkb89zce6y7sxzeuhfavchdyqm5u','OGZkYmFjYjU1YjlmMGE3OTliM2M2ZjNkMzQ3ZWYwMDhiNzhhZDJjMjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBek9UY3pNRFFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TkRJM016QTBmUS5OdndoVmdBVnQzbG10ZGpDc19UbWgwZnk5ZWF4OXR2VC1PdkFMc0stZGc0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-21 04:35:04.845118'),('6seb9qhacl5oihbybex9b3sz7gyupyye','NTM0YTY5Yjk4MTFlMjJmYTQ2YzA1ZTgwNzM2ZTM4MjE2NzhhODdmZDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRjNU56RXlNVFVzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU0TURBeE1qRTFmUS5wOHlHeWU4SlF1empyb0VPSEZqZ3doY0w2TXd4eTVJU0pVcW5uWjcxcUpvIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-02-21 02:40:15.400197'),('741lqowj16gw7fwdft3lnbm56pbncarr','YWE4YTdiMTMyYTU5MjFhM2E2YzczNzk5NDk0Njg5NTMyMGRiYTQyMzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBeU1USXlOVFVzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TWpReU1qVTFmUS52UkstajRLbzJ3RTZDZEFNUlRJQjhvdUdNc0huSGtxcGViM2NFc2RCNWxBIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-19 01:10:55.360423'),('85qmw80np0v65phvq4grpfchhmtuv5tg','ODIyZmNkZTI1YTBmNWQ2Zjc3MzBiNGUyNWM5ZDc2MWQwMmJjZTc4Mjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNU16VTJOelVzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T1RZMU5qYzFmUS5KYzV6VktGdFR3aGVieGVYX0ppbW9aalliMGphOGNRNkxicFlrdFJqS1E0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-27 10:07:55.680150'),('8c7aj0ndqjt1p2rq2nz1dbztaqn4g52p','MzdhYjFiNGFkZDA3YmY5M2VlODQ2NTM2M2I3ODljZTdhNzU1YmVmMTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME5ESTFNeklzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRjeU5UTXlmUS5COXc3SFVDeG02Slh3MjdvYWJKRHluUklFTU1oTGRobmNSdXF0alZvU3RrIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 06:55:32.456704'),('8dh0c64nmhns3019fmqz6b12nn5x8418','M2Y2YmQxYmRjNzI4ZmM2ZGVmYjljMzc2ODcyZjNkODRiODhmYmVjOTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNU16RTNOVFFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T1RZeE56VTBmUS55ZUNUbGEzRnc0OG12QU9sNHNoQUpKZDJ2cGkya1hnLU5ESWFXUEIwTGJVIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-27 09:02:34.160000'),('9ozvb3juep76lsey9ot4qdczftxo71e3','NTEyNTJjZjZlOGVkOTIzYzRjMTAyN2JkMzk4MWY0NzIzOGQwOGJkNzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFd01EVTFOVE1zSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TURNMU5UVXpmUS53RHFTeTR1Qk9kRUpLdnpvdDBiNEVNZ0RxM0NDWEpnUlB2czRiMDdkOE13IiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-28 05:32:33.181348'),('a43936jcpc55g4er3kedq9p609xjpan7','YTMzNTgxNjJlNTY1OTkwYzcyMTVmMDg0MDQwZDNkMGRjYTA1MDYwMDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFeE1ERXpNakFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRNeE16SXdmUS5DSWFHSEpPeHM2VnlyWjZGWXZLVlFsVTFtaTlQQ0QyRGczUkdLYmZhb2dVIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-29 08:08:40.313219'),('adj00xd39f995rk1zc4c9ciz68eeualx','ZGE0Y2U5N2YzZGNmMWJmMmI1Y2RjZTM1YjYzOGFmNDVhZjk5N2RjZjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrMk1UQTJOVFFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1TmpRd05qVTBmUS5Id2VSZE9pRGJRSVpYX3VFTFkxU3VWWkE2bFFST091dmQweVEyN2dnQmZzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-12 02:04:14.205096'),('ai4t5s7kg6pxua6un7tonfvy7l31l6v7','OWEyZmY1OGFmYWQ5ZjUxYzg5NDJlMTkyYzExYjBhZmI0ZTE0NmQ2NTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME16Z3lOVElzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRZNE1qVXlmUS5JZ2ZKVFFsQzNSNXR5N1pRLXFhaFU1RWlDLUNzMmdUeWlUSGZISXBGdXUwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 05:44:12.366262'),('arze4smmv2j8e5a541gvlyni8cldcpwp','MDBkYzIyZDFkMmUzMDAyNDk5NjlhNjRlZDgyYzEwNGIxNzBlODg0Nzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME1qVTFOelFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRVMU5UYzBmUS5Lc2FpQXU5eWxMM1dPVWZac1N0dDU5SldTR3hxa2ZZaHVHLS1VbC1tZ0QwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 02:12:54.239058'),('b8il4u0sbnwqtais7kx1amxobajv1la0','MDNlZGIzODdlYjA0ZmQ3YjRmNzkzMDZlN2Q0ODRkZGExYTIyZjE0ZDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNE1URTNNRE1zSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1T0RReE56QXpmUS56MWdqZmZqRW5fRl9OTGlOMFM2VFpENlJuV0VBTVhjODVaYi0wNk1lcHJRIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-14 09:55:03.446000'),('bsarhqwb1vuts4furl8e76j9qct4d5n5','NjU0YzJmZWZkMmY1ZDQ3MmFmNzFhZjFmMGQ0MjQwZTdkZjE1NDNkODp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNU56UTVORFFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TURBME9UUTBmUS5McGJpUzVRNFhEa3dGekE5Mlp6NTlHaG1aZUNXRFBJTUQ2OVFLS2c0bHRnIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-16 07:15:44.352000'),('c4jlwcd2c8l9hp0fp6c9lci02tipngal','OWYxNzMyYWMwY2Q4MWFhYTVmYmNlY2MxMTk4YWI3YTYyNDRhODkwZjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrMk1qazNORGtzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1TmpVNU56UTVmUS4tVjNjRl9BSG1ubXhGZ0plYnFkZUQ3dFFvWGd1dzQyNU5LeEZPZVZQQXlnIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-12 07:22:29.393599'),('crb2paulp58ef17wh43oipphnb85fd1b','NjA4YTBiYmQ5NWM3YmE1NTZiNjNhZGE3MGQ2NjBjYjk1M2ExMGZhNDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrMk1qazNOVEVzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1TmpVNU56VXhmUS5lVFM1MHgwcDlXOUwtS0xCcTI3TTRKVk9rOHZHbkVFY0JMSzZHUzBWRG5RIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-12 07:22:31.021994'),('d54o35fk69q0i0grpjm0m1mjos5eq13b','YTZhNDc4OWQ4NWYyMWQ5ZmJlMzRiZWVkNDUwZDI3ODAxNmU5NGRiYzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNU16RTBPRGtzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T1RZeE5EZzVmUS5rZ1lMaHc1N2Nhem1lWmN3Qzk1WUttQ2xQVW1RQktGQmg5dFB6VXVvWVJVIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-27 08:58:09.511728'),('e404pli9bmmmj4tq21qka67m0ruy2q6d','YjFjMGFjMmFlYjJhMDE3ZTg1OTBiNDYwZWQ4MzVmZDhjNTA2YWVhOTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRjNU56SXpNVEFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU0TURBeU16RXdmUS51dkFlalM5XzBTbWRhSng0bllNMlhUbTFTOFVmQlNrNTNUQTlEZnJXdnVNIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-02-21 02:58:30.347325'),('f1cz0w17hemrv67sbm9mys6a6ohzsqlh','YTI0OGE1ODVkOTk3MjRkYTE4OGZkNDYyM2MyOGQ0NmYyOGNiYmM5ZDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNU5UVXpORFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1T1RnMU16UTJmUS5sQ3BFYmpGSTFNMF9IbDY0YmdqcnhIUVFEOTVkT0Y4RDQtTVZnRF92aVQ0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-16 01:49:06.204269'),('f2o2aejpwc7svazdfhj0swfsrbvju74o','YzlhZGY3NjYyZWZlMWRlY2RlMDU1Mzc1MzI0ZGZhMzA0M2EzOTg2Zjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNE16UTBPVFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T0RZME5EazJmUS5JWjZCOTdfRUtveENKdFBrY2w4TlY1WjFfeXhpZV9ud2kxbXcxN0ZMX0dZIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-26 06:01:36.999000'),('g1evyhesxxd5e5q4abtjy6v7wobhqol1','MDNlZGIzODdlYjA0ZmQ3YjRmNzkzMDZlN2Q0ODRkZGExYTIyZjE0ZDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNE1URTNNRE1zSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1T0RReE56QXpmUS56MWdqZmZqRW5fRl9OTGlOMFM2VFpENlJuV0VBTVhjODVaYi0wNk1lcHJRIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-14 09:55:03.514000'),('gb116zcoiwxpye07g9ts7tyr3yb3c6ml','ZTYyNGIyMTNmNzIyN2MxNGRmNTdhYmRkYTFjNjAxMWNhZjc5NWY1YTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFeE1EZ3hPVGdzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRNNE1UazRmUS5NdzRIWmRUQmt6SzJhWGVmd0lJYV9uWWFQNmJEdnlQbFhBUklYa2ZGb25JIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-29 10:03:18.792000'),('haa4et4ba9y0et56z8bhgf3svmkl1e7f','YmQ2ZjZjN2ZlM2I0NjBlZThiNWJiMmJhMDZkNzdlYjQ1ZGRjNzVjODp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFd09UUXlOVElzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRJME1qVXlmUS5Ec3ZuUHBGQnl5aWRJc2V0Yll2RjNjT1R3TFNieHJ3T2pXaEhfMFZvazBjIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-29 06:10:52.578916'),('hvbylwm5zcqeg6hmkbaiy3i6q6xwyji7','MjQxODAyNWRmNTUxYmM3OTU1MDk2MTM2Mzg5YTc3ZmEwMzNjOTg1Njp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpJeE16SXlOallzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl5TVRZeU1qWTJmUS5DWndzLWpnTGdHOTZLMWRxTENabVg1bDVBVDRzNTBNMGRBMUZjcnprSC1ZIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-10 06:31:06.640000'),('kfrthxfkyikcn5g145914e48qm4hpjmf','YWY0NzQwNjNmOGFiODQzNjcyMDU3YjI1OTRjMTRiZDk1ZjRiNzBmMTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNU56STVPVE1zSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TURBeU9Ua3pmUS51UGVqcTJMdkhhM1hvalEyNnkteXRpcDVnY2RVOTdubVVTMHdWbGRVMmpBIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-16 06:43:13.201164'),('kkpd88i4x2ctvjaret16vhpkzl45kkvi','Mzk3M2JlZGYyNjkyY2M1NDMwNWRmY2I2MzFiYzA2Yjk0MDJlOTdjYzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNE5qY3hOVGtzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1T0RrM01UVTVmUS45eUFlcmMwZDBiSFlfM1E4SGVQeGRNelFUdWR3WUFWYjJiREpXSDJGbXdzIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-15 01:19:19.853302'),('kn5pv3a9wtaeppdoffqze5l64sosr7q1','YzgzMTVhNGRlYjQ4ZGRhMDZhOTk4ZjRmMmVlZTcxMDBmM2U3Y2YwMDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNU1qYzRNVFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T1RVM09ERTJmUS5US1I0dHlCOXBNb2p1MkdSMHd0NnA2WkRDa0pWS1g2VjFINXZVMExERnJNIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-27 07:56:56.063304'),('kpq4krchzn7d5342m81v9r8hy34tebme','Y2Y0YmI5MDViYzEzYzQ1OWU4MTAxMDE2YTA3ODU5ZTQzOTJmYWZhZTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBMU56WXpNallzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TmpBMk16STJmUS5VWkVVcTFlcm9VRnNYQnM4VC05VGU2Q2sxS0NmMWl3SExyNnFfWU92b1pnIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-23 06:18:46.663000'),('kqe4eqybv2lffp5jw6j32q24drx5nshm','ODVkNmE4ZTRmYTEyOWIxMDA0OTgyNDAwOWVkOWE1ODcxMzg0NTU2MTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFd01EWTBNakFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TURNMk5ESXdmUS40Ym9OOVRtcDdGRkNhbXlnX2pwMEUxaGJ0ZHVmZkV2T3ExMkxid1hsWEpJIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-28 05:47:00.457133'),('lo73kokeu2lg78q6ivkowvpavl5gmrcj','N2YyMWI4OWI5YmUyZmQ0YzQxY2NkNzkwNGUwMDk4MjBhZTZhMmNkYjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBMU9EVXhORGdzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TmpFMU1UUTRmUS5pSmhHNEdWYUdpY01nNzhkTkNaMjlZWWFZZUhLaWItYnUxN25mc2NxSlZRIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-23 08:45:48.566911'),('lpn8a1l6o43oldhoxxg328ywjrcm4lqo','MmQ2N2Q0OGU3YmI4OTQxYjc0MWQ5ZTU2YTNmODBhM2U1MTg1YzVkYzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNU56WXlOVEFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TURBMk1qVXdmUS44TGxQTzM3QnpTNEtKM193ZVlRYVJtb3RBTGVUMVFJclduMGx5aFYzbFdrIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-16 07:37:30.166000'),('lx624gdj90251zvkx8iu44vkmyme80fa','ODkxYmY3NDUxYjk2ZWUwYWU3N2M4YzViMzM2NjlkOWNlMmIxMDdhNDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNU9UTXlNamNzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TURJek1qSTNmUS5RWXVMN0Zoc1FzeldGYTdERGVMUlJsdE9mRlBmdEpBRDNYa2tFb05KVVhBIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-28 02:07:07.656903'),('nmjetj2pkexn0qmbfnh1pnruac8as8c4','OTc1NjMyMzY0YTAwNmM0YjliYzI5M2NjODNkMGYyZTg1NWYzM2ZhOTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME16WTJPVEFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRZMk5qa3dmUS5fYzZYcTRwVkY1NlFPQ09aR2RoeVQ5WERqU2lJYlFrUEw3d2Y1RFowMGlNIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 05:18:10.221648'),('ob0txrkdm4y9n3lohh05ktv938wagr35','MmY2YjQ3NzA3MTM3MjdmMjhmZTZiNWIyYmU0YmU3MzM1YWU4N2M3Yjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME1qZzNORFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRVNE56UTJmUS5OMXY1ODB3UWtGdkdwN3NuY3JFU1JlLXY4STVoYmJoNXo4LWRDYnVpc1hZIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 03:05:46.714223'),('odait2ilhyia9kqxcywjrg1o5abdt10n','NjNiOTZiZGMzNjJhMTVlNWQzYWQzMmI5ZmRlMDgxMDgyN2ZmZDRhYzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFd056Z3lORFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRBNE1qUTJmUS52aE4tRWJBbW93WXU0X0VOZ0xBejZnbGU0S0xnNzYzS2pKcDhkYXFha0pRIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-29 01:44:06.572720'),('of6o72ukp9l2p67h1udtrdtp4so87i19','MWE1NjdjMGZjMDRlNGVlMzZhMmZhNWY1ZWVjNzk4YjUyOTRiMzZiYzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNU9UYzBNak1zSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TURJM05ESXpmUS5QX1htQlRRQWwxQ0ltZEowbG4wbHhoTFhuLTdUcTlhUkFCYjhPZGxvQjlnIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-28 03:17:03.068642'),('onldku1e4kqxtagyhwc8tmn81h7avnfg','YmNkZWVlOWYyYTQzNTA3NmUyNGYwZTRjNTg0NzZkMWE5ZGQ2ZTNjYTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRjNU56TTJOekVzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU0TURBek5qY3hmUS41SFlIQzFXX0NBb195bDl1MU9GSTZhREdxX0tsbDRUNkk4QnllR2pRRVFnIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-02-21 03:21:11.927116'),('pf2at45fg9z0cm4866qzvkpvqade420j','ZDdlNmRmNzBlZDIyZmRlYWRhMTFhZjQyNDI5MmFhY2YyNGE5YThmZDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRjNU56STFNRFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU0TURBeU5UQTJmUS5NVXFvWklzTHQ2Mkd0aElzUWhVcXVQMWRtSTdyM01xSUlmYkRIWkRpS2dRIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-02-21 03:01:46.131913'),('pg0hddo6do1saasxiewvff28bx0cfxr6','MTQ4Yzg4MWEzNTI1N2RkYmI0NjBhOTQ3YTZiNmNjNTM4OGYwMWMzMzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNE16WXpPVFFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T0RZMk16azBmUS5kTDlOV0NfcWItQTdBVFJDNzBPUUJkN1BxSG1PTFBneUd6di1PS1dUdUV3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-26 06:33:14.186000'),('q410oudws06dfqf65m16bmewlayujbol','NjhhNDFhNjNlZWI4OWI1ZmY2MTI5NjU3NDI5MjlkYTM0NmNkMzBiNjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrMk1qVTFPVGdzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1TmpVMU5UazRmUS5PV0ttaEpYRk1DUVFyWkQtM1d1R0prVVdhN01jTDVGNzA4bENXc0J6QjFFIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-12 06:13:18.045392'),('qawxgq46o72bbm3nhb6m2gfip88pe2wp','ODUxZGFkOTA3ZTU2MjFkODg3ZmM2MTk2ZjFmNDg2YjMzNzNkZWI1MDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNE1qUTFNVElzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T0RVME5URXlmUS45anN4MVBsMVhISDRia3BGbS13ZjVTNmZjc0ZVd3Z5SERaYWhUV3FmUFRjIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-26 03:15:12.105906'),('qmi8xpvcdvysz8u2ae2ciz1w9nfnzxr4','NTVhMmRiNmFhNDAyMzAzNTkyZWZiOWZjMmQzZGFjYWU3OWIyZGNhNDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNE16UTBPRGdzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T0RZME5EZzRmUS5yWmsxTkhBWUpZSUxRNlBIb3piY042NTVYZHBVVzRQSVhCWW5vME4wYldRIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-26 06:01:28.791000'),('qtdsaab2kp3dw365zi1n1c28y9spy0md','Mzg2MWQzNDNhMDQ5YjI1MDNhODBmYjk5NTMwNjhhN2VjNDAzMTk0MTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNE16WXdORGtzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T0RZMk1EUTVmUS5XWk1XS0NvZEZCcmxqbkFQR1E1dFEtZVBjZWNUd09iclYydFpzNVFfd1prIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-26 06:27:29.004000'),('ravva40xu96suxlfkefvwa3apm2cxl5l','Y2UyNDU2OGE4NWI3YWE1Zjg4OGE0ODg0YWU5Njk1Njc1YmQ5ZTJjZjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNE16STNPVFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T0RZeU56azJmUS5pejh4MUJrM0xMQnpVOTZydlU1Y25LVkNDV21DZWZYckswNFFBN3g2dWNVIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-26 05:33:16.201000'),('rdg4aqw99muwq78bmcqyvky8p22d8pp9','ZTZmNWEwMTA3N2IxZDUxN2I5YTQ2YTIwNDljMDE5NWM1Y2M5N2QyMTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME5ESTBNek1zSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRjeU5ETXpmUS5JRzdSMnRQbzkydHJ6VVFMT1FHTEVGYWhlcklLMXFnX1ZpaVJYQ3FLUHlJIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 06:53:53.809420'),('rk8mwc5ohql7tjm9bua01s6gh07qywsj','MjAxNDJiMzZkNTUzNWZjZTM4MWM3YjQ4ZmI3M2MwYWFlMThmOTVhYzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBeU16QTROVGNzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TWpZd09EVTNmUS5rc2RJMXhNQ1o4bUVLZ2stYVJ3ZklVNE1TeUhmZEo3OGlZdFBlVVBtbzdJIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-19 06:20:57.654904'),('rnox6u3xgbhb2zwpnd1drm1sdyhb6pni','NjFjODY0ZGQ2ZWQ5MDNmMTNjM2I1N2U2NTkyOWRjMjVjNzI4YzY0Njp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME5EWXpNRGdzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRjMk16QTRmUS5zSEw2VHNIek1LajkzeVBCNF9hY3kxd29WLW9yS28tSVZMdDYxV0UwdHBBIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 07:58:28.932388'),('rsrytbye5exq6c3d1ef1posl9kyti279','M2U1YjI2YWY3OTNiMzM0NTZkYzJlZDA4NmJhZWIyZDAyY2MzYzNjNzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNU56WXlORGtzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TURBMk1qUTVmUS5MOFRVTnBmZ3hGUVdHZi01WU5jbUxRRHVKZDYwaWtfbkZnNTBxLUtLUTJvIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-16 07:37:29.191000'),('s291l9ge0mwk7cn7yzkowj2onj2w647a','ODY4NzkyYTU2NTI1OTE4ODE2YmRjYWJiMWFhNjhiOGIyNjM5MzZiZTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNU5qSXlOemdzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1T1RreU1qYzRmUS5oNm8wTXpuSjBFNWstQkliT0lIR08wdkplVkNYM2gxQmJWWFJTOHJTZU9rIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-16 03:44:38.019461'),('s9jwpe5bvq1s065ahrw56984z2g4bjt4','M2RiYzAwY2QyMjk0OWM5ODllNTA2MDU4MDQ1Y2ZkODRjMzk4N2QxYTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFeE9UQXdORFFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TWpJd01EUTBmUS5zZW5zWk1PT21XMUg2Y2lYaGpJLTduWXpTRGoxWHhiZ2tQbzB6ZWJUVmlzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-30 08:47:24.827487'),('sa490jutkg40u37nn202bsr5m6ya6hj9','OTc2YzBhNjA4ZjliM2I2Mjk1OGEzMzVhZjU1MjM0ZDg3NjY2MzY4ODp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME5EZ3lNVElzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRjNE1qRXlmUS5Eak8yb2wtUzh6S21mb2owYzVzckkzRE9qRHpNTHdCZWl6WVplTmtqQzhJIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-04-02 08:30:12.095046'),('t7x6703u5uc4wjj3nc6p4kvorcinlt60','NGRmM2Y5MzA1M2JkNzA1ZTliNDdhZjgxMDc5OTgyMzBhOWJlMmFmZjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNE5EUTFNelVzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T0RjME5UTTFmUS5VQ3VUMzlYSUpJd3dPZjBmVkpJSWtiOWNBbE1ja21tRGhBb2VpVzlGanZNIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-26 08:48:55.352000'),('txm21i1vxd5bi5e5fbs5t1f6gr5ve53n','YjJmMWMxZThkNTNlOTU5ZmY0NjRmZDRiMjc0NTlkNGEzZjYzYWZhYTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFeE1URTFOVFFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRReE5UVTBmUS5QUzhfLUFuV1daSFpSTjY1UHJ3c2tDXzFKWDFSeHFoZlJ2V2k4azdEWG5zIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-29 10:59:14.565681'),('v9c4gjn9jqrmlil8tclfxkaitckebbsw','MGQ1YTA2NmU1ODNiNWQ2NGRkMGI5OTk5MzYxMTc0MWY0ZjY5MTk0Mjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFeE5qVXhOVGdzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRrMU1UVTRmUS5Zb2trMllMZm81SG5jRW40WENFYlhJRVUxQ2x1NUlaVWJaSTBLU0pzMTNBIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-30 01:52:38.482000'),('vfqv9blji54faua0rq5sot88lgjpz36x','MDNlZGIzODdlYjA0ZmQ3YjRmNzkzMDZlN2Q0ODRkZGExYTIyZjE0ZDp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTVRrNE1URTNNRE1zSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEU1T0RReE56QXpmUS56MWdqZmZqRW5fRl9OTGlOMFM2VFpENlJuV0VBTVhjODVaYi0wNk1lcHJRIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-14 09:55:03.374000'),('vpmv5d90yjcb4ip5iwpd9ler2a813e4p','Y2I0NmQxNDFkY2RhYTVkM2U1NGZkN2EyYjczMzc1YzNjNDcwZGE5Nzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBeU1UY3hNRFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TWpRM01UQTJmUS5xWnlNYTV5S084SEZibE5MSG9adldlQzgxT1dhV1dRajA5aWl6NnUzVkw0IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-19 02:31:46.250000'),('w3nm5b7amns30d6fld5t24cexc5l3jk0','YzdhYTdmYjdmYmNmYzMzNGE1ZDQ5NGFlNGI2N2E5NzM3MmZjYzllNTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFd09UTTFPVFFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRJek5UazBmUS5oZWJFYkNib2lBdEN0TEkxQmdZQWM5RVRYS1dLaThmMEJHR0U1dWYtQU93IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-29 05:59:54.149346'),('wzvrbnka65jgy3e9i0aub5tpzob8c0da','YzhlMjdkYjc1MWI5OGJhNDkxYTFmN2I4YjViNDllZTU4MDUyZTE0Zjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFd09URTVNRFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRJeE9UQTJmUS5LQmVJVV96MzVlaFJ0WWQ5M3VjNjVucnFUb19CR3l0UWliRS1vdk9pa0RBIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-29 05:31:46.962587'),('x05dvsd6465e2d7a6xnsi9fduq158wsm','ZGVhZmRkN2VkM2M5M2Y4ZjlmODAzYTA0YTdkMDQ2NTJmZGQ0Mzk5YTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBek9UQXpNRGtzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TkRJd016QTVmUS5SU3FVS0toTzNVdkRFSlRMVXFfQUk1TUFXQ3pzcWVEX3hjWXVjcm5aWFNrIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-21 02:38:29.540521'),('x3riji0q6mxm7u1vhb0wufufv5a5hr00','MzM1ZGU2ZmRjOTNkZWY5OWM3YTVkNThmYzFlNWM3ZTI5MWY3OTY5ZTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFeE1EUTVNRE1zSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRNME9UQXpmUS51S3ptRGdsWjBFZEh2ZlpWcFBNRW9xSEpNQUJOVm5zU3hidmZHWk5jVHJRIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-29 09:08:23.651724'),('xd6vfmhpl3fnvmapvmhue3p41ybyscsb','NGQzNDUwOTU2NTExMjk5OWE2MTQ0YWRjODgzYmFmODEzMDU2YTc4NTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFeE5qVXhOVFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRrMU1UVTJmUS53Yk1EMUpjVHhGaXZocF94ZExaUFlRMGI1S3dUc3QydEhBejlYLTVKdFRVIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-30 01:52:36.634000'),('xm72pck5j1jfn688umafw8vqwd1et79b','NjdhYjUxM2JhOWUyNGZlODYyN2RmZGM1YmM0MmFkNzBjMWIyYmNjNjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFeE1EZ3hPVFlzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRNNE1UazJmUS54ZHpoWWFISEY0QXZPYlBGZFY1RURFTHdRV1pwa1ZCTHJ3SzZRejBmVGN3IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-29 10:03:16.632000'),('xyf2qa2vu2c0q0nwil9a2xhfmnbs3b1x','NTcyYzM5YWRlMmE2NDM5MGEzNjJhZDkyYzgzZTQ2NDZjZTBiNmJjYzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFeE1ESXdOREFzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TVRNeU1EUXdmUS5KQk9TMHNnZjU0RGZUQ3plMzRpWVBfQ0xsRUF4QkNoTkVnQmtIQUp3RTMwIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-29 08:20:40.841252'),('y4r3sfx4znxaf4az4938hltz5eezxqo7','NWM3YmMyY2U2ZTRkNmM2OTBmNDQwNmZkNmMwNzE4N2NiOWUyN2E5Zjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBNU1URXdPVGdzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3T1RReE1EazRmUS5KWjZYdU1rY0Q3X2JtdGVPOVdmVVlFeG5GbHlRVU9mU1BqSVJJSkR2b1cwIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-27 03:18:18.005286'),('ydivadvmycvarnbm39qzbtlccm077ud1','Y2M1MjkxMzJhZmRhNTRjYTBkOGE1MjUwNGJkMzVlODlkMjVlZGI2Mjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFd01EWTBOamdzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TURNMk5EWTRmUS40VXlhWktpYlBpOE1wSzZnUnFPTTloOHYyQU1UdDEzRVdhQVVKWUo5RzBRIiwiX2F1dGhfdXNlcl9pZCI6IjEiLCJfYXV0aF91c2VyX2JhY2tlbmQiOiJkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZCJ9','2018-03-28 05:47:48.874976'),('ynydldy7yclt0nejtr287qlmudyiljby','YzFlY2ZiYjBjYzFhZTM2NWU2ZjZkZjgyZWVkMGQ1NGI0ZThkNzkxMzp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME5EUTROVGdzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRjME9EVTRmUS5Qakh1OFY1M3g5SzZVa3NkNFg2VC1nMXc3X2stZUxsV3otOWdVUWZGQ0tjIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 07:34:18.930242'),('zo7k67rxx1xm974x5ifs2xeiylinosgq','OGI5ODFmZmZhODYwNmRlYjdjODliZDY2NzNkNzZjYzQyYmNhNjVkYTp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpBM05qVTJOalVzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl3TnprMU5qWTFmUS5Rd2tGdWNiUG1xV1RsdndZbFVldWFUSEpCQTVWaWhrVmtXenhoRkQyR2dzIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-03-25 10:54:25.719709'),('zvz27wocvht79f1lp6ahyqemd1z7t8kl','NTJmZjU4OTYzYzUxNWE1OGFhZWFlMWRhZmU3MTY3YjAwMGI0ZjYwMjp7Il91c2VybmFtZSI6ImFkbWluIiwiX2F1dGhfdXNlcl9oYXNoIjoiYTQ5ZDljOTg2NGU4MGE1NTY0N2NhYWM4MGU3NjQ1NTRjNTZmOTNmOCIsImFkbWluX3Rva2VuIjoiZXlKaGJHY2lPaUpJVXpJMU5pSXNJblI1Y0NJNklrcFhWQ0o5LmV5SjFjMlZ5Ym1GdFpTSTZJbUZrYldsdUlpd2liM0pwWjE5cFlYUWlPakUxTWpFME1qVTFOVEVzSW5WelpYSmZhV1FpT2pFc0ltVnRZV2xzSWpvaWEydEFZMmx6WTI4dVkyOXRJaXdpWlhod0lqb3hOVEl4TkRVMU5UVXhmUS5CWmppX1hES2FJUmlyMXJIRzdQSjZZdmNIOHMtRFplQlR5amRvaGNab213IiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2lkIjoiMSJ9','2018-04-02 02:12:31.066586');

#
# Structure for table "event"
#

CREATE TABLE `event` (
  `event_id` int(11) NOT NULL AUTO_INCREMENT,
  `clock` int(11) DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `value` int(11) DEFAULT NULL,
  `objectid` int(11) DEFAULT NULL,
  PRIMARY KEY (`event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "event"
#


#
# Structure for table "mapping"
#

CREATE TABLE `mapping` (
  `mapping_id` int(11) NOT NULL AUTO_INCREMENT,
  `descr` varchar(2000) DEFAULT NULL,
  `source` varchar(255) DEFAULT NULL,
  `code` int(11) DEFAULT NULL,
  `code_meaning` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`mapping_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "mapping"
#


#
# Structure for table "ostype"
#

CREATE TABLE `ostype` (
  `ostypeid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `log_fail_judges` varchar(3000) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `snmp_timeout` int(11) DEFAULT NULL,
  `telnet_timeout` int(11) DEFAULT NULL,
  `telnet_prompt` varchar(255) DEFAULT NULL,
  `start_default_commands` varchar(3000) DEFAULT NULL,
  `end_default_commands` varchar(3000) DEFAULT NULL,
  `desc` varchar(1000) DEFAULT NULL,
  PRIMARY KEY (`ostypeid`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8;

#
# Data for table "ostype"
#


#
# Structure for table "groups"
#

CREATE TABLE `groups` (
  `group_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `desc` varchar(2000) DEFAULT NULL,
  `ostype_id` int(11) NOT NULL,
  PRIMARY KEY (`group_id`),
  KEY `groups_ostype_id_f166de12_fk_ostype_ostypeid` (`ostype_id`),
  CONSTRAINT `groups_ostype_id_f166de12_fk_ostype_ostypeid` FOREIGN KEY (`ostype_id`) REFERENCES `ostype` (`ostypeid`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8;

#
# Data for table "groups"
#


#
# Structure for table "devices"
#

CREATE TABLE `devices` (
  `device_id` int(11) NOT NULL AUTO_INCREMENT,
  `hostname` varchar(256) DEFAULT NULL,
  `ip` varchar(30) NOT NULL,
  `telnet_port` int(11) DEFAULT NULL,
  `snmp_port` int(11) DEFAULT NULL,
  `snmp_community` varchar(30) DEFAULT NULL,
  `snmp_version` varchar(5) DEFAULT NULL,
  `login_expect` varchar(1000) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `telnet_status` varchar(200) DEFAULT NULL,
  `snmp_status` varchar(200) DEFAULT NULL,
  `device_type` varchar(255) DEFAULT NULL,
  `ostype_id` int(11) NOT NULL,
  PRIMARY KEY (`device_id`),
  KEY `devices_ostype_id_5574a276_fk_ostype_ostypeid` (`ostype_id`),
  CONSTRAINT `devices_ostype_id_5574a276_fk_ostype_ostypeid` FOREIGN KEY (`ostype_id`) REFERENCES `ostype` (`ostypeid`)
) ENGINE=InnoDB AUTO_INCREMENT=2043 DEFAULT CHARSET=utf8;

#
# Data for table "devices"
#


#
# Structure for table "devices_groups"
#

CREATE TABLE `devices_groups` (
  `devicegroup_id` int(11) NOT NULL AUTO_INCREMENT,
  `device_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`devicegroup_id`),
  KEY `devices_groups_device_id_329c7a71_fk_devices_device_id` (`device_id`),
  KEY `devices_groups_group_id_0cfe7d5f_fk_groups_group_id` (`group_id`),
  CONSTRAINT `devices_groups_device_id_329c7a71_fk_devices_device_id` FOREIGN KEY (`device_id`) REFERENCES `devices` (`device_id`),
  CONSTRAINT `devices_groups_group_id_0cfe7d5f_fk_groups_group_id` FOREIGN KEY (`group_id`) REFERENCES `groups` (`group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2164 DEFAULT CHARSET=utf8;

#
# Data for table "devices_groups"
#


#
# Structure for table "coll_policy_groups"
#

CREATE TABLE `coll_policy_groups` (
  `policy_group_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `desc` varchar(2000) DEFAULT NULL,
  `ostypeid` int(11) NOT NULL,
  PRIMARY KEY (`policy_group_id`),
  KEY `coll_policy_groups_ostypeid_7bf9be7a_fk_ostype_ostypeid` (`ostypeid`),
  CONSTRAINT `coll_policy_groups_ostypeid_7bf9be7a_fk_ostype_ostypeid` FOREIGN KEY (`ostypeid`) REFERENCES `ostype` (`ostypeid`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

#
# Data for table "coll_policy_groups"
#


#
# Structure for table "coll_policy"
#

CREATE TABLE `coll_policy` (
  `coll_policy_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `cli_command` varchar(256) DEFAULT NULL,
  `cli_command_result` longtext,
  `desc` varchar(2000) DEFAULT NULL,
  `policy_type` int(11) DEFAULT NULL,
  `snmp_oid` varchar(256) DEFAULT NULL,
  `history` varchar(255) DEFAULT NULL,
  `value_type` int(11) DEFAULT NULL,
  `ostype_id` int(11) NOT NULL,
  PRIMARY KEY (`coll_policy_id`),
  KEY `coll_policy_ostype_id_009344fd_fk_ostype_ostypeid` (`ostype_id`),
  CONSTRAINT `coll_policy_ostype_id_009344fd_fk_ostype_ostypeid` FOREIGN KEY (`ostype_id`) REFERENCES `ostype` (`ostypeid`)
) ENGINE=InnoDB AUTO_INCREMENT=109 DEFAULT CHARSET=utf8;

#
# Data for table "coll_policy"
#


#
# Structure for table "coll_policy_cli_rule"
#

CREATE TABLE `coll_policy_cli_rule` (
  `ruleid` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(30) DEFAULT NULL,
  `key_str` varchar(30) DEFAULT NULL,
  `mark_string` varchar(256) DEFAULT NULL,
  `split_char` varchar(10) DEFAULT NULL,
  `extract_key` varchar(50) DEFAULT NULL,
  `x_offset` int(11) DEFAULT NULL,
  `y_offset` int(11) DEFAULT NULL,
  `line_nums` int(11) DEFAULT NULL,
  `rule_type` int(11) DEFAULT NULL,
  `end_mark_string` varchar(256) DEFAULT NULL,
  `start_line_num` int(11) DEFAULT NULL,
  `end_line_num` int(11) DEFAULT NULL,
  `desc` varchar(2000) DEFAULT NULL,
  `is_serial` int(11) DEFAULT NULL,
  `is_include` int(11) DEFAULT NULL,
  `command` varchar(256) DEFAULT NULL,
  `value_type` int(11) DEFAULT NULL,
  `coll_policy_id` int(11) NOT NULL,
  PRIMARY KEY (`ruleid`),
  KEY `coll_policy_cli_rule_coll_policy_id_52122139_fk_coll_poli` (`coll_policy_id`),
  CONSTRAINT `coll_policy_cli_rule_coll_policy_id_52122139_fk_coll_poli` FOREIGN KEY (`coll_policy_id`) REFERENCES `coll_policy` (`coll_policy_id`)
) ENGINE=InnoDB AUTO_INCREMENT=278 DEFAULT CHARSET=utf8;

#
# Data for table "coll_policy_cli_rule"
#


#
# Structure for table "coll_policy_rule_tree"
#

CREATE TABLE `coll_policy_rule_tree` (
  `treeid` int(11) NOT NULL AUTO_INCREMENT,
  `parent_tree_id` int(11) DEFAULT NULL,
  `is_leaf` int(11) DEFAULT NULL,
  `level` int(11) DEFAULT NULL,
  `rule_id_path` varchar(2000) DEFAULT NULL,
  `coll_policy_id` int(11) NOT NULL,
  `rule_id` int(11) NOT NULL,
  PRIMARY KEY (`treeid`),
  KEY `coll_policy_rule_tre_coll_policy_id_44a8a286_fk_coll_poli` (`coll_policy_id`),
  KEY `coll_policy_rule_tre_rule_id_83e32d8d_fk_coll_poli` (`rule_id`),
  CONSTRAINT `coll_policy_rule_tre_coll_policy_id_44a8a286_fk_coll_poli` FOREIGN KEY (`coll_policy_id`) REFERENCES `coll_policy` (`coll_policy_id`),
  CONSTRAINT `coll_policy_rule_tre_rule_id_83e32d8d_fk_coll_poli` FOREIGN KEY (`rule_id`) REFERENCES `coll_policy_cli_rule` (`ruleid`)
) ENGINE=InnoDB AUTO_INCREMENT=327 DEFAULT CHARSET=utf8;

#
# Data for table "coll_policy_rule_tree"
#


#
# Structure for table "data_table"
#

CREATE TABLE `data_table` (
  `table_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `descr` varchar(1000) DEFAULT NULL,
  `coll_policy` int(11) NOT NULL,
  `groups` int(11) NOT NULL,
  `tree_id` int(11) DEFAULT NULL,
  `policy_group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`table_id`),
  KEY `fk_data_table_coll_policy` (`coll_policy`),
  KEY `fk_data_table_groups` (`groups`),
  KEY `fk_data_table_coll_policy_rule_tree` (`tree_id`),
  KEY `fk_data_table_policy_group_id` (`policy_group_id`),
  CONSTRAINT `fk_data_table_coll_policy` FOREIGN KEY (`coll_policy`) REFERENCES `coll_policy` (`coll_policy_id`),
  CONSTRAINT `fk_data_table_coll_policy_rule_tree` FOREIGN KEY (`tree_id`) REFERENCES `coll_policy_rule_tree` (`treeid`),
  CONSTRAINT `fk_data_table_groups` FOREIGN KEY (`groups`) REFERENCES `groups` (`group_id`),
  CONSTRAINT `fk_data_table_policy_group_id` FOREIGN KEY (`policy_group_id`) REFERENCES `coll_policy_groups` (`policy_group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

#
# Data for table "data_table"
#


#
# Structure for table "policys_groups"
#

CREATE TABLE `policys_groups` (
  `policys_groups_id` int(11) NOT NULL AUTO_INCREMENT,
  `exec_interval` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `history` varchar(255) DEFAULT NULL,
  `policy_id` int(11) NOT NULL,
  `policy_group_id` int(11) NOT NULL,
  PRIMARY KEY (`policys_groups_id`),
  KEY `policys_groups_policy_id_ae62e30f_fk_coll_policy_coll_policy_id` (`policy_id`),
  KEY `policys_groups_policy_group_id_f8b91a54_fk_coll_poli` (`policy_group_id`),
  CONSTRAINT `policys_groups_policy_group_id_f8b91a54_fk_coll_poli` FOREIGN KEY (`policy_group_id`) REFERENCES `coll_policy_groups` (`policy_group_id`),
  CONSTRAINT `policys_groups_policy_id_ae62e30f_fk_coll_policy_coll_policy_id` FOREIGN KEY (`policy_id`) REFERENCES `coll_policy` (`coll_policy_id`)
) ENGINE=InnoDB AUTO_INCREMENT=96 DEFAULT CHARSET=utf8;

#
# Data for table "policys_groups"
#


#
# Structure for table "schedules"
#

CREATE TABLE `schedules` (
  `schedule_id` int(11) NOT NULL AUTO_INCREMENT,
  `valid_period_type` int(11) DEFAULT NULL,
  `data_schedule_type` int(11) DEFAULT NULL,
  `start_period_time` varchar(255) DEFAULT NULL,
  `end_period_time` varchar(255) DEFAULT NULL,
  `data_schedule_time` varchar(255) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `device_group_id` int(11) NOT NULL,
  `ostype_id` int(11) NOT NULL,
  `policy_group_id` int(11) NOT NULL,
  PRIMARY KEY (`schedule_id`),
  KEY `schedules_device_group_id_55611fe5_fk_groups_group_id` (`device_group_id`),
  KEY `schedules_ostype_id_c6f25217_fk_ostype_ostypeid` (`ostype_id`),
  KEY `schedules_policy_group_id_106f5a98_fk_coll_poli` (`policy_group_id`),
  CONSTRAINT `schedules_device_group_id_55611fe5_fk_groups_group_id` FOREIGN KEY (`device_group_id`) REFERENCES `groups` (`group_id`),
  CONSTRAINT `schedules_ostype_id_c6f25217_fk_ostype_ostypeid` FOREIGN KEY (`ostype_id`) REFERENCES `ostype` (`ostypeid`),
  CONSTRAINT `schedules_policy_group_id_106f5a98_fk_coll_poli` FOREIGN KEY (`policy_group_id`) REFERENCES `coll_policy_groups` (`policy_group_id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8;

#
# Data for table "schedules"
#


#
# Structure for table "items"
#

CREATE TABLE `items` (
  `item_id` int(11) NOT NULL AUTO_INCREMENT,
  `value_type` int(11) DEFAULT NULL,
  `item_type` int(11) DEFAULT NULL,
  `key_str` varchar(30) DEFAULT NULL,
  `status` int(11) DEFAULT '1',
  `last_exec_time` int(11) DEFAULT '1',
  `coll_policy_id` int(11) NOT NULL,
  `coll_policy_rule_tree_treeid` int(11) DEFAULT NULL,
  `device_id` int(11) NOT NULL,
  `schedule_id` int(11) NOT NULL,
  `policys_groups_id` int(11) DEFAULT NULL,
  `enable_status` int(11) NOT NULL,
  `groups_id` int(11) NOT NULL,
  PRIMARY KEY (`item_id`),
  KEY `items_coll_policy_id_5d9e2d3c_fk_coll_policy_coll_policy_id` (`coll_policy_id`),
  KEY `items_coll_policy_rule_tre_c284a62d_fk_coll_poli` (`coll_policy_rule_tree_treeid`),
  KEY `items_device_id_b165d358_fk_devices_device_id` (`device_id`),
  KEY `items_schedule_id_2402dbb2_fk_schedules_schedule_id` (`schedule_id`),
  CONSTRAINT `items_coll_policy_id_5d9e2d3c_fk_coll_policy_coll_policy_id` FOREIGN KEY (`coll_policy_id`) REFERENCES `coll_policy` (`coll_policy_id`),
  CONSTRAINT `items_device_id_b165d358_fk_devices_device_id` FOREIGN KEY (`device_id`) REFERENCES `devices` (`device_id`),
  CONSTRAINT `items_schedule_id_2402dbb2_fk_schedules_schedule_id` FOREIGN KEY (`schedule_id`) REFERENCES `schedules` (`schedule_id`)
) ENGINE=InnoDB AUTO_INCREMENT=41 DEFAULT CHARSET=utf8;

#
# Data for table "items"
#


#
# Structure for table "data_table_history_items"
#

CREATE TABLE `data_table_history_items` (
  `data_table_history_items_id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) NOT NULL,
  `table_id` int(11) NOT NULL,
  PRIMARY KEY (`data_table_history_items_id`),
  KEY `data_table_history_items_item_id_fk_items_item_id` (`item_id`),
  KEY `data_table_history_items_table_id_fk_data_table_table_id` (`table_id`),
  CONSTRAINT `data_table_history_items_item_id_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`),
  CONSTRAINT `data_table_history_items_table_id_fk_data_table_table_id` FOREIGN KEY (`table_id`) REFERENCES `data_table` (`table_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "data_table_history_items"
#


#
# Structure for table "data_table_items"
#

CREATE TABLE `data_table_items` (
  `data_table_items_id` int(11) NOT NULL AUTO_INCREMENT,
  `item_id` int(11) NOT NULL,
  `table_id` int(11) NOT NULL,
  PRIMARY KEY (`data_table_items_id`),
  KEY `data_table_items_item_id_e3b57427_fk_items_item_id` (`item_id`),
  KEY `data_table_items_table_id_f43b161a_fk_data_table_table_id` (`table_id`),
  CONSTRAINT `data_table_items_item_id_e3b57427_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`),
  CONSTRAINT `data_table_items_table_id_f43b161a_fk_data_table_table_id` FOREIGN KEY (`table_id`) REFERENCES `data_table` (`table_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "data_table_items"
#


#
# Structure for table "history_cli_float"
#

CREATE TABLE `history_cli_float` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` double DEFAULT NULL,
  `clock` int(11) DEFAULT NULL,
  `ns` int(11) DEFAULT NULL,
  `block_path` varchar(255) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `history_cli_float_item_id_e4dd4ea2_fk_items_item_id` (`item_id`),
  CONSTRAINT `history_cli_float_item_id_e4dd4ea2_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "history_cli_float"
#


#
# Structure for table "history_cli_int"
#

CREATE TABLE `history_cli_int` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` bigint(20) DEFAULT NULL,
  `clock` int(11) DEFAULT NULL,
  `ns` int(11) DEFAULT NULL,
  `block_path` varchar(255) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `history_cli_int_item_id_803f6c12_fk_items_item_id` (`item_id`),
  CONSTRAINT `history_cli_int_item_id_803f6c12_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "history_cli_int"
#


#
# Structure for table "history_cli_str"
#

CREATE TABLE `history_cli_str` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clock` int(11) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `ns` int(11) DEFAULT NULL,
  `block_path` varchar(255) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `history_cli_str_item_id_6e3a5d1b_fk_items_item_id` (`item_id`),
  CONSTRAINT `history_cli_str_item_id_6e3a5d1b_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "history_cli_str"
#


#
# Structure for table "history_cli_text"
#

CREATE TABLE `history_cli_text` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clock` int(11) DEFAULT NULL,
  `value` longtext,
  `ns` int(11) DEFAULT NULL,
  `block_path` varchar(255) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `history_cli_text_item_id_ae17b56b_fk_items_item_id` (`item_id`),
  CONSTRAINT `history_cli_text_item_id_ae17b56b_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "history_cli_text"
#


#
# Structure for table "history_snmp_float"
#

CREATE TABLE `history_snmp_float` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` double DEFAULT NULL,
  `clock` int(11) DEFAULT NULL,
  `ns` int(11) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `history_snmp_float_item_id_35fc9258_fk_items_item_id` (`item_id`),
  CONSTRAINT `history_snmp_float_item_id_35fc9258_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "history_snmp_float"
#


#
# Structure for table "history_snmp_int"
#

CREATE TABLE `history_snmp_int` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` bigint(20) DEFAULT NULL,
  `clock` int(11) DEFAULT NULL,
  `ns` int(11) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `history_snmp_int_item_id_10b32be3_fk_items_item_id` (`item_id`),
  CONSTRAINT `history_snmp_int_item_id_10b32be3_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "history_snmp_int"
#


#
# Structure for table "history_snmp_str"
#

CREATE TABLE `history_snmp_str` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clock` int(11) DEFAULT NULL,
  `value` varchar(255) DEFAULT NULL,
  `ns` int(11) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `history_snmp_str_item_id_e74802b6_fk_items_item_id` (`item_id`),
  CONSTRAINT `history_snmp_str_item_id_e74802b6_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "history_snmp_str"
#


#
# Structure for table "history_snmp_text"
#

CREATE TABLE `history_snmp_text` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `clock` int(11) DEFAULT NULL,
  `value` longtext,
  `ns` int(11) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `history_snmp_text_item_id_17c301c8_fk_items_item_id` (`item_id`),
  CONSTRAINT `history_snmp_text_item_id_17c301c8_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "history_snmp_text"
#


#
# Structure for table "triggers"
#

CREATE TABLE `triggers` (
  `trigger_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(256) DEFAULT NULL,
  `descr` varchar(1000) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `value` varchar(256) DEFAULT NULL,
  `priority` int(11) DEFAULT NULL,
  `trigger_type` int(11) DEFAULT NULL,
  `trigger_limit_nums` int(11) DEFAULT NULL,
  `condition` int(11) DEFAULT NULL,
  `expression` varchar(256) DEFAULT NULL,
  `columnA` int(11) DEFAULT NULL,
  `columnB` int(11) DEFAULT NULL,
  PRIMARY KEY (`trigger_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "triggers"
#


#
# Structure for table "trigger_detail"
#

CREATE TABLE `trigger_detail` (
  `trigger_detail_id` int(11) NOT NULL AUTO_INCREMENT,
  `expression` varchar(255) DEFAULT NULL,
  `descr` varchar(2000) DEFAULT NULL,
  `status` int(11) DEFAULT NULL,
  `expression_view` varchar(255) DEFAULT NULL,
  `trigger_id` int(11) NOT NULL,
  `device_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`trigger_detail_id`),
  KEY `trigger_detail_trigger_id_7916ab0c_fk_triggers_trigger_id` (`trigger_id`),
  CONSTRAINT `trigger_detail_trigger_id_7916ab0c_fk_triggers_trigger_id` FOREIGN KEY (`trigger_id`) REFERENCES `triggers` (`trigger_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "trigger_detail"
#


#
# Structure for table "functions"
#

CREATE TABLE `functions` (
  `function_id` int(11) NOT NULL AUTO_INCREMENT,
  `function` varchar(12) DEFAULT NULL,
  `parameter` varchar(255) DEFAULT NULL,
  `item_id` int(11) NOT NULL,
  `trigger_detail_id` int(11) NOT NULL,
  PRIMARY KEY (`function_id`),
  KEY `functions_item_id_20030605_fk_items_item_id` (`item_id`),
  KEY `functions_trigger_detail_id_9d19e98e_fk_trigger_d` (`trigger_detail_id`),
  CONSTRAINT `functions_item_id_20030605_fk_items_item_id` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`),
  CONSTRAINT `functions_trigger_detail_id_9d19e98e_fk_trigger_d` FOREIGN KEY (`trigger_detail_id`) REFERENCES `trigger_detail` (`trigger_detail_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "functions"
#


#
# Structure for table "actions"
#

CREATE TABLE `actions` (
  `action_id` int(11) NOT NULL AUTO_INCREMENT,
  `action_type` varchar(2000) DEFAULT NULL,
  `action_name` varchar(256) DEFAULT NULL,
  `snmp_version` varchar(255) DEFAULT NULL,
  `snmp_oid` varchar(255) DEFAULT NULL,
  `community` varchar(255) DEFAULT NULL,
  `ip_address` varchar(256) DEFAULT NULL,
  `username` varchar(30) DEFAULT NULL,
  `password` varchar(30) DEFAULT NULL,
  `command` varchar(1000) DEFAULT NULL,
  `agent_address` varchar(255) DEFAULT NULL,
  `oid` varchar(255) DEFAULT NULL,
  `message` varchar(255) DEFAULT NULL,
  `param` varchar(255) DEFAULT NULL,
  `script_path` varchar(1000) DEFAULT NULL,
  `status` varchar(45) DEFAULT NULL,
  `trigger_id` int(11) NOT NULL,
  PRIMARY KEY (`action_id`),
  KEY `actions_trigger_id_3aa75782_fk_triggers_trigger_id` (`trigger_id`),
  CONSTRAINT `actions_trigger_id_3aa75782_fk_triggers_trigger_id` FOREIGN KEY (`trigger_id`) REFERENCES `triggers` (`trigger_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

#
# Data for table "actions"
#

