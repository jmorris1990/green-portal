from flask import Flask, render_template, g, request, redirect, make_response, flash, url_for, send_from_directory
from .auth import login_required

from werkzeug.utils import secure_filename

from . import db
from .auth import login_required
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DB_NAME='portal',
        DB_USER='portal_user',
        UPLOAD_FOLDER=app.instance_path
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    # TODO: Create untracked config.py with random secret key for production
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    

   
    
    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import courses
    app.register_blueprint(courses.bp)

    from . import sessions
    app.register_blueprint(sessions.bp)

    from . import assignments
    app.register_blueprint(assignments.bp)

    from . import submissions
    app.register_blueprint(submissions.bp)

    from . import uploads
    app.register_blueprint(uploads.bp)

    @app.route('/home')
    @login_required
    def home():
        return render_template('home.html')


    return app
