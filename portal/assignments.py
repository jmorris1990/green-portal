from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('assignments', __name__)

# get all assignments that are associated with the session id parameter in the route
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

# create a new assignment associated with the session id parameter 
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


            # check the session_id in the route param vs the database
            cur.execute(""" 
                SELECT id FROM sessions
                WHERE id = %s
                """,(session_id,))
            
            current_session_id = cur.fetchone()
            # error handling if session_id in the route is not in db 
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

                cur.close()
                con.close()

                return redirect(url_for('assignments.assignments', session_id=session_id))
        else:
            return render_template('create_assignments.html')
