-- Mock Data For Tests
--
INSERT INTO users (email, password, role)

VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$CiF5gKcu$7e96aa72c1e2f3394d73e664cf1146640df2ee24e0f1b7a04045a6e22d94b870', 'teacher'), -- password = qwerty
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$xLNvSdNU$b88d9edfe7e4ec954549f9b16ad155cd8a34ffd2d304031e78c429122053d4e7', 'student'); -- password = asdfgh

INSERT INTO courses (name, course_code, description, teacher_id)
VALUES ('Course 1', 'CSET 180', 'Test Course', 1),
       ('Course 2', 'CSET 170', 'Test Course Number 2', 1);

INSERT INTO sessions (course_id, session_name, day, start_time, end_time)
VALUES  (1, 'A', 'MTWRF', '12:00:00', '16:30:00'),
        (1, 'C', 'MWF', '8:00:00', '9:50:00'),
        (2, 'A', 'TWF', '12:00:00', '13:00:00'),
        (2, 'B', 'M', '12:00:00', '15:00:00');

INSERT INTO user_sessions (user_id, session_id)
VALUES (1, 1),
       (1, 2),
       (1, 3),
       (1, 4),
       (2, 1),
       (2, 3);

INSERT INTO assignments (session_id, name, description)
VALUES (1, 'Assignment 1', 'This is assignment 1'),
       (1, 'Assignment 2', 'This is assignment 2');

INSERT INTO submissions (assignment_id, student_id, content)
VALUES (1, 2, 'I wrote this paper by myself. There is nothing here.'),
       (2, 2, 'Yeah.');