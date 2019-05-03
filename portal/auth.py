from functools import wraps
from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint
from werkzeug.security import check_password_hash

from . import db

bp = Blueprint('auth', __name__)
# force redirect to login page if user isnt logged in
def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.index'))

        return view(**kwargs)

    return wrapped_view
# load the user id into the global namespace
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute(
                    'SELECT * FROM users WHERE id = %s', (user_id,)
                )
                g.user = cur.fetchone()

# login page
@bp.route('/', methods=('GET', 'POST'))
def index():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']
        #have an error
        error = None
        with db.get_db() as con:
            with con.cursor() as cur:
                cur.execute(
                    'SELECT * FROM users WHERE email = %s;', (email,)
                )
                user = cur.fetchone()

        if user is None:
            # throw an error
            error = 'Incorrect email'
            flash(error)
        elif not check_password_hash(user[2], password):
            error = 'Incorrect password'
            flash(error)
        else:
            # clear existing session and set to logged in user id
            session.clear()
            session['user_id'] = user[0]

            return redirect(url_for('home'))

    # if a post has happened i want to go to a new template(view)
    return render_template('index.html')


@bp.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('auth.index'))
