import os
from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, current_app
from werkzeug.utils import secure_filename

from . import db
from .auth import login_required

bp = Blueprint('uploads', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if g.user[3] != 'student':
        return make_response("Unauthorized", 401)
    else:

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
                    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                    message = '{} uploaded'.format(filename)
                    flash(message)
                    return redirect(url_for('uploads.upload'))
        return render_template('upload.html')
