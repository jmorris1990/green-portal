from flask import Flask, render_template, g, request, redirect, flash, url_for, send_from_directory
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
        UPLOAD_FOLDER = os.path.join(app.instance_path, './uploaded_submissions'),
    )


    # TODO: Create untracked config.py with random secret key for production
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)
    

    def allowed_file(filename):
        ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
                # check if the post request has the file part
                if 'file' not in request.files:
                    flash('No file part')
                    return redirect(request.url)
                file = request.files['file']
                # if user does not select file, browser also
                # submit an empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return redirect(request.url)
                if file and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return redirect(url_for('upload'))
        return render_template('upload.html')

    
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
