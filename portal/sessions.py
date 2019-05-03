from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('sessions', __name__)

# view all sessions associated with the teacher who created them
@bp.route('/sessions', methods=['GET'])
@login_required
def sessions():

    with db.get_db() as con:
        with con.cursor() as cur:

            cur.execute("""
                SELECT courses.name, courses.course_code, sessions.session_name, sessions.day, sessions.start_time, sessions.end_time, sessions.id FROM user_sessions
                JOIN sessions ON user_sessions.session_id = sessions.id
                JOIN courses ON courses.id = sessions.course_id
                WHERE user_sessions.user_id = %s;
            """,
            (g.user[0],))

            sessions_list = cur.fetchall()

            return render_template('sessions.html', sessions_list=sessions_list)

# add a session to any courses the teacher has created
@bp.route('/sessions/add', methods=['GET', 'POST'])
@login_required
def add_session():

    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    else:
        if request.method == 'POST':

            course_id = request.form.get('course_id')
            session_name = request.form.get('session_name')
            day = request.form.get('day')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')

            if course_id == '' or session_name == '' or day == '' or start_time == '' or end_time == '':
                error = 'Please Fill Out All Fields'
                flash(error)

                #fill out the fields with info in the db after the error flashes
                with db.get_db() as con:
                    with con.cursor() as cur:
                        cur.execute("""
                            SELECT id, name FROM courses;
                        """)
                        courses = cur.fetchall()

                        cur.execute("""
                            SELECT id, email FROM users
                            WHERE role = 'student';
                        """)
                        students = cur.fetchall()

                        return render_template('add_session.html', courses=courses, students=students)
            else:
                with db.get_db() as con:
                    with con.cursor() as cur:
                        cur.execute("""
                            SELECT id FROM courses
                            WHERE id = %s
                            """, (course_id,))

                        current_course_id = cur.fetchone()

                if current_course_id == None:
                    flash("You must create a course first.")

                    with db.get_db() as con:
                        with con.cursor() as cur:
                            cur.execute("""
                                SELECT id, name FROM courses;
                            """)
                            courses = cur.fetchall()
                            cur.execute("""
                                SELECT id, email FROM users
                                WHERE role = 'student';
                            """)
                            students = cur.fetchall()

                            return render_template('add_session.html', courses=courses, students=students)
                else:

                    with db.get_db() as con:
                        with con.cursor() as cur:
                            cur.execute("""
                                INSERT INTO sessions (course_id, session_name, day, start_time, end_time)
                                VALUES (%s, %s, %s, %s, %s);
                            """,
                            (course_id, session_name, day, start_time, end_time))

                            cur.execute("""
                                SELECT id FROM sessions
                                WHERE course_id = %s AND
                                    session_name = %s AND
                                    day = %s AND
                                    start_time = %s AND
                                    end_time = %s;
                            """,
                            (course_id, session_name, day, start_time, end_time))
                            new_session = cur.fetchone()

                            cur.execute("""
                                INSERT INTO user_sessions (user_id, session_id)
                                VALUES (%s, %s);
                            """,
                            (g.user[0], new_session[0]))
                            con.commit()
                            copy = request.form.copy()
                            copy.pop('course_id')
                            copy.pop('session_name')
                            copy.pop('day')
                            copy.pop('start_time')
                            copy.pop('end_time')
                            if copy.get('submit'):
                                copy.pop('submit')
                            for entry in copy:
                                cur.execute("""
                                    INSERT INTO user_sessions (user_id, session_id)
                                    VALUES (%s, %s);
                                """,
                                (copy.get(entry), new_session[0]))

                            return redirect(url_for('sessions.sessions', id=course_id))

        else:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        SELECT id, name FROM courses;
                    """)
                    courses = cur.fetchall()

                    cur.execute("""
                        SELECT id, email FROM users
                        WHERE role = 'student';
                    """)
                    students = cur.fetchall()

                    return render_template('add_session.html', courses=courses, students=students)
