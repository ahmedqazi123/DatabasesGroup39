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
)ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `Booking` (
	`booking_id` int NOT NULL AUTO_INCREMENT,
	`date` varchar(255),
	`time` varchar(255) NOT NULL ,
	`member_id`  varchar(255) NOT NULL ,
	`facility_type` varchar(255) NOT NULL ,
	`facility_id` int NOT NULL  ,
	`number_of_people` int NOT NULL ,
    `charges` bigint NOT NULL,
	`status` varchar(255) NOT NULL,

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

CREATE TABLE IF NOT EXISTS `bodMeeting`
(
	`meeting_id` int NOT NULL AUTO_INCREMENT,
	`bod_name` varchar(255) NOT NULL,
	`time` varchar(255) NOT NULL,
	`date` varchar(255) NOT NULL,
	`agenda` varchar(255) NOT NULL,

	PRIMARY KEY (`meeting_id`)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS`Grade` (
	`grade_no` int NOT NULL,
	`amount` bigint NOT NULL,
	`max_loan` bigint NOT NULL,

	PRIMARY KEY (`grade_no`)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `Employee` (
	`employee_id` int NOT NULL AUTO_INCREMENT,
    `password` varchar(255) NOT NULL,
	`name` varchar(255) NOT NULL ,
	`designation` varchar(255) NOT NULL,
	`cnic` varchar(255) NOT NULL,
	`dob` varchar(255) NOT NULL,
	`grade_no` int NOT NULL ,
	`amount_owed` int ,
	`joining_date` varchar(255) NOT NULL ,
	`no_of_leaves` int ,
    `bank_account` varchar(255),
	`quart_report` varchar(255),

	PRIMARY KEY (`employee_id`)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `Finance` (
	`year` int NOT NULL AUTO_INCREMENT,
    `amount` int NOT NULL,
	`funds_available` bigint NOT NULL ,
	`funds_spent` bigint NOT NULL,
	`revenue` bigint NOT NULL,
	`dispersed` bigint NOT NULL,
	`loans_given` int NOT NULL ,
	`loans_due` int ,
	`loan` varchar(255) NOT NULL ,
	`summary` varchar(255) ,

	PRIMARY KEY (`year`)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `Loan`
(
	`loanID` int NOT NULL AUTO_INCREMENT,
	`amount` int NOT NULL,
	`employeeID` int NOT NULL,
	`reason` varchar(255) not NULL,
	`duration` varchar(255) not NULL,
	`status` varchar(255) not NULL,

	PRIMARY KEY (`loanID`)
)ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `Report`
(
	`emp_id` int NOT NULL ,
	`name` varchar(255) NOT NULL,
	`manager` varchar(255) NOT NULL,
	`date` varchar(255) NOT NULL,
	`job_knowledge` int NOT NULL,
	`work_quality` int NOT NULL,
    `attend` int NOT NULL,
    `comm skills`int NOT NULL,
    `initiative` int NOT NULL,

	PRIMARY KEY (`emp_id`)
)ENGINE=InnoDB;

/*to use employee useid,recommended structure,
staff - grade 6 - salary 25000
managers - grade 8 - salary 50000
General manager - grade 12 - salary 100000
Finance Manager - grade 14 - salary 150000
refer to tuple entries below to log in as an employee*/

INSERT INTO `bod` (`bod_id`, `status`, `name`, `username`, `password`, `email`, `cnic`, `dob`) VALUES (1, 'Director', 'Hamd Jalil', 'hamdjalil', 'hamduqazi', '22100083@lums.edu.pk', '35202-6637366-3', '27/05/1999');
INSERT INTO `bod` (`bod_id`, `status`, `name`, `username`, `password`, `email`, `cnic`, `dob`) VALUES (2, 'Director', 'Ahmed Qazi', 'ahmed.r.qazi', 'ahmedqazi', '22100234@lums.edu.pk', '35202-6637366-3', '12/06/1999');
INSERT INTO `bod` (`bod_id`, `status`, `name`, `username`, `password`, `email`, `cnic`, `dob`) VALUES (3, 'CEO', 'Abdullah Saleem', 'abduhere', 'abduqazi', '22100125@lums.edu.pk', '35202-6637366-3', '11/08/1999');

INSERT INTO Employee VALUES(1, 'milkyway1', 'Hamd Bhatti', 'manager', '3410158293466', '1/2/99', 6, 0,'3/4/99',25, 'none', 'none');
INSERT INTO Employee VALUES(2,'abc123', 'Mr.Qazi', 'staff', '3410158293422', '5/6/99', 6, 0,'7/8/99',25, 'none', 'none');
INSERT INTO Employee VALUES(3,'hello123', 'Abdullah Saleem', 'finance', '3410158223452', '11/7/99', 6, 0,'7/8/99',25, 'none', 'none');

INSERT INTO Grade VALUES(6, 25000, 50000);
INSERT INTO Grade VALUES(8, 50000, 100000);
INSERT INTO Grade VALUES(12, 100000, 150000);
INSERT INTO Grade VALUES(14, 150000, 200000);

INSERT INTO Finance VALUES(2020, 1000000, 700000, 100000, 800000, 0, 0, 0,  'nothing',  'nothing');