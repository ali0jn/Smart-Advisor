from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.user import Student
from flaskr.testimonials import fetch_testifiers, save_testimony
from flaskr.scrapers.sap_scraper import fetch_sap_data

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/')
@login_required
def profile():
    current_user = g.user
    block, radio, label = fetch_testifiers()
    return render_template('profile/profile.html', name=current_user[2], email=current_user[3], profile_pic=current_user[4], testifiers=block, radio_buttons=radio, labels=label)

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
        fetch_sap_data(email, password, current_user[0])
        return redirect(url_for('profile.profile'))

@bp.route('/testify', methods=['POST', 'GET'])
@login_required
def testify():
    current_user = g.user
    if request.method == 'GET':
        return render_template('profile/testimonial.html', name=current_user[2], profile_pic=current_user[4])
    else:
        headline = request.form['headline']
        testimony = request.form['testimony']
        save_testimony(testimony, headline, current_user[0])
        return redirect(url_for('profile.profile'))


@bp.route('/handle_rating', methods=['POST', 'GET'])
@login_required
def handle_rating():
    return redirect(url_for('profile.profile'))
