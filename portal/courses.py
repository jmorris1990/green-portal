from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('courses', __name__)

@bp.route('/courses')
@login_required
def courses():
    con = db.get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT courses.id, courses.name FROM courses 
        JOIN user_courses ON courses.id = user_courses.course_id
        WHERE user_courses.user_id = %s;
    """,
    ([g.user[0]]))

    my_courses = cur.fetchall()

    cur.close()
    con.close()

    return render_template('courses.html', role=g.user[3], courses=my_courses)


@bp.route('/courses/add', methods=['GET', 'POST'])
@login_required
def add_courses():
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    elif g.user[3] == 'teacher':
        if request.method == 'POST':
            name = request.form.get('name')
            code = request.form.get('code')
            class_session = request.form.get('class_session')
            days = request.form.get('days')
            start = request.form.get('start')
            end = request.form.get('end')
            description = request.form.get('description')

            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                INSERT INTO courses (name, course_code, day, start_time, end_time, session, description)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """,
            (name, code, days, start, end, class_session, description))

            con.commit()

            cur.execute("""
                SELECT courses.id FROM courses;
            """)

            new_course = cur.fetchall()[-1]

            cur.execute("""
                INSERT INTO user_courses (user_id, course_id)
                VALUES (%s, %s)
            """,
            (g.user[0], new_course[0]))

            con.commit()

            cur.close()
            con.close()

            return render_template('add_courses.html')
        else:
            return render_template('add_courses.html')
        

@bp.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_courses(id):
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    elif g.user[3] == 'teacher':
        if request.method == 'POST':
            name = request.form['name']
            code = request.form['code']
            class_session = request.form['class_session']
            days = request.form['days']
            start = request.form['start']
            end = request.form['end']
            description = request.form['description']

            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                UPDATE courses
                SET name = %s,
                    course_code = %s,
                    session = %s,
                    day = %s,
                    start_time = %s,
                    end_time = %s,
                    description = %s
                WHERE id = %s;
            """,
            (name, code, class_session, days, start, end, description, id))

            con.commit()

            cur.close()
            con.close()

            return render_template('edit_courses.html', info=(name, code, class_session, days, start, end, description, id))
        
        else:
            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                SELECT name, course_code, session, day, start_time, end_time, description, id FROM courses
                WHERE id = %s;
            """,
            (id,))

            form_info = cur.fetchone()

            cur.close()
            con.close()

            return render_template('edit_courses.html', info=form_info)