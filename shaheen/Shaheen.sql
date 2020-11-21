CREATE DATABASE IF NOT EXISTS `shaheen` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;
USE `shaheen`;

CREATE TABLE IF NOT EXISTS `Members` (
	`member_id` int NOT NULL AUTO_INCREMENT,
	`name` varchar(255)  NOT NULL,
    `username` varchar(50)  NOT NULL ,
  	`password` varchar(255) NOT NULL ,
    `email` varchar(100) NOT NULL,
	`cnic` varchar(255)  NOT NULL,
	`dob` varchar(255) NOT NULL,
	`member_since` varchar(255)  NOT NULL,
	`subscription_type` varchar(255) NOT NULL,
	PRIMARY KEY (`member_id`)
)
ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;