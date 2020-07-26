from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('courses', __name__)

# display all courses created by the teacher who is logged in
@bp.route('/courses')
@login_required
def courses():
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    else:
        with db.get_db() as con:
            with con.cursor() as cur:
                # get the name of courses to display them in the template
                cur.execute("""
                    SELECT id, name FROM courses
                    WHERE teacher_id = %s;
                """,
                ([g.user[0]]))

                my_courses = cur.fetchall()

                return render_template('courses.html', courses=my_courses)

# add a new course associated with the logged in teacher
@bp.route('/courses/add', methods=['GET', 'POST'])
@login_required
def add_courses():
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    else:
        if request.method == 'POST':
            name = request.form.get('name')
            code = request.form.get('code')
            description = request.form.get('description')

            if name == '' or code == '' or description == '':
                error = 'Please Fill Out All Fields'
                flash(error)
                return render_template('add_courses.html')

            else:
                with db.get_db() as con:
                    with con.cursor() as cur:
                        cur.execute("""
                            INSERT INTO courses (name, course_code, description, teacher_id)
                            VALUES (%s, %s, %s, %s);
                        """,
                        (name, code, description, g.user[0]))

                        return redirect(url_for('courses.courses'))
        else:
            return render_template('add_courses.html')

# edit a course
@bp.route('/courses/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_courses(id):

    with db.get_db() as con:
        with con.cursor() as cur:
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

            

            with db.get_db() as con:
                with con.cursor() as cur:

                    cur.execute("""
                        UPDATE courses
                        SET name = %s,
                            course_code = %s,
                            description = %s
                        WHERE id = %s;
                    """,
                    (name, code, description, id))

            return redirect(url_for('courses.courses'))

        else:
            with db.get_db() as con:
                with con.cursor() as cur:


                    cur.execute("""
                        SELECT name, course_code, description, id FROM courses
                        WHERE id = %s;
                    """,
                    (id,))

                    form_info = cur.fetchone()

            return render_template('edit_courses.html', info=form_info)
