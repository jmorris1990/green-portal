from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('sessions', __name__)

@bp.route('/sessions/add/<int:course_id>', methods=['GET', 'POST'])
@login_required
def add_session(course_id):
    
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    elif g.user[3] == 'teacher':
        if request.method == 'POST':

            session_name = request.form.get('session_name')
            day = request.form.get('day')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')


            con = db.get_db()
            cur = con.cursor() 

            cur.execute("""
                INSERT INTO sessions (course_id, session_name, day, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s)
            """,
            (course_id, session_name, day, start_time, end_time))

            con.commit()

            cur.close()
            con.close()

            return redirect(url_for('courses.edit_courses', id=course_id))

        else: 
            return render_template('add_session.html')
        


    
    

