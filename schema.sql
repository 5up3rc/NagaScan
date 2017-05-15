-- init database

drop database if exists nagascan;

create database nagascan;

use nagascan;

DROP TABLE IF EXISTS `users`;
create table users (
    `id` varchar(50) not null,
    `email` varchar(50) not null,
    `password` varchar(50) not null,
    `admin` bool not null,
    `name` varchar(50) not null,
    `image` varchar(500) not null,
    `created_at` real not null,
    unique key `idx_email` (`email`),
    key `idx_created_at` (`created_at`),
    primary key (`id`)
) engine=innodb default charset=utf8;

-- email / password:
-- nagascan@example.com / Naga5c@n

insert into users (`id`, `email`, `password`, `admin`, `name`, `image`, `created_at`) values ('0010018336417540987fff4508f43fbaed718e263442526000', 'nagascan@example.com', '1ab3f265aee6b93afa940aa5325035e2', 1, 'Administrator', 'http://avfisher.win/wp-content/uploads/2015/10/avfisher.jpg', 1402909113.628);

--
-- Table structure for table `requests`
--

DROP TABLE IF EXISTS `requests`;
CREATE TABLE `requests` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `rid` varchar(64) DEFAULT NULL,
  `ip` varchar(40) DEFAULT NULL,
  `port` varchar(40) DEFAULT NULL,
  `protocol` varchar(40) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `method` varchar(40) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `accept` varchar(255) DEFAULT NULL,
  `accept_language` varchar(255) DEFAULT NULL,
  `accept_encoding` varchar(255) DEFAULT NULL,
  `cookie` text DEFAULT NULL,
  `referer` text DEFAULT NULL,
  `content_type` varchar(255) DEFAULT NULL,
  `post_data` text DEFAULT NULL,
  `path` text DEFAULT NULL,
  `scan_xss` int(4) DEFAULT 0,
  `scan_sqli` int(4) DEFAULT 0,
  `scan_fi` int(4) DEFAULT 0,
  `result_xss` varchar(40) DEFAULT 'not scan yet',
  `result_sqli` varchar(40) DEFAULT 'not scan yet',
  `result_fi` varchar(40) DEFAULT 'not scan yet',
  `poc_xss` text DEFAULT NULL,
  `poc_sqli` text DEFAULT NULL,
  `poc_fi` text DEFAULT NULL,
  `time` varchar(255) DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `responses`
--

DROP TABLE IF EXISTS `responses`;
CREATE TABLE `responses` (
  `id` int(32) NOT NULL AUTO_INCREMENT,
  `rid` varchar(64) DEFAULT NULL,
  `response_xss` longtext DEFAULT NULL,
  `response_sqli` longtext DEFAULT NULL,
  `response_fi` longtext DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

--
-- Table structure for table `exclusions_parse`
--

DROP TABLE IF EXISTS `exclusions_parse`;
CREATE TABLE `exclusions_parse` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `exclusion` varchar(255) DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


insert into exclusions_parse (`id`) values (1);

--
-- Table structure for table `exclusions_cookie`
--

DROP TABLE IF EXISTS `exclusions_cookie`;
CREATE TABLE `exclusions_cookie` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `exclusion` text DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


insert into exclusions_cookie (`id`) values (1);

--
-- Table structure for table `exclusions_scan`
--

DROP TABLE IF EXISTS `exclusions_scan`;
CREATE TABLE `exclusions_scan` (
  `id` int(50) NOT NULL AUTO_INCREMENT,
  `type` int(4) DEFAULT NULL, -- 0: scan_xss; 1: scan_sqli; 2: scan_fi
  `ip` varchar(40) DEFAULT NULL,
  `port` varchar(40) DEFAULT NULL,
  `protocol` varchar(40) DEFAULT NULL,
  `host` varchar(255) DEFAULT NULL,
  `method` varchar(40) DEFAULT NULL,
  `user_agent` text DEFAULT NULL,
  `accept` varchar(255) DEFAULT NULL,
  `accept_language` varchar(255) DEFAULT NULL,
  `accept_encoding` varchar(255) DEFAULT NULL,
  `cookie` text DEFAULT NULL,
  `referer` text DEFAULT NULL,
  `content_type` varchar(255) DEFAULT NULL,
  `post_data` text DEFAULT NULL,
  `path` text DEFAULT NULL,
  `update_time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;

insert into exclusions_scan (`id`, `type`) values (1, 0);
insert into exclusions_scan (`id`, `type`) values (2, 1);
insert into exclusions_scan (`id`, `type`) values (3, 2);

  --
  -- Table structure for table `sqlmap`
  --

  DROP TABLE IF EXISTS `sqlmap`;
  CREATE TABLE `sqlmap` (
    `id` varchar(50) not null,
    `ip` varchar(40) DEFAULT NULL,
    `port` varchar(40) DEFAULT NULL,
    `status` int(4) DEFAULT 1, -- 2: not available; 1: available
    `update_time` varchar(255) DEFAULT NULL,
    PRIMARY KEY (`id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;
