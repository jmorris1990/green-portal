from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('submissions', __name__)

@bp.route('/sessions/<int:session_id>/assignments/<int:assignment_id>/submissions/<int:submission_id>/update', methods=['GET', 'POST'])
@login_required
def enter_grade(session_id, assignment_id, submission_id):
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    else:
        if request.method == 'POST':
            grade = request.form.get('grade')

            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                UPDATE submissions
                SET points_earned = %s
                WHERE id = %s;
            """,
            (grade, submission_id))

            con.commit()

            cur.execute("""
                SELECT submissions.content, submissions.points_earned, assignments.total_points, users.email FROM submissions
                JOIN assignments ON submissions.assignment_id = assignments.id
                JOIN users ON submissions.student_id = users.id
                WHERE submissions.id = %s;
            """,
            (submission_id,))

            submission = cur.fetchone()

            cur.close()
            con.close()

            return render_template('grade_submission.html', submission=submission)
        else:
            con = db.get_db()
            cur = con.cursor()

            cur.execute("""
                SELECT submissions.content, submissions.points_earned, assignments.total_points, users.email FROM submissions
                JOIN assignments ON submissions.assignment_id = assignments.id
                JOIN users ON submissions.student_id = users.id
                WHERE submissions.id = %s;
            """,
            (submission_id,))

            submission = cur.fetchone()

            cur.close()
            con.close()

            return render_template('grade_submission.html', submission=submission)

@bp.route('/view_submissions/<int:assignment_id>')
@login_required
def view_assignments(assignment_id):
    if g.user != 'teacher':
        return make_response("Unauthorized", 401)
    else:
        con = db.get_db()
        cur = con.cursor()

        cur.execute("""
            SELECT session_id FROM assignments
            WHERE id = %s;
            """,(assignment_id,))

        session_id = cur.fetchone()

        cur.execute("""
            SELECT user_id FROM user_sessions
            WHERE session_id = %s
            AND role = 'student'; """
            ,(session_id,))

        student_id = cur.fetchall()

        cur.execute("""
            SELECT email FROM users
            WHERE id = %s;
            """)
        student_emails = cur.fetchall()

        cur.execute("""
                    SELECT content, points_earned FROM submissions
                    WHERE assignment_id = %s
                    AND student_id = %s;
                    """,
                    (assignment_id, student_id))

        submission_list = cur.fetchall()
        print(submission_list)

        cur.close()
        con.close()

        return render_template('view_submissions.html', submission_list=submission_list, student_emails=student_emails, role=g.user[3])
