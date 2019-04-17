DROP TABLE IF EXISTS user_courses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS courses;

CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

CREATE TABLE courses (
    id bigserial PRIMARY KEY,
    name varchar(100) NOT NULL,
    course_code varchar(50) NOT NULL,
    description text NOT NULL,
    teacher_id bigint REFERENCES users (id) NOT NULL
);