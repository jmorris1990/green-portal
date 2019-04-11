-- Mock Data For Tests
--
INSERT INTO users (email, password, role)
VALUES ('teacher@stevenscollege.edu', 'pbkdf2:sha256:150000$vabLpq6w$1b5021c0313f059dce39833e64ba44eba0dad10bdbd630f942469fc873781bb2', 'teacher'), -- password = qwerty
       ('student@stevenscollege.edu', 'pbkdf2:sha256:150000$ELq3TqsJ$1c60f43f7085a68425e165f27a74c7d7bcc94ce98e604b874e8419f7efefbc06', 'student'); -- password = asdfgh
