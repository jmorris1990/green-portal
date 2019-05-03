DROP TABLE IF EXISTS users CASCADE;
DROP TABLE IF EXISTS courses CASCADE;
DROP TABLE IF EXISTS user_courses CASCADE;
DROP TABLE IF EXISTS sessions CASCADE;
DROP TABLE IF EXISTS user_sessions CASCADE;
DROP TABLE IF EXISTS assignments CASCADE;
DROP TABLE IF EXISTS submissions CASCADE;



CREATE TABLE users (
    id bigserial PRIMARY KEY,
    email text UNIQUE NOT NULL,
    password text NOT NULL,
    role varchar(7) NOT NULL CHECK (role IN ('teacher', 'student'))
);

CREATE TABLE courses (
    id bigserial PRIMARY KEY,
    name text NOT NULL,
    course_code text NOT NULL,
    description text NOT NULL,
    teacher_id bigint REFERENCES users (id) NOT NULL
);


CREATE TABLE sessions (
    id bigserial PRIMARY KEY,
    course_id bigserial REFERENCES courses (id),
    session_name text,
    day text NOT NULL, -- M T W R F S U
    start_time text NOT NULL,
    end_time text NOT NULL

);

CREATE TABLE user_sessions (
    id bigserial PRIMARY KEY,
    user_id bigint REFERENCES users (id),
    session_id bigint REFERENCES sessions (id)
);

CREATE TABLE assignments (
    id bigserial PRIMARY KEY,
    session_id bigint REFERENCES sessions (id),
    name text,
    description text,
    total_points numeric,
    submission_type varchar(6)
);

CREATE TABLE submissions (
    id bigserial PRIMARY KEY,
    assignment_id bigint REFERENCES assignments (id),
    student_id bigint REFERENCES users (id),
    points_earned numeric,
    file text
);
