-- Mock Data For Tests
--
INSERT INTO users (email, password, role)
<<<<<<< HEAD
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
=======
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$noRUlTgK$0d1d97ff6ab86c00a3fb9ff626dc2eeabd11c349a47d3c862a5f7db7b8216dfc', 'teacher'), -- password = qwerty
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$ELq3TqsJ$1c60f43f7085a68425e165f27a74c7d7bcc94ce98e604b874e8419f7efefbc06', 'student'); -- password = asdfgh
>>>>>>> master
