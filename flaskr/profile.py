import os

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.user import Student
from flaskr.testimonials import fetch_testifiers, save_testimony
from flaskr.scrapers.sap_scraper import fetch_transcript

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/')
@login_required
def profile():
    current_user = g.user
    block, radio, label = fetch_testifiers()
    student_number, semester_of_student, advisor, standing, gpa, completed_credits, completed_ects, department = Student.get_details(current_user[0])
    graduation_progress = 100
    if department != None:
        graduation_progress = Student.graduation_progress(department, current_user[0])
    time_table = Student.get_user_timetable(current_user[0])
    return render_template('profile/profile.html', name=current_user[2], email=current_user[3], profile_pic=current_user[4], testifiers=block, radio_buttons=radio, labels=label,
                           student_number=student_number, semester_of_student=semester_of_student, advisor=advisor, standing=standing, gpa=gpa, completed_credits=completed_credits,
                           completed_ects=completed_ects, department=department, graduation_progress=graduation_progress, time_table=time_table)

@bp.route('/fetch_sap', methods=['POST', 'GET'])
@login_required
def fetch_sap():
    current_user = g.user
    if request.method == 'GET':
        return render_template('profile/fetch_sap.html', name=current_user[2], profile_pic=current_user[4])
    else:
        email = request.form['email']
        password = request.form['password']
        fetch_transcript(email, password, current_user[0])
        return redirect(url_for('profile.profile'))

@bp.route('/predict', methods=['POST', 'GET'])
@login_required
def predict():
    current_user = g.user
    subjects = []
    with open(os.getcwd() + '/Smart-Advisor/flaskr/data/subject_names.txt') as subject_names:
        for subject in subject_names:
            subjects.append(subject.strip())
            
    if request.method == 'GET':
        return render_template('profile/predict.html', name=current_user[2], profile_pic=current_user[4], subjects=subjects)
    else:
        selected_subjects = request.get_json()
        prediction_data = []
        if selected_subjects != None:
            for subject in selected_subjects:
                prediction_data.append(subject)
        if prediction_data != []:
            pass
        
        return render_template('profile/predict.html', name=current_user[2], profile_pic=current_user[4], subjects=subjects)

@bp.route('/rate_instructor', methods=['POST', 'GET'])
@login_required
def rate_instructor():
    current_user = g.user
    if request.method == 'POST':
        instructor_email = request.form['instructor_email_form']
        course_details = request.form['course_details']
        semester_year = request.form['semester_year']
        rating = request.form['rating']
        will_rec = request.form['will_rec']
        is_suitable = request.form['is_suitable']
        grading = request.form['grading_policy']
        explanation = request.form['explanation']
        take_again = request.form['take_again']
        Student.save_instructor_rating(instructor_email, course_details, semester_year, rating, will_rec, is_suitable, grading, explanation, take_again, current_user[0])

    unrated_instructors = Student.get_unrated_instructors(current_user[0])
    for i in range(len(unrated_instructors)):
        unrated_instructors[i] = list(unrated_instructors[i])
        unrated_instructors[i][0] = int(unrated_instructors[i][0]) + 1
        if unrated_instructors[i][6] == None:
            unrated_instructors[i][6] = "static/media/users/default.jpg"
    return render_template('profile/rate_instructor.html', name=current_user[2], profile_pic=current_user[4], unrated_instructors=unrated_instructors)

@bp.route('/rate_course', methods=['POST', 'GET'])
@login_required
def rate_course():
    current_user = g.user
    if request.method == 'POST':
        course_details = request.form['course_details']
        semster_year = request.form['semester_year']
        rating = request.form['rating']
        will_rec = request.form['will_rec']
        did_enjoy = request.form['did_enjoy']
        take_sim = request.form['take_sim']
        good_content = request.form['good_content']
        was_helpful = request.form['was_helpful']
        Student.save_course_rating(course_details, semster_year, rating, will_rec, did_enjoy, take_sim, good_content, was_helpful, current_user[0])

    unrated_courses = Student.get_unrated_courses(current_user[0])
    for i in range(len(unrated_courses)):
        unrated_courses[i] = list(unrated_courses[i])
        unrated_courses[i][2] = int(unrated_courses[i][2]) + 1
        unrated_courses[i] = tuple(unrated_courses[i])

    return render_template('profile/rate_course.html', name=current_user[2], profile_pic=current_user[4], unrated_courses=unrated_courses)

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
