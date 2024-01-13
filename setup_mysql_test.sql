-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS dzinza_test;
CREATE USER IF NOT EXISTS 'test'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON `dzinza_test`.* TO 'test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'test'@'localhost';
FLUSH PRIVILEGES;
