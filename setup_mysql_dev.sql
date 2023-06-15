-- prepares a MySQL server for the project

CREATE DATABASE IF NOT EXISTS findmynanny;
CREATE USER IF NOT EXISTS 'fmn_dev'@'localhost' IDENTIFIED BY 'fmn_dev_pwd';
GRANT ALL PRIVILEGES ON `findmynanny`.* TO 'fmn_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'fmn_dev'@'localhost';
FLUSH PRIVILEGES;
