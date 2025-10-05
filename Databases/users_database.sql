DROP DATABASE IF EXISTS `users_database`;
CREATE DATABASE `users_database`;
USE `users_database`;


CREATE TABLE users (
user_id INT NOT NULL,
first_name VARCHAR(50) NOT NULL,
last_name VARCHAR(50) NOT NULL,
pin VARCHAR(13) NOT NULL, --Personal Identification Number
phone_number VARCHAR(17) NOT NULL,
email VARCHAR(100) NOT NULL,
user_password VARCHAR(50) NOT NULL
);

CREATE TABLE accounts (
user_id INT NOT NULL,
account_type varchar(20) NOT NULL,
money DECIMAL(15, 2) NOT NULL
);

/*
--Test
INSERT INTO users (user_id, first_name, last_name, pin, email, user_password) 
VALUES 
(1, "asd", "def", "1111111111111", "asd@gmail.com", "asdpass")
*/