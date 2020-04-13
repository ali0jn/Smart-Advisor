from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.user import Student

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/')
@login_required
def profile():
    current_user = g.user
    return render_template('profile/profile.html', name=current_user[2], email=current_user[3], profile_pic=current_user[4])

@bp.route('/rate_instructor')
@login_required
def rate_instructor():
    return render_template('rate_instructor.html')

@bp.route('/fetch_sap', methods=['POST', 'GET'])
@login_required
def fetch_sap():
    if request.method == 'GET':
        return render_template('profile/fetch_sap.html')
    else:
        email = request.form['email']
        password = request.form['password']
        return redirect(url_for('profile.profile'))

