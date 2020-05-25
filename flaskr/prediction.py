from flaskr.db import get_db
import pickle
import numpy as np
import os
from sklearn.preprocessing import LabelEncoder

letter_grades = {'A+': 4.1, 'A': 4.0, 'A-': 3.7, 'B+': 3.3, 'B': 3.0, 'B-': 2.7,
                 'C+': 2.3, 'C': 2.0, 'C-': 1.7, 'D+': 1.3, 'D': 1.0, 'D-': 0.5, 'F': 0.0}
le = LabelEncoder()
le.fit(list(letter_grades.keys()))

feature_dept = ['Department Code_CS',
                'Department Code_CTV', 'Department Code_CULT/T',
                'Department Code_ECE/NT', 'Department Code_ECE/T', 'Department Code_EE',
                'Department Code_HIST', 'Department Code_HIST PhD',
                'Department Code_HIST/T', 'Department Code_HUK', 'Department Code_IE',
                'Department Code_ISE/NT', 'Department Code_ISE/T',
                'Department Code_ISS', 'Department Code_ITM', 'Department Code_KHUK/T',
                'Department Code_LIT', 'Department Code_MGT', 'Department Code_MTS/T',
                'Department Code_PHIL', 'Department Code_POLS',
                'Department Code_POLS/NT', 'Department Code_POLS/T',
                'Department Code_PSY', 'Department Code_SOC', 'Department Code_SOC/T',
                'Department Code_ÖHUK/NT', 'Department Code_İHP']

def get_model():
    lower = pickle.load(open(os.getcwd() + '/Smart-Advisor/flaskr/reg_model/gb_model_lower', 'rb'))
    mid = pickle.load(open(os.getcwd() + '/Smart-Advisor/flaskr/reg_model/gb_model_mid', 'rb'))
    upper = pickle.load(open(os.getcwd() + '/Smart-Advisor/flaskr/reg_model/gb_model_upper', 'rb'))
    return lower, mid, upper

def get_gpa(ls):
    numerator = 0
    sum_ = 0
    for grade, count in ls:
        if grade not in letter_grades:
            continue
        numerator += letter_grades[grade] * count
        sum_ += count
    if sum_ == 0:
        return 0
    return numerator / sum_

def get_gpa_change(current_gpa, completed_credit, course_credit, predicted_grade):
    calculated_gpa = (current_gpa * completed_credit + (letter_grades[predicted_grade] * course_credit)) / (completed_credit + course_credit)
    change = calculated_gpa / current_gpa
    change = round(change - 1, 4)
    if change > 0:
        return '+' + str(change)
    elif change < 0:
        return str(change)
    else:
        return str(change)

def get_candidate_courses(subject, department_name, student_google_id):
    db = get_db()
    cursor = db.cursor()
    candidate_courses = []
    for s in subject:
        cursor.execute("SELECT c.course_id, title, cd.course_type, credit, ects, theoritical_credit, practical_credit, course_year, d.department_code "
                        "FROM course AS c, course_department AS cd, department as d "
                        "WHERE c.course_id REGEXP '^{}[[:space:]][0-9]*$' "
                        "AND c.course_id=cd.course_id "
                        "AND cd.department_name = '{}' "
                        "AND d.department_name = cd.department_name "
                        "AND c.course_id NOT IN (SELECT course_id FROM takes WHERE student_google_id = {} AND grade IS NOT NULL);".format(s, department_name, student_google_id))
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
                if lg not in letter_grades:
                    continue
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
    if sum_ == 0:
        return 0
    return numerator / sum_

def get_student_features(student):
    student_features = student.get_details()[3:]
    return student_features

def get_feature_set(student, student_subject_gpa, candidate_courses, avg_grade_subject):
    course_features = {}
    student_features = get_student_features(student)
    gpa = float(student_features[1])
    completed_credit = int(student_features[2])
    for course in candidate_courses:
        course_features.setdefault(course[0], {})
        course_features[course[0]]['title'] = course[1]
        course_features[course[0]]['type'] = course[2]
        course_features[course[0]]['credit'] = course[3]

        res = []
        res.extend([float(student_features[1]), int(student_features[2]), int(student_features[3])])
        res.append(student_subject_gpa[course[0].split()[0]])
        res.append(get_avg_grade_taken(course[0]))
        res.append(avg_grade_subject[course[0].split()[0]])
        res.extend([course[5], course[6], course[3], course[4]])
        course_year = [1 if i+1 == course[7] else 0 for i in range(4)]
        res.extend(course_year)
        department = [1 if feature_dept[i].split('_')[-1] == course[8] else 0 for i in range(len(feature_dept))]
        res.extend(department)
        res.extend([0, 1])
        level = [1 if l == student_features[0] else 0 for l in ['Freshman', 'Junior', 'Senior', 'Sophomore']]
        res.extend(level)
        course_features[course[0]]['feature_set'] = res
    return course_features, gpa, completed_credit

def get_predictions(filter_details, min_grade, student):
    predictions = {}
    lower, mid, upper = get_model()    
    candidate_courses = get_candidate_courses(filter_details, student.get_department(), student.student_google_id)
    gpa_student_subject = get_avg_gpa_student(filter_details, student.student_google_id)
    avg_grade_subject = get_avg_grade_subject(filter_details)
    feature_set, gpa, completed_credit = get_feature_set(student, gpa_student_subject, candidate_courses, avg_grade_subject)

    for course_code in feature_set:
        X = np.array([feature_set[course_code]['feature_set']])
        predicted_grade = le.inverse_transform([round(int(mid.predict(X)[0]))])[0]
        if letter_grades[predicted_grade] < letter_grades[min_grade]:
            continue
        predictions.setdefault(course_code, {})
        predictions[course_code]['title'] = feature_set[course_code]['title']
        predictions[course_code]['type'] = feature_set[course_code]['type']
        predictions[course_code]['credit'] = feature_set[course_code]['credit']        
        predictions[course_code]['prediction'] = predicted_grade
        predictions[course_code]['best'] = le.inverse_transform([round(int(lower.predict(X)[0]))])[0]
        predictions[course_code]['worst'] = le.inverse_transform([round(int(upper.predict(X)[0]))])[0]
        predictions[course_code]['change'] = get_gpa_change(gpa, completed_credit, feature_set[course_code]['credit'], predicted_grade)

    return predictions    
