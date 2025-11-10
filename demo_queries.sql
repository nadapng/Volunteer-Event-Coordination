USE volunteer_app;

-- Show all users
SELECT * FROM users;

-- Show all events
SELECT * FROM events;

-- Simple join example: users registered for events
SELECT 
    r.registration_id,
    u.full_name,
    e.event_title,
    r.registration_date
FROM registrations r
JOIN users u ON r.user_id = u.user_id
JOIN events e ON r.event_id = e.event_id;

-- Update example
UPDATE users SET phone = '+1-555-5555' WHERE user_id = 2;

-- Delete example
DELETE FROM registrations WHERE registration_id = 3;
