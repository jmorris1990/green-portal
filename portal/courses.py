from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('courses', __name__)

@bp.route('/courses')
@login_required
def courses():
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    else:
        con = db.get_db()
        cur = con.cursor()

        cur.execute("""
            SELECT id, name FROM courses
            WHERE teacher_id = %s;
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
    else:
        if request.method == 'POST':
            name = request.form.get('name')
            print(name)
            code = request.form.get('code')
            description = request.form.get('description')

            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                INSERT INTO courses (name, course_code, description, teacher_id)
                VALUES (%s, %s, %s, %s);
            """,
            (name, code, description, g.user[0]))

            con.commit()

            return redirect(url_for('courses.courses'))
        else:
            return render_template('add_courses.html')


@bp.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_courses(id):
    con = db.get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT id FROM courses
        WHERE teacher_id = %s;
    """,
    (g.user[0],))

    teacher_courses = cur.fetchall()

    if g.user[3] != 'teacher' or id in teacher_courses:
        return make_response("Unauthorized", 401)
    else:
        if request.method == 'POST':
            name = request.form['name']
            code = request.form['code']
            description = request.form['description']

            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                UPDATE courses
                SET name = %s,
                    course_code = %s,
                    description = %s
                WHERE id = %s;
            """,
            (name, code, description, id))

            con.commit()

            cur.close()
            con.close()

            return redirect(url_for('courses.courses'))

        else:
            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                SELECT name, course_code, description, id FROM courses
                WHERE id = %s;
            """,
            (id,))

            form_info = cur.fetchone()

            cur.close()
            con.close()



            return render_template('edit_courses.html', info=form_info)
