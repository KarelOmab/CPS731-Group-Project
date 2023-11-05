/*
 Navicat MySQL Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 100428 (10.4.28-MariaDB)
 Source Host           : localhost:3306
 Source Schema         : CodeChamp-mockup

 Target Server Type    : MySQL
 Target Server Version : 100428 (10.4.28-MariaDB)
 File Encoding         : 65001

 Date: 05/11/2023 15:13:43
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for account
-- ----------------------------
DROP TABLE IF EXISTS `account`;
CREATE TABLE `account` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `usergroup_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_username` (`username`),
  UNIQUE KEY `unique_email` (`email`),
  KEY `fk_usergroup_id` (`usergroup_id`),
  CONSTRAINT `fk_usergroup_id` FOREIGN KEY (`usergroup_id`) REFERENCES `usergroup` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of account
-- ----------------------------
BEGIN;
INSERT INTO `account` (`id`, `created_at`, `is_deleted`, `usergroup_id`, `username`, `password`, `email`) VALUES (1, '2023-10-09 19:21:14', 0, 2, 'karel', '365bdc6ae8c657d005aefebe0e904766c1d7222251738a317671cd0dac96d50d', 'karel@email.com');
INSERT INTO `account` (`id`, `created_at`, `is_deleted`, `usergroup_id`, `username`, `password`, `email`) VALUES (15, '2023-11-01 21:38:24', 0, 3, 'test', '9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08', 'tester@test.com');
INSERT INTO `account` (`id`, `created_at`, `is_deleted`, `usergroup_id`, `username`, `password`, `email`) VALUES (16, '2023-11-03 23:40:15', 0, 3, '1337_C0d3r', '92459cd7842265516df5ffefb5dc99076c6dbc8d10748f0e34fe81392d932b58', 'i_can_haz_cheezburger@mail.com');
COMMIT;

-- ----------------------------
-- Table structure for challenge
-- ----------------------------
DROP TABLE IF EXISTS `challenge`;
CREATE TABLE `challenge` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `account_id` int(11) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `name` varchar(255) NOT NULL,
  `difficulty` enum('Easy','Medium','Hard') NOT NULL,
  `description` text NOT NULL,
  `stub_name` varchar(255) NOT NULL,
  `stub_block` text NOT NULL,
  `time_allowed_sec` double DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_account_id` (`account_id`),
  CONSTRAINT `fk_account_id` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of challenge
-- ----------------------------
BEGIN;
INSERT INTO `challenge` (`id`, `created_at`, `account_id`, `is_deleted`, `name`, `difficulty`, `description`, `stub_name`, `stub_block`, `time_allowed_sec`) VALUES (1, '2023-10-09 19:21:58', 1, 0, 'This and That', 'Easy', 'Write a function named sum that takes two integers as arguments and returns their sum.', 'sum', '# a method that adds two numbers\ndef sum(x, y):\n    #Write your code here', 5);
INSERT INTO `challenge` (`id`, `created_at`, `account_id`, `is_deleted`, `name`, `difficulty`, `description`, `stub_name`, `stub_block`, `time_allowed_sec`) VALUES (2, '2023-10-09 20:03:36', 1, 0, 'Biggest Number', 'Easy', 'Write a function named max_integer that takes a list of integers as an argument and returns the maximum element in the list.', 'max_integer', 'def max_integer(lst):\r\n	# Write your code here', 5);
INSERT INTO `challenge` (`id`, `created_at`, `account_id`, `is_deleted`, `name`, `difficulty`, `description`, `stub_name`, `stub_block`, `time_allowed_sec`) VALUES (3, '2023-10-09 20:12:31', 1, 0, 'The Classic Buzz', 'Medium', 'Write a function named fizz_buzz that takes in an integer n. The function should return a list of strings where:\n- For multiples of three it returns \"Fizz\" instead of the number.\n- For the multiples of five, it returns \"Buzz\" instead of the number.\n- For numbers which are multiples of both three and five, it returns \"FizzBuzz\".\n- For numbers that aren\'t multiples of three or five, it returns the number as a string.', 'fizz_buzz', 'def fizz_buzz(n):\r\n	# Write your code here', 5);
INSERT INTO `challenge` (`id`, `created_at`, `account_id`, `is_deleted`, `name`, `difficulty`, `description`, `stub_name`, `stub_block`, `time_allowed_sec`) VALUES (4, '2023-10-10 16:19:51', 1, 0, 'I Got The Power', 'Easy', 'Write a function named power that takes two integers (a and b) as arguments and returns a to the power of b', 'power', 'def power(a, b):\n    # Write your code here', 3.25);
COMMIT;

-- ----------------------------
-- Table structure for challenge_comment
-- ----------------------------
DROP TABLE IF EXISTS `challenge_comment`;
CREATE TABLE `challenge_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `account_id` int(11) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `challenge_id` int(11) NOT NULL,
  `title` varchar(255) NOT NULL,
  `text` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_account_id2` (`account_id`),
  KEY `fk_challenge_id` (`challenge_id`),
  CONSTRAINT `fk_account_id2` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `fk_challenge_id` FOREIGN KEY (`challenge_id`) REFERENCES `challenge` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of challenge_comment
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for challenge_submission
-- ----------------------------
DROP TABLE IF EXISTS `challenge_submission`;
CREATE TABLE `challenge_submission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `created_at` datetime NOT NULL,
  `challenge_id` int(11) NOT NULL,
  `account_id` int(11) NOT NULL,
  `exec_time` double NOT NULL,
  `exec_chars` int(11) NOT NULL,
  `exec_src` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_account_id3` (`account_id`),
  KEY `fk_challenge_id2` (`challenge_id`),
  CONSTRAINT `fk_account_id3` FOREIGN KEY (`account_id`) REFERENCES `account` (`id`),
  CONSTRAINT `fk_challenge_id2` FOREIGN KEY (`challenge_id`) REFERENCES `challenge` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of challenge_submission
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for challenge_test
-- ----------------------------
DROP TABLE IF EXISTS `challenge_test`;
CREATE TABLE `challenge_test` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `challenge_id` int(11) NOT NULL,
  `is_deleted` tinyint(1) NOT NULL,
  `input` text NOT NULL,
  `output` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of challenge_test
-- ----------------------------
BEGIN;
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (1, 1, 0, '1, 2', '3');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (2, 1, 0, '10, 20', '30');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (3, 1, 0, '15, 35', '50');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (4, 2, 0, '[1, 2, 3, 4, 5]', '5');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (5, 2, 0, '[-5, -4, -3, -2, -1]', '-1');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (6, 2, 0, '[0, -1, 1, -100, 100]', '100');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (7, 3, 0, '5', '[\"1\", \"2\", \"Fizz\", \"4\", \"Buzz\"]');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (8, 3, 0, '15', '[\"1\", \"2\", \"Fizz\", \"4\", \"Buzz\", \"Fizz\", \"7\", \"8\", \"Fizz\", \"Buzz\", \"11\", \"Fizz\", \"13\", \"14\", \"FizzBuzz\"]');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (9, 3, 0, '2', '[\"1\", \"2\"]');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (10, 4, 0, '1, 1', '1');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (11, 4, 0, '5, 2', '25');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (12, 4, 0, '2, 8', '256');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (35, 16, 0, '100, 99', '1');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (36, 16, 0, '1, 5', '-4');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (37, 16, 0, '0, 0', '0');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (38, 16, 1, '-1, -1', '-2');
INSERT INTO `challenge_test` (`id`, `challenge_id`, `is_deleted`, `input`, `output`) VALUES (39, 16, 0, '-1, -1', '0');
COMMIT;

-- ----------------------------
-- Table structure for usergroup
-- ----------------------------
DROP TABLE IF EXISTS `usergroup`;
CREATE TABLE `usergroup` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(25) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- ----------------------------
-- Records of usergroup
-- ----------------------------
BEGIN;
INSERT INTO `usergroup` (`id`, `type`) VALUES (1, 'admin');
INSERT INTO `usergroup` (`id`, `type`) VALUES (2, 'moderator');
INSERT INTO `usergroup` (`id`, `type`) VALUES (3, 'user');
COMMIT;

-- ----------------------------
-- Procedure structure for DeleteAccount
-- ----------------------------
DROP PROCEDURE IF EXISTS `DeleteAccount`;
delimiter ;;
CREATE PROCEDURE `DeleteAccount`(IN in_account_id INT)
BEGIN
    UPDATE account SET is_deleted=1
		WHERE account.id=in_account_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for DeleteChallengeById
-- ----------------------------
DROP PROCEDURE IF EXISTS `DeleteChallengeById`;
delimiter ;;
CREATE PROCEDURE `DeleteChallengeById`(IN in_challenge_id INT)
BEGIN
		UPDATE challenge SET is_deleted=1
		WHERE challenge.id=in_challenge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for DeleteChallengeComment
-- ----------------------------
DROP PROCEDURE IF EXISTS `DeleteChallengeComment`;
delimiter ;;
CREATE PROCEDURE `DeleteChallengeComment`(IN in_comment_id INT)
BEGIN
		UPDATE challenge_comment SET is_deleted=1
		WHERE challenge_comment.id = in_comment_id;
		
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for DeleteChallengeCommentByIdAndChallengeId
-- ----------------------------
DROP PROCEDURE IF EXISTS `DeleteChallengeCommentByIdAndChallengeId`;
delimiter ;;
CREATE PROCEDURE `DeleteChallengeCommentByIdAndChallengeId`(IN in_challenge_comment_id INT,
		IN in_challenge_id INT)
BEGIN
		UPDATE challenge_comment SET is_deleted=1 
		WHERE challenge_comment.id=in_challenge_comment_id AND challenge_comment.challenge_id=in_challenge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for DeleteChallengeTestByIdAndChallengeId
-- ----------------------------
DROP PROCEDURE IF EXISTS `DeleteChallengeTestByIdAndChallengeId`;
delimiter ;;
CREATE PROCEDURE `DeleteChallengeTestByIdAndChallengeId`(IN in_challenge_test_id INT,
		IN in_challenge_id INT)
BEGIN
		UPDATE challenge_test SET is_deleted=1 
		WHERE challenge_test.id=in_challenge_test_id AND challenge_test.challenge_id=in_challenge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetAccountByUsernameAndPassword
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetAccountByUsernameAndPassword`;
delimiter ;;
CREATE PROCEDURE `GetAccountByUsernameAndPassword`(IN in_username varchar(255), IN in_password varchar(255))
BEGIN
  SELECT id, created_at, usergroup_id, username, email FROM account WHERE username=in_username and `password`=in_password and is_deleted=0;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetAllChallenges
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetAllChallenges`;
delimiter ;;
CREATE PROCEDURE `GetAllChallenges`()
BEGIN
  SELECT * FROM challenge WHERE is_deleted=0;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetChallengeById
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetChallengeById`;
delimiter ;;
CREATE PROCEDURE `GetChallengeById`(IN in_id INT)
BEGIN
  SELECT * FROM challenge WHERE is_deleted=0 and id=in_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetChallengeCommentsById
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetChallengeCommentsById`;
delimiter ;;
CREATE PROCEDURE `GetChallengeCommentsById`(IN in_challenge_id INT)
BEGIN
  SELECT cc.*, a.username FROM challenge_comment cc
	JOIN account a ON a.id=cc.account_id
	WHERE cc.is_deleted=0 and cc.challenge_id=in_challenge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetChallengeSubmissionsByIdAndAccountId
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetChallengeSubmissionsByIdAndAccountId`;
delimiter ;;
CREATE PROCEDURE `GetChallengeSubmissionsByIdAndAccountId`(IN in_challenge_id INT,
 IN in_account_id INT)
BEGIN
		SELECT cs.*
    FROM `challenge_submission` cs
    INNER JOIN `challenge` c ON c.`id` = cs.`challenge_id`
    WHERE 
	  c.`id` = in_challenge_id AND
		cs.`account_id` = in_account_id AND 
		c.is_deleted=0;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetChallengeTestsById
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetChallengeTestsById`;
delimiter ;;
CREATE PROCEDURE `GetChallengeTestsById`(IN in_id INT)
BEGIN
  SELECT * FROM challenge_test WHERE is_deleted=0 and challenge_id=in_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetChallengeTestsByIdAndLimit
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetChallengeTestsByIdAndLimit`;
delimiter ;;
CREATE PROCEDURE `GetChallengeTestsByIdAndLimit`(IN in_id INT, IN in_limit INT)
BEGIN
  SELECT * FROM challenge_test WHERE is_deleted=0 and challenge_id=in_id LIMIT in_limit;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetSolvedChallengesByAccountId
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetSolvedChallengesByAccountId`;
delimiter ;;
CREATE PROCEDURE `GetSolvedChallengesByAccountId`(IN in_account_id INT)
BEGIN
		SELECT c.*
    FROM `challenge` c
    INNER JOIN `challenge_submission` cs ON c.`id` = cs.`challenge_id`
    WHERE cs.`account_id` = in_account_id AND c.is_deleted=0;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for GetUnsolvedChallengesByAccountId
-- ----------------------------
DROP PROCEDURE IF EXISTS `GetUnsolvedChallengesByAccountId`;
delimiter ;;
CREATE PROCEDURE `GetUnsolvedChallengesByAccountId`(IN in_account_id INT)
BEGIN
		SELECT c.*
    FROM `challenge` c
    WHERE NOT EXISTS (
        SELECT 1 
        FROM `challenge_submission` cs
        WHERE cs.`challenge_id` = c.`id` AND cs.`account_id` = in_account_id AND c.is_deleted=0
    );
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for InsertAccount
-- ----------------------------
DROP PROCEDURE IF EXISTS `InsertAccount`;
delimiter ;;
CREATE PROCEDURE `InsertAccount`(IN in_usergroup INT,
    IN in_username VARCHAR(255),
    IN in_password VARCHAR(255),
    IN in_email VARCHAR(255))
insertAccount:BEGIN
	DECLARE lv_username_count INT;
	DECLARE lv_email_count INT;
	
	SELECT COUNT(*) INTO lv_username_count FROM account WHERE username = in_username;
	SELECT COUNT(*) INTO lv_email_count FROM account WHERE email = in_email;
	
	IF lv_username_count > 0 THEN
		SELECT 'Username in use' as message; 
		LEAVE insertAccount;
	END IF;
	
	IF lv_email_count > 0 THEN
		SELECT 'Email in use' as message;
		LEAVE insertAccount;
	END IF;
	
	INSERT INTO account(created_at, is_deleted, usergroup_id, username, `password`, email)
	VALUES(NOW(), 0, in_usergroup, in_username, in_password, in_email);
	
	COMMIT;
	
	SELECT 'Success' as message; 
	
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for InsertChallenge
-- ----------------------------
DROP PROCEDURE IF EXISTS `InsertChallenge`;
delimiter ;;
CREATE PROCEDURE `InsertChallenge`(IN in_account_id INT,
    IN in_name VARCHAR(255),
    IN in_difficulty ENUM('Easy', 'Medium', 'Hard'),
    IN in_description TEXT,
    IN in_stub_name VARCHAR(255),
    IN in_stub_block TEXT,
    IN in_time_allowed_sec DOUBLE)
BEGIN
		INSERT INTO challenge(created_at, account_id, is_deleted, name, difficulty, description, stub_name, stub_block, time_allowed_sec)
    VALUES (NOW(), in_account_id, 0, in_name, in_difficulty, in_description, in_stub_name, in_stub_block, in_time_allowed_sec);
		SELECT LAST_INSERT_ID();
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for InsertChallengeComment
-- ----------------------------
DROP PROCEDURE IF EXISTS `InsertChallengeComment`;
delimiter ;;
CREATE PROCEDURE `InsertChallengeComment`(IN in_account_id INT,
		IN in_challenge_id INT,
		IN in_title VARCHAR(255),
		IN in_text TEXT)
BEGIN
		INSERT INTO challenge_comment (created_at, account_id, is_deleted, challenge_id, title, text) 
		VALUES (NOW(), in_account_id, 0, in_challenge_id, in_title, in_text);
		SELECT LAST_INSERT_ID();
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for InsertChallengeSubmission
-- ----------------------------
DROP PROCEDURE IF EXISTS `InsertChallengeSubmission`;
delimiter ;;
CREATE PROCEDURE `InsertChallengeSubmission`(IN in_challenge_id INT,
		IN in_account_id INT,
		IN in_exec_time DOUBLE,
		IN in_exec_chars INT,
		IN in_exec_src TEXT)
BEGIN
		INSERT INTO challenge_submission (created_at, challenge_id, account_id, exec_time, exec_chars, exec_src) 
		VALUES (NOW(), in_challenge_id, in_account_id, in_exec_time, in_exec_chars, in_exec_src);
		SELECT LAST_INSERT_ID();
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for InsertChallengeTest
-- ----------------------------
DROP PROCEDURE IF EXISTS `InsertChallengeTest`;
delimiter ;;
CREATE PROCEDURE `InsertChallengeTest`(IN in_challenge_id INT,
		IN in_input TEXT,
		IN in_output TEXT)
BEGIN
		INSERT INTO challenge_test (challenge_id, is_deleted, input, output) 
		VALUES (in_challenge_id, 0, in_input, in_output);
		SELECT LAST_INSERT_ID();
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateAccount
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateAccount`;
delimiter ;;
CREATE PROCEDURE `UpdateAccount`(IN in_account_id INT,
		IN in_usergroup_id INT,
    IN in_username VARCHAR(255),
    IN in_password VARCHAR(255),
    IN in_email VARCHAR(255))
BEGIN
    UPDATE account SET usergroup_id=in_usergroup_id, username=in_username, password=in_password, email=in_email
		WHERE account.id=in_account_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateChallenge
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateChallenge`;
delimiter ;;
CREATE PROCEDURE `UpdateChallenge`(IN in_challenge_id INT,
    IN in_name VARCHAR(255),
    IN in_difficulty ENUM('Easy', 'Medium', 'Hard'),
    IN in_description TEXT,
    IN in_stub_name VARCHAR(255),
    IN in_stub_block TEXT,
    IN in_time_allowed_sec DOUBLE)
BEGIN
		UPDATE challenge SET name=in_name, difficulty=in_difficulty, description=in_description, stub_name=in_stub_name, stub_block=in_stub_block, time_allowed_sec=in_time_allowed_sec
		WHERE challenge.id=in_challenge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateChallengeComment
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateChallengeComment`;
delimiter ;;
CREATE PROCEDURE `UpdateChallengeComment`(IN in_comment_id INT,
		IN in_account_id INT,
		IN in_challenge_id INT,
		IN in_title VARCHAR(255),
		IN in_text TEXT)
BEGIN
		UPDATE challenge_comment SET title=in_title, text=in_text
		WHERE challenge_comment.id = in_comment_id;
		
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateChallengeDescriptionById
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateChallengeDescriptionById`;
delimiter ;;
CREATE PROCEDURE `UpdateChallengeDescriptionById`(IN in_challenge_id INT,
    IN in_description text)
BEGIN
		UPDATE challenge SET description=in_description
		WHERE challenge.id=in_challenge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateChallengeDifficultyById
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateChallengeDifficultyById`;
delimiter ;;
CREATE PROCEDURE `UpdateChallengeDifficultyById`(IN in_challenge_id INT,
    IN in_difficulty ENUM('Easy', 'Medium', 'Hard'))
BEGIN
		UPDATE challenge SET difficulty=in_difficulty
		WHERE challenge.id=in_challenge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateChallengeNameById
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateChallengeNameById`;
delimiter ;;
CREATE PROCEDURE `UpdateChallengeNameById`(IN in_challenge_id INT,
    IN in_name VARCHAR(255))
BEGIN
		UPDATE challenge SET name=in_name
		WHERE challenge.id=in_challenge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateChallengeStubBlockById
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateChallengeStubBlockById`;
delimiter ;;
CREATE PROCEDURE `UpdateChallengeStubBlockById`(IN in_challenge_id INT,
    IN in_stub_block text)
BEGIN
		UPDATE challenge SET stub_block=in_stub_block
		WHERE challenge.id=in_challenge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateChallengeStubNameById
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateChallengeStubNameById`;
delimiter ;;
CREATE PROCEDURE `UpdateChallengeStubNameById`(IN in_challenge_id INT,
    IN in_stub_name varchar(255))
BEGIN
		UPDATE challenge SET stub_name=in_stub_name
		WHERE challenge.id=in_challenge_id;
END
;;
delimiter ;

-- ----------------------------
-- Procedure structure for UpdateChallengeTest
-- ----------------------------
DROP PROCEDURE IF EXISTS `UpdateChallengeTest`;
delimiter ;;
CREATE PROCEDURE `UpdateChallengeTest`(IN in_challenge_test_id INT,
		IN in_challenge_id INT,
		IN in_input TEXT,
		IN in_output TEXT)
BEGIN
		UPDATE challenge_test SET input=in_input, output=in_output 
		WHERE challenge_test.id=in_challenge_test_id AND challenge_test.challenge_id=in_challenge_id;
END
;;
delimiter ;

SET FOREIGN_KEY_CHECKS = 1;
