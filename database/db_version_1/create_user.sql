-- create mysql user for application
CREATE USER IF NOT EXISTS 'vol_app_user'@'localhost' IDENTIFIED BY 'Password123!';

GRANT ALL PRIVILEGES ON volunteer_app.* TO 'vol_app_user'@'localhost';

FLUSH PRIVILEGES;
