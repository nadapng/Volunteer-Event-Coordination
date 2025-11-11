USE `volunteer_app`;

-- Insert sample users
INSERT INTO users (full_name, email, phone, role)
VALUES
('Nada Tester', 'nada@example.com', '2025553333', 'admin'),
('Test Organizer', 'org@example.com', '2025554444', 'organizer'),
('General Volunteer', 'vol@example.com', '2025555555', 'volunteer');

-- Insert sample events
INSERT INTO events (title, description, location, starts_at, ends_at, capacity, created_by)
VALUES
('Cyber Awareness Workshop', 'Cybersecurity event for student volunteers', 'Marymount Hall A', '2025-11-25 09:00:00', '2025-11-25 12:00:00', 40, 1),
('Cloud Security Talk', 'Discussion on AWS IAM risks & controls', 'Library Hall', '2025-12-01 13:00:00', '2025-12-01 16:00:00', 60, 1);

-- Insert sample registrations
INSERT INTO registrations (event_id, user_id, status)
VALUES
(1, 2, 'registered'),
(1, 3, 'registered'),
(2, 3, 'waitlist');

