import os
from flask import render_template, flash, url_for, redirect, request, session, g, Blueprint, current_app, make_response
from werkzeug.utils import secure_filename

from . import db
from .auth import login_required

bp = Blueprint('uploads', __name__)

def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['.doc', '.docx', '.pdf', '.txt'])

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(url_for('uploads.upload'))
        file = request.files['file']
        print(request.files)
        print(file.filename)
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('Please select a file to upload.')
            return redirect(url_for('uploads.upload'))
        
        if file and allowed_file(file.filename):
            print("-----------------------------")
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            message = '{} uploaded'.format(filename)
            print("-----------------------------")
            print(message)
            flash(message)
            return redirect(url_for('uploads.upload'))
    else:
        return render_template('upload.html')
