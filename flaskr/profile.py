from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.user import Student

bp = Blueprint('profile', __name__)


@bp.route('/<current_user>/profile')
@login_required
def profile(current_user):
    current_user = Student.get(current_user)
    return render_template('profile/profile.html', name=current_user.student_name, email=current_user.student_email, profile_pic=current_user.google_profile_pic)

@bp.route('/rate_instructor')
@login_required
def rate_instructor():
    return render_template('rate_instructor.html')

@bp.route('/fetch_sap', methods=['POST', 'GET'])
@login_required
def fetch_sap():
    if request.method == 'GET':
        return render_template('fetch_sap.html')
    else:
        email = request.form['email']
        password = request.form['password']
        return redirect(url_for('profile'))

