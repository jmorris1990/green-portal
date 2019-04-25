from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('submissions', __name__)


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
