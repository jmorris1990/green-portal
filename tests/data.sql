-- Mock Data For Tests
--
INSERT INTO users (email, password, role)

VALUES ('teacher@stevenscollege.edu', 'qwerty', 'teacher'), -- password = qwerty
       ('student@stevenscollege.edu', 'asdfgh', 'student'); -- password = asdfgh

INSERT INTO courses (name, course_code, day, start_time, end_time, session, description)
VALUES ('Course 1', 'CSET 180', 'MTWRF', '12:00:00', '16:30:00', 'A', 'Test Course'),
       ('Course 2', 'CSET 170', 'MWF', '8:00:00', '9:50:00', 'C', 'Test Course Number 2');

INSERT INTO user_courses (user_id, course_id)
VALUES (1, 1),
       (2, 1),
       (1, 2),
       (2, 2);
