-- schema_seed.sql
CREATE DATABASE IF NOT EXISTS volunteer_app
  CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE volunteer_app;

-- USERS
CREATE TABLE IF NOT EXISTS users (
  user_id       INT AUTO_INCREMENT PRIMARY KEY,
  full_name     VARCHAR(120) NOT NULL,
  email         VARCHAR(160) NOT NULL UNIQUE,
  phone         VARCHAR(30),
  role          ENUM('admin','organizer','volunteer') DEFAULT 'volunteer',
  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- EVENTS
CREATE TABLE IF NOT EXISTS events (
  event_id      INT AUTO_INCREMENT PRIMARY KEY,
  title         VARCHAR(150) NOT NULL,
  description   TEXT,
  location      VARCHAR(150),
  starts_at     DATETIME NOT NULL,
  ends_at       DATETIME NOT NULL,
  capacity      INT DEFAULT 0,
  created_by    INT,
  created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (created_by) REFERENCES users(user_id)
    ON DELETE SET NULL ON UPDATE CASCADE
);

-- REGISTRATIONS (junction)
CREATE TABLE IF NOT EXISTS registrations (
  reg_id        INT AUTO_INCREMENT PRIMARY KEY,
  event_id      INT NOT NULL,
  user_id       INT NOT NULL,
  status        ENUM('registered','waitlist','cancelled') DEFAULT 'registered',
  registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uniq_event_user (event_id, user_id),
  FOREIGN KEY (event_id) REFERENCES events(event_id)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

-- SEED
INSERT INTO users (full_name, email, phone, role) VALUES
('Nada Alamri','nada@example.com','+1-555-0101','organizer'),
('Sara Ali','sara@example.com',NULL,'volunteer'),
('Omar Z','omar@example.com',NULL,'volunteer')
ON DUPLICATE KEY UPDATE full_name=VALUES(full_name);

INSERT INTO events (title, description, location, starts_at, ends_at, capacity, created_by) VALUES
('Food Drive', 'Community food collection and sorting', 'Community Center',
 '2025-11-20 10:00:00','2025-11-20 14:00:00',50, 1),
('Park Cleanup', 'Clean-up of Riverside Park', 'Riverside Park',
 '2025-11-22 09:00:00','2025-11-22 12:30:00',30, 1);

INSERT INTO registrations (event_id, user_id, status) VALUES
(1, 2, 'registered'),
(1, 3, 'registered'),
(2, 2, 'waitlist')
ON DUPLICATE KEY UPDATE status=VALUES(status);
