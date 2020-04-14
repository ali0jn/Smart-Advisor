from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.user import Student
from flaskr.testimonials import fetch_testifiers

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/')
@login_required
def profile():
    current_user = g.user
    block, radio, label, total = fetch_testifiers()
    return render_template('profile/profile.html', name=current_user[2], email=current_user[3], profile_pic=current_user[4], testifiers=block, radio_buttons=radio, labels=label, total_testifiers=total)

@bp.route('/rate_instructor')
@login_required
def rate_instructor():
    current_user = g.user
    return render_template('profile/rate_instructor.html', name=current_user[2], profile_pic=current_user[4])


@bp.route('/rate_course')
@login_required
def rate_course():
    current_user = g.user
    return render_template('profile/rate_course.html', name=current_user[2], profile_pic=current_user[4])

@bp.route('/analyze_instructor')
@login_required
def analyze_instructor():
    current_user = g.user
    return render_template('profile/analyze_instructor.html', name=current_user[2], profile_pic=current_user[4])

@bp.route('/analyze_course')
@login_required
def analyze_course():
    current_user = g.user
    return render_template('profile/analyze_course.html', name=current_user[2], profile_pic=current_user[4])

@bp.route('/fetch_sap', methods=['POST', 'GET'])
@login_required
def fetch_sap():
    current_user = g.user
    if request.method == 'GET':
        return render_template('profile/fetch_sap.html', name=current_user[2], profile_pic=current_user[4])
    else:
        email = request.form['email']
        password = request.form['password']
        return redirect(url_for('profile.profile'))

