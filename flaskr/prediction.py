from flaskr.db import get_db
import pickle
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder

letter_grades = {'A+': 4.1, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.5, 'F': 0.0}
le = LabelEncoder()
le.fit(list(letter_grades.keys()))

def get_model():
    model = pickle.load(open(os.getcwd() + '/Smart-Advisor/flaskr/gb_model', 'rb'))
    return model

def get_gpa(ls):
    numerator = 0
    sum_ = 0
    for grade, count in ls:
        if grade in letter_grades:
            numerator += letter_grades[grade] * count
            sum_ += count
    return numerator / sum_

def get_candidate_courses(subject, department_name):
    db = get_db()
    cursor = db.cursor()
    candidate_courses = []
    for s in subject:
        cursor.execute("SELECT c.course_id, title, cd.course_type, credit, ects, theoritical_credit, practical_credit, course_year "
                        "FROM course AS c, course_department AS cd "
                        "WHERE c.course_id REGEXP '^{}[[:space:]][0-9]*$' "
                        "AND c.course_id=cd.course_id "
                        "AND cd.department_name = '{}';".format(s, department_name))
        candidate_courses += cursor.fetchall()
    return candidate_courses

def get_avg_gpa_student(subject, student_google_id):
    """
    Average GPA of user with the same subject
    """
    db = get_db()
    cursor = db.cursor()
    gpa_dict = {}
    for s in subject:
        cursor.execute("SELECT t.grade, c.credit "
                    "FROM takes AS t, student AS s, course AS c "
                    "WHERE t.student_google_id = s.student_google_id "
                    "AND c.course_id = t.course_id "
                    "AND c.course_id REGEXP '^{}[[:space:]][0-9]*$' "
                    "AND s.student_google_id={} "
                    "AND t.grade IS NOT NULL;".format(s, student_google_id))
        res = cursor.fetchall()
        if cursor != []:
            c = 0
            for lg, cr in res:
                c += letter_grades[lg] * cr
            gpa_dict[s] = c    
    return gpa_dict

def get_avg_grade_subject(subject):
    """
    Average grade of courses with the that subject
    """
    db = get_db()
    cursor = db.cursor()
    average_grades = {}
    for s in subject:
        average_grades.setdefault(s, 0)
        cursor.execute("SELECT grade, count(grade) "
                       "FROM takes "
                       "WHERE course_id REGEXP '^{}[[:space:]][0-9]*$' "
                       "GROUP BY grade;".format(s))
        grade_frequencies = cursor.fetchall()
        if grade_frequencies != []:
            average_grade = get_gpa(grade_frequencies)
            average_grades[s] = average_grade
    return average_grades

def get_avg_grade_taken(course_id):
    """
    Average grade of students who have taken that course so far
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT grade, COUNT(grade) "
                   "FROM takes "
                   "WHERE course_id = '{}' "
                   "GROUP BY grade;".format(course_id))
    grade_frequencies = cursor.fetchall()
    numerator = 0
    sum_ = 0
    for grade, count in grade_frequencies:
        if grade in letter_grades:
            numerator += letter_grades[grade] * count
            sum_ += count
    return numerator / sum_

def get_predictions(filter_details, min_grade, student):
    model = get_model()
    # test = np.array([[3.93, 63, 100, 3.2, 3.0, 2.9, 3, 0, 3, 5, 0, 0, 1, 0, 1, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1]])
    # prediction = round(int(model.predict(test)[0]))
    # print(le.inverse_transform([prediction]))
    
    candidate_courses = get_candidate_courses(filter_details, student.get_department())
    print(candidate_courses)
    gpa_student_subject = get_avg_gpa_student(filter_details, student.student_google_id)
    print(gpa_student_subject)
    avg_grade_subject = get_avg_grade_subject(filter_details)
    print(avg_grade_subject)
    
    