from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('assignments', __name__)

@bp.route('/sessions/<int:session_id>/assignments')
@login_required
def assignments(session_id):
    con = db.get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT name, description, total_points, id FROM assignments
        WHERE session_id = %s;
    """,
    (session_id,))

    assignments_list = cur.fetchall()

    cur.close()
    con.close()

    return render_template('assignments.html', assignments_list=assignments_list, role=g.user[3])

@bp.route('/sessions/<int:session_id>/assignments/create', methods=['GET', 'POST'])
@login_required
def create_assignments(session_id):
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    else:
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            total_points = request.form.get('total_points')

            con = db.get_db()
            cur = con.cursor()

            cur.execute(""" 
                SELECT id FROM sessions
                WHERE id = %s
                """,(session_id,))
            
            current_session_id = cur.fetchone()

            if current_session_id == None:
                flash("Session not found, go back to sessions.")
                return render_template('create_assignments.html')

            else:
                cur.execute("""
                INSERT INTO assignments (session_id, name, description, total_points)
                VALUES (%s, %s, %s, %s);
                """,
                (session_id, name, description, total_points))
                 
                con.commit()

                cur.execute("""
                    SELECT id FROM assignments
                    WHERE session_id = %s
                    AND name = %s
                    AND description = %s
                    AND total_points = %s;
                """,
                (session_id, name, description, total_points))

                assignment_id = cur.fetchone()

                cur.execute("""
                    SELECT user_sessions.user_id, assignments.id FROM user_sessions
                    JOIN users ON user_sessions.user_id = users.id
                    JOIN sessions ON user_sessions.session_id = sessions.id
                    JOIN assignments ON sessions.id = assignments.session_id
                    WHERE users.role = 'student'
                    AND user_sessions.session_id = %s
                    AND assignments.id = %s;
                """,
                (session_id, assignment_id))

                students_in_session = cur.fetchall()

                for student in students_in_session:
                    cur.execute("""
                        INSERT INTO submissions (student_id, assignment_id, content, points_earned)
                        VALUES (%s, %s, 'default', 0);
                    """,
                    # grabs the user id and the assignment id from the previous query
                    (student[0], student[1]))

                    con.commit()

                cur.close()
                con.close()

                return redirect(url_for('assignments.assignments', session_id=session_id))
        else:
            return render_template('create_assignments.html')
