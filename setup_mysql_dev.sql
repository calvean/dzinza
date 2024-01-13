-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS dzinza_dev;
CREATE USER IF NOT EXISTS 'dev'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON `dzinza_dev`.* TO 'dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'dev'@'localhost';
FLUSH PRIVILEGES;
