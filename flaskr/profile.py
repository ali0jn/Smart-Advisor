import os
import json

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from flaskr.auth import login_required
from flaskr.user import Student, Instructor
from flaskr.testimonials import fetch_testifiers, save_testimony
from flaskr.scrapers.sap_scraper import fetch_transcript
from flaskr.prediction import get_predictions

bp = Blueprint('profile', __name__, url_prefix='/profile')


@bp.route('/')
@login_required
def profile():
    current_user = g.user
    if '@' in current_user[0]:
        return redirect(url_for('profile.instructor_profile'))
    student = Student.get(current_user[0])
    block, radio, label = fetch_testifiers()
    student_number, semester_of_student, advisor, standing, gpa, completed_credits, completed_ects = student.get_details()
    department = student.get_department()
    graduation_progress = 100
    if department != None:
        graduation_progress = student.graduation_progress()
    incompleted_required_courses = student.get_incompleted_required_courses()
    time_table = student.get_timetable()
    return render_template('profile/profile.html', name=student.student_name, email=student.student_email, profile_pic=student.student_profile_picture, testifiers=block, 
                           radio_buttons=radio, labels=label, student_number=student_number, semester_of_student=semester_of_student, advisor=advisor, standing=standing, 
                           gpa=gpa, completed_credits=completed_credits, completed_ects=completed_ects, department=department, graduation_progress=graduation_progress, 
                           time_table=time_table, incompleted_courses=incompleted_required_courses)

@bp.route('/fetch_sap', methods=['POST', 'GET'])
@login_required
def fetch_sap():
    current_user = g.user
    student = Student.get(current_user[0])
    if request.method == 'GET':
        return render_template('profile/fetch_sap.html', name=student.student_name, profile_pic=student.student_profile_picture)
    else:
        email = request.form['email']
        password = request.form['password']
        fetch_transcript(email, password, student)
        return redirect(url_for('profile.profile'))

@bp.route('/predict', methods=['POST', 'GET'])
@login_required
def predict():
    current_user = g.user
    student = Student.get(current_user[0])
    subjects = []
    with open(os.getcwd() + '/Smart-Advisor/flaskr/data/subject_names.txt') as subject_names:
        for subject in subject_names:
            subjects.append(subject.strip())
            
    if request.method == 'GET':
        return render_template('profile/predict.html', name=student.student_name, profile_pic=student.student_profile_picture, subjects=subjects)
    else:
        subject_filters = request.form['subject_filters']
        min_grade = request.form['min-grade']
        predictions = get_predictions(subject_filters.strip().split(), min_grade, student)
        return render_template('profile/predict.html', name=student.student_name, profile_pic=student.student_profile_picture, subjects=subjects)

@bp.route('/rate_instructor', methods=['POST', 'GET'])
@login_required
def rate_instructor():
    current_user = g.user
    student_object = Student.get(current_user[0])
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
        student_object.save_instructor_rating(instructor_email, course_details, semester_year, rating, will_rec, is_suitable, grading, explanation, take_again)

    unrated_instructors = student_object.get_unrated_instructors()
    for i in range(len(unrated_instructors)):
        unrated_instructors[i] = list(unrated_instructors[i])
        unrated_instructors[i][0] = int(unrated_instructors[i][0]) + 1
        if unrated_instructors[i][6] == None:
            unrated_instructors[i][6] = "static/media/users/default.jpg"
    return render_template('profile/rate_instructor.html', name=student_object.student_name, profile_pic=student_object.student_profile_picture, unrated_instructors=unrated_instructors)

@bp.route('/rate_course', methods=['POST', 'GET'])
@login_required
def rate_course():
    current_user = g.user
    student_object = Student.get(current_user[0])
    if request.method == 'POST':
        course_details = request.form['course_details']
        semster_year = request.form['semester_year']
        rating = request.form['rating']
        will_rec = request.form['will_rec']
        did_enjoy = request.form['did_enjoy']
        take_sim = request.form['take_sim']
        good_content = request.form['good_content']
        was_helpful = request.form['was_helpful']
        student_object.save_course_rating(course_details, semster_year, rating, will_rec, did_enjoy, take_sim, good_content, was_helpful)

    unrated_courses = student_object.get_unrated_courses()
    for i in range(len(unrated_courses)):
        unrated_courses[i] = list(unrated_courses[i])
        unrated_courses[i][2] = int(unrated_courses[i][2]) + 1
        unrated_courses[i] = tuple(unrated_courses[i])

    return render_template('profile/rate_course.html', name=student_object.student_name, profile_pic=student_object.student_profile_picture, unrated_courses=unrated_courses)

@bp.route('/testify', methods=['POST', 'GET'])
@login_required
def testify():
    current_user = g.user
    student_object = Student.get(current_user[0])
    if request.method == 'GET':
        return render_template('profile/testimonial.html', name=student_object.student_name, profile_pic=student_object.student_profile_picture)
    else:
        headline = request.form['headline']
        testimony = request.form['testimony']
        save_testimony(testimony, headline, student_object.student_google_id)
        return redirect(url_for('profile.profile'))

@bp.route('/instructor_profile')
@login_required
def instructor_profile():
    current_inst = g.user
    instructor = Instructor(current_inst[1], current_inst[2], current_inst[0], current_inst[3])
    department = instructor.get_department()
    time_table = instructor.get_timetable()
    block, radio, label = fetch_testifiers()
    course_stats, gpa_stats = instructor.get_course_stats()
    return render_template('profile/instructor_profile.html', name=instructor.instructor_name, email=instructor.instructor_email,
                            profile_pic=instructor.instructor_profile_pic, department=department, time_table=time_table, testifiers=block,
                            radio_buttons=radio, labels=label, course_stats=course_stats, gpa_stats=gpa_stats)

@bp.route('/student_progress')
@login_required
def student_progress():
    current_inst = g.user
    instructor = Instructor(current_inst[1], current_inst[2], current_inst[0], current_inst[3])
    department = instructor.get_department()
    advisees = instructor.get_advisees()    
    advisees_details = {}
    for i in range(len(advisees)):
        advisees[i] = list(advisees[i])
        student = Student(advisees[i][0], advisees[i][2], advisees[i][3], advisees[i][4])
        graduation_progress = student.graduation_progress()
        department = student.get_department()
        advisees[i].append(graduation_progress)
        advisees[i].append("width: {}%;".format(graduation_progress))
        completed_courses = student.get_completed_courses()
        incompleted_required_courses = student.get_incompleted_required_courses()
        advisees_details[advisees[i][1]] = {'student_number': advisees[i][1],
                                    'student_name': advisees[i][2],
                                    'student_email': advisees[i][3],
                                    'profile_picture': advisees[i][4],
                                    'student_semester': str(advisees[i][5]),
                                    'standing': advisees[i][6],
                                    'completed_credit': str(advisees[i][7]),
                                    'completed_ects': str(advisees[i][8]),
                                    'gpa': str(advisees[i][9]),
                                    'department': department,
                                    'completed_courses': completed_courses,
                                    'incompleted_required_courses': incompleted_required_courses,
                                    'graduation_progress': str(graduation_progress)}

    return render_template('profile/student_progress.html', name=instructor.instructor_name, profile_pic=instructor.instructor_profile_pic, advisees_details=json.dumps(advisees_details), advisees=advisees)
