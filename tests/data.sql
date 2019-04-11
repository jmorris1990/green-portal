-- Mock Data For Tests
--
INSERT INTO users (email, password, role)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$noRUlTgK$0d1d97ff6ab86c00a3fb9ff626dc2eeabd11c349a47d3c862a5f7db7b8216dfc', 'teacher'), -- password = qwerty
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$ELq3TqsJ$1c60f43f7085a68425e165f27a74c7d7bcc94ce98e604b874e8419f7efefbc06', 'student'); -- password = asdfgh
