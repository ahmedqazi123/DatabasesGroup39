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
    `amount` int NOT NULL,

	PRIMARY KEY (`member_id`)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `Booking` (
	`booking_id` int NOT NULL AUTO_INCREMENT,
	`date` varchar(255)  ,
	`time` varchar(255) NOT NULL ,
	`member_id`  varchar(255) NOT NULL ,
	`facility_type` varchar(255) NOT NULL ,
	`facility_id` int NOT NULL  ,
	`number_of_people` int NOT NULL ,
    `charges` bigint NOT NULL,

	PRIMARY KEY (`booking_id`)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `Receipt` (
	`reciept_no` int NOT NULL AUTO_INCREMENT,
	`member_id` int NOT NULL ,
	`purpose` varchar(255) NOT NULL,
	`amount` int NOT NULL ,
	`date` varchar(255) NOT NULL ,

	PRIMARY KEY (`reciept_no`)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `bod`
(
	`bod_id` int NOT NULL AUTO_INCREMENT,
	`status` varchar(255) NOT NULL,
	`name` varchar(255) NOT NULL,
	`username` varchar(255) NOT NULL,
	`password` varchar(255) NOT NULL,
	`email` varchar(255) NOT NULL,
	`cnic` varchar(255) NOT NULL,
	`dob` varchar(255) NOT NULL,

	PRIMARY KEY (`bod_id`)
)ENGINE=InnoDB;
INSERT INTO `bod` (`bod_id`, `status`, `name`, `username`, `password`, `email`, `cnic`, `dob`) VALUES (1, 'Director', 'Hamd Jalil', 'hamdjalil', 'hamduqazi', '22100083@lums.edu.pk', '35202-6637366-3', '27/05/1999');
INSERT INTO `bod` (`bod_id`, `status`, `name`, `username`, `password`, `email`, `cnic`, `dob`) VALUES (2, 'Director', 'Ahmed Qazi', 'ahmed.r.qazi', 'ahmedqazi', '22100234@lums.edu.pk', '35202-6637366-3', '12/06/1999');
INSERT INTO `bod` (`bod_id`, `status`, `name`, `username`, `password`, `email`, `cnic`, `dob`) VALUES (3, 'CEO', 'Abdullah Saleem', 'abduhere', 'abduqazi', '22100125@lums.edu.pk', '35202-6637366-3', '11/08/1999');


CREATE TABLE IF NOT EXISTS `bodMeeting`
(
	`meeting_id` int NOT NULL AUTO_INCREMENT,
	`bod_name` varchar(255) NOT NULL,
	`time` varchar(255) NOT NULL,
	`date` varchar(255) NOT NULL,
	`agenda` varchar(255) NOT NULL,

	PRIMARY KEY (`meeting_id`)
)ENGINE=InnoDB;