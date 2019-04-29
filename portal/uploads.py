from flask import render_template, flash, session, url_for, redirect, request, g, Blueprint
from werkzeug.utils import secure_filename

from . import db
from .auth import login_required

bp = Blueprint('uploads', __name__)

