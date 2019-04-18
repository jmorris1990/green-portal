DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS user_courses CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS user_sessions CASCADE;


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


CREATE TABLE sessions (
    id bigserial PRIMARY KEY,
    course_id bigserial REFERENCES courses (id),
    session_name varchar(2),
    day varchar(7) NOT NULL, -- M T W R F S U
    start_time time NOT NULL,
    end_time time NOT NULL
    
);

CREATE TABLE user_sessions (
    id bigserial PRIMARY KEY,
    user_id bigint REFERENCES users (id),
    session_id bigint REFERENCES sessions (id)
);