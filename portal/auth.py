from functools import wraps
from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint
from werkzeug.security import check_password_hash

from . import db

bp = Blueprint('auth', __name__)

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user') is None:
            return redirect(url_for('auth.index'))

        return view(**kwargs)

    return wrapped_view

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('id')

    if user_id is None:
        g.user = None
    else:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM user WHERE id = %s', (user_id[0],)
        )
        g.user = cursor.fetchone()
        cursor.close()
        conn.close()



@bp.route('/', methods=('GET', 'POST'))
def index():
    print(g.user)
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        #have an error
        error = None
        conn = db.get_db()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM users WHERE email = %s;', (email,)
        )
        # set the user to be only the ID
        user = cursor.fetchone()

        if user is None:
            # throw an error
            error = 'Incorrect email'
            flash(error)
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password'
            flash(error)
        else:
            session.clear()
            session['user'] = user
            cursor.close()
            conn.close()

            return redirect(url_for('home'))

    # if a post has happened i want to go to a new template(view)
    return render_template('index.html')


@bp.route('/logout')
# @login_required
def logout():
    session.clear()
    return redirect(url_for('auth.index'))
