import os
from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint, current_app, make_response
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash


from . import db
from .auth import login_required

bp = Blueprint('uploads', __name__)

# prevent relative path traversal exploit eg ../../../malicious.txt
def allowed_file(filename):
    ALLOWED_EXTENSIONS = set(['doc', 'docx', 'pdf', 'txt'])

    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/upload/<int:assignment_id>', methods=['GET', 'POST'])
@login_required
def upload(assignment_id):
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
                    with db.get_db() as con:
                        with con.cursor() as cur:
                            # assignment_data[0] is the submission id, assignment_data[1] is the submission type
                            cur.execute("""
                                SELECT submissions.id, assignments.submission_type FROM assignments
                                JOIN submissions ON assignments.id = submissions.assignment_id
                                WHERE submissions.student_id = %s
                                AND submissions.assignment_id = %s;""",(g.user[0], assignment_id))

                            assignment_data = cur.fetchone()

                    if assignment_data[1] == 'upload':

                        filename = secure_filename(file.filename)

                        message = '{} uploaded'.format(filename)
                        flash(message) # flash the message before appending and hashing so it just returns the filename they uploaded

                        # append the submission id to the filename before the file extension, then hash the filename, then insert that filename into the file field in the submissions table

                        fname, extension = os.path.splitext(filename) # splits filename into its name and extension so the submission id can be inserted before extension on the next line

                        appended_filename = "{fname}{a_id}{extension}".format(fname=fname, a_id=assignment_data[0], extension=extension)

                        hashed_filename = generate_password_hash(appended_filename) # hashes filename to prevent direct object reference

                        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], hashed_filename))

                        with db.get_db() as con:
                            with con.cursor() as cur:
                                cur.execute("""
                                    UPDATE submissions
                                    SET file = %s
                                    WHERE id = %s
                                    """,(filename, assignment_data[0]))

                        return redirect(request.url)

                    else:
                        flash("You cannot upload a file to this submission.")
                        return redirect(request.url)

                if file is not allowed_file(file.filename):

                    flash("That file type is not supported, only upload .doc .docx .pdf. or .txt ")
                    return redirect(request.url)

        return render_template('upload.html')
