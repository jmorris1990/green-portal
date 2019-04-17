-- Mock Data For Tests
--
INSERT INTO users (email, password, role)

VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$CiF5gKcu$7e96aa72c1e2f3394d73e664cf1146640df2ee24e0f1b7a04045a6e22d94b870', 'teacher'), -- password = qwerty
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$xLNvSdNU$b88d9edfe7e4ec954549f9b16ad155cd8a34ffd2d304031e78c429122053d4e7', 'student'); -- password = asdfgh

INSERT INTO courses (name, course_code, description, teacher_id)
VALUES ('Course 1', 'CSET 180', 'Test Course', 1),
       ('Course 2', 'CSET 170', 'Test Course Number 2', 1);
