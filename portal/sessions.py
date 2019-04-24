from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, make_response

from . import db
from .auth import login_required

bp = Blueprint('sessions', __name__)

@bp.route('/sessions', methods=['GET'])
@login_required
def sessions():
    con = db.get_db()
    cur = con.cursor()

    cur.execute("""
        SELECT courses.name, courses.course_code, sessions.session_name, sessions.day, sessions.start_time, sessions.end_time, sessions.id FROM user_sessions
        JOIN sessions ON user_sessions.session_id = sessions.id
        JOIN courses ON courses.id = sessions.course_id
        WHERE user_sessions.user_id = %s;
    """,
    (g.user[0],))

    sessions_list = cur.fetchall()

    cur.close()
    con.close()

    return render_template('sessions.html', sessions_list=sessions_list)

@bp.route('/sessions/add/', methods=['GET', 'POST'])
@login_required    
def add_session():
    
    if g.user[3] != 'teacher':
        return make_response("Unauthorized", 401)
    elif g.user[3] == 'teacher':
        if request.method == 'POST':
            course_id = None
            
            session_name = request.form.get('session_name')
            day = request.form.get('day')
            start_time = request.form.get('start_time')
            end_time = request.form.get('end_time')


            con = db.get_db()
            cur = con.cursor() 

            cur.execute("""
                INSERT INTO sessions (course_id, session_name, day, start_time, end_time)
                VALUES (%s, %s, %s, %s, %s);
            """,
            (course_id, session_name, day, start_time, end_time))

            con.commit()

            cur.execute("""
                SELECT id FROM sessions
                WHERE course_id = %s AND
                      session_name = %s AND
                      day = %s AND
                      start_time = %s AND
                      end_time = %s;
            """,
            (course_id, session_name, day, start_time, end_time))

            new_session = cur.fetchone()

            cur.execute("""
                INSERT INTO user_sessions (user_id, session_id)
                VALUES (%s, %s);
            """,
            (g.user[0], new_session[0]))

            con.commit()

            cur.close()
            con.close()

            return redirect(url_for('courses.edit_courses', id=course_id))

        else: 
            return render_template('add_session.html')






        


    
    

