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
    day varchar(7) NOT NULL, -- M T W R F S U
    start_time time NOT NULL,
    end_time time NOT NULL,
    session varchar(2),
    description text NOT NULL
);

CREATE TABLE user_courses (
    id bigserial PRIMARY KEY,
    user_id bigint REFERENCES users (id) NOT NULL,
    course_id bigint REFERENCES courses (id) NOT NULL
);