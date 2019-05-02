from flask import render_template, flash, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('submissions', __name__)

# enter new grades into submissions associated to the submission_id route param
@bp.route('/sessions/<int:session_id>/assignments/<int:assignment_id>/submissions/<int:submission_id>/update', methods=['GET', 'POST'])
@login_required
def enter_grade(session_id, assignment_id, submission_id):
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    else:
        if request.method == 'POST':
            grade = request.form.get('grade')
            error = None

            if grade == '':
                error = 'You Have Not Entered A Grade'
                flash(error)

                with db.get_db() as con:
                    with con.cursor() as cur:
                        cur.execute("""
                            SELECT submissions.points_earned, assignments.total_points, users.email FROM submissions
                            JOIN assignments ON submissions.assignment_id = assignments.id
                            JOIN users ON submissions.student_id = users.id
                            WHERE submissions.id = %s;
                        """,
                        (submission_id,))

                        submission = cur.fetchone()

                        return render_template('grade_submission.html', submission=submission)

            else:
                with db.get_db() as con:
                    with con.cursor() as cur:
                        cur.execute("""
                            UPDATE submissions
                            SET points_earned = %s
                            WHERE id = %s;
                        """,
                        (grade, submission_id))

                        cur.execute("""
                            SELECT submissions.points_earned, assignments.total_points, users.email FROM submissions
                            JOIN assignments ON submissions.assignment_id = assignments.id
                            JOIN users ON submissions.student_id = users.id
                            WHERE submissions.id = %s;
                        """,
                        (submission_id,))
                        submission = cur.fetchone()

                        return redirect(url_for('submissions.submissions', session_id=session_id, assignment_id=assignment_id))
        # GET request
        else:
            with db.get_db() as con:
                with con.cursor() as cur:
                    cur.execute("""
                        SELECT submissions.points_earned, assignments.total_points, users.email FROM submissions
                        JOIN assignments ON submissions.assignment_id = assignments.id
                        JOIN users ON submissions.student_id = users.id
                        WHERE submissions.id = %s;
                    """,
                    (submission_id,))

                    submission = cur.fetchone()

                    return render_template('grade_submission.html', submission=submission)

# view all submissions for assignment given by the assignment_id route param
@bp.route('/sessions/<int:session_id>/assignments/<int:assignment_id>/submissions')
@login_required
def submissions(session_id, assignment_id):
    if g.user[3] == 'student':
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT submissions.points_earned, users.email, submissions.id FROM submissions
                JOIN users ON submissions.student_id = users.id
                WHERE submissions.assignment_id = %s;
                """, (assignment_id,))

                submission_list = cur.fetchall()

                return render_template('view_submissions.html', submission_list=submission_list, session_id=session_id)
    else:
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute("""
                SELECT submissions.points_earned, users.email, submissions.id FROM submissions
                JOIN users ON submissions.student_id = users.id
                WHERE submissions.assignment_id = %s;
                """, (assignment_id,))

                submission_list = cur.fetchall()

                return render_template('view_submissions.html', submission_list=submission_list, session_id=session_id)
