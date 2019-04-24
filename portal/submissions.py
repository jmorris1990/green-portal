from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('submissions', __name__)


@bp.route('<int:assignment_id>/submissions')
@login_required
def view_assignments(assignment_id):
    if g.user != 'teacher':
        return make_response("Unauthorized", 401)
    else:
        con.db.get_db()
        cur = con.cursor()

        cur.execute("""
                    SELECT content, points_earned FROM submissions
                    WHERE assignment_id = %s
                    AND student_id = %s;
                    """,
                    (assignment_id, student_id))

        submission_list = cur.fetchall()

        cur.close()
        con.close()

        return render_template('view_submissions.html', submission_list=submission_list, role=g.user[3])
