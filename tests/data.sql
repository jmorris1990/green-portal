-- Mock Data For Tests
--
INSERT INTO users (email, password, role)

VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$CiF5gKcu$7e96aa72c1e2f3394d73e664cf1146640df2ee24e0f1b7a04045a6e22d94b870', 'teacher'), -- password = qwerty
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$xLNvSdNU$b88d9edfe7e4ec954549f9b16ad155cd8a34ffd2d304031e78c429122053d4e7', 'student'); -- password = asdfgh

INSERT INTO courses (name, course_code, day, start_time, end_time, session, description)
VALUES ('Course 1', 'CSET 180', 'MTWRF', '12:00:00', '16:30:00', 'A', 'Test Course'),
       ('Course 2', 'CSET 170', 'MWF', '8:00:00', '9:50:00', 'C', 'Test Course Number 2');

INSERT INTO user_courses (user_id, course_id)
VALUES (1, 1),
       (2, 1),
       (1, 2),
       (2, 2);

INSERT INTO sessions (course_id, session_name, day, start_time, end_time)
VALUES  (1, 'A', 'MTWRF', '12:00:00', '16:30:00'),
        (1, 'C', 'MWF', '8:00:00', '9:50:00'),
        (2, 'A', 'TWF', '12:00:00', '13:00:00'),
        (2, 'B', 'M', '12:00:00', '15:00:00');

