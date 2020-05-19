from flask_login import UserMixin
from flaskr.db import get_db
import mysql.connector
import datetime
import random

course_department = {'Computer Science and Engineering (English)': {'Core Course Elective': 5,
                                                                    'General Elective': 3,
                                                                    'Department Elective': 4}}

class Student(UserMixin):
    def __init__(self, id_, name, email, profile_pic):
        self.id = id_
        self.student_name = name
        self.student_email = email
        self.google_profile_pic = profile_pic

    @staticmethod
    def get(std_google_id):
        db = get_db()
        cursor = db.cursor()
        std = cursor.execute("SELECT * FROM student WHERE student_google_id = {};".format(std_google_id))
        std = cursor.fetchall()

        if std == []:
            return None

        std = std[0]
        std = Student(
            id_=std[0], name=std[2], email=std[3], profile_pic=std[4]
        )
        return std

    @staticmethod
    def create(id_, name, email, profile_pic):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO student (student_google_id, student_name, student_email, student_profile_picture) "
                       "VALUES(%s, %s, %s, %s);", (id_, name, email, profile_pic))
        db.commit()

    @staticmethod
    def update_profile(student_number, student_semester, advisor, standing, gpa, completed_credits, completed_ects, std_google_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE student "
                       "SET student_id = %s, student_semester = %s, advisor = (select instructor_email from instructor where instructor_name = %s), standing = %s, gpa = %s, completed_credits = %s, completed_ects = %s "
                       "WHERE student_google_id = %s;", (student_number, int(student_semester), advisor, standing, float(gpa), int(completed_credits), int(completed_ects), std_google_id))
        db.commit()

    @staticmethod
    def get_details(std_google_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT student_id, student_semester, (SELECT instructor_name FROM instructor WHERE instructor_email = advisor), standing, gpa, completed_credits, completed_ects "
                       "FROM student "
                       "WHERE student_google_id = {};".format(std_google_id))
        details = cursor.fetchall()[0]
        cursor.execute("SELECT department_name FROM student_department WHERE enrolled_type = 'Main Prg' AND student_google_id = {};".format(std_google_id))
        cursor = cursor.fetchall()
        if cursor == []:
            dept = None
        else:        
            dept = cursor[0][0]
        return details[0], details[1], details[2], details[3], details[4], details[5], details[6], dept

    @staticmethod
    def graduation_progress(department_name, std_google_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) "
                       "FROM course_department "
                       "WHERE course_type='Required' AND department_name = '{}';".format(department_name))
        total_required = int(cursor.fetchall()[0][0])
        extras = sum(list(course_department[department_name].values()))
        cursor.execute("SELECT COUNT(*) "
                       "FROM takes "
                       "WHERE student_google_id = {} AND grade IS NOT NULL AND grade NOT IN ('F', 'IA');".format(std_google_id))
        total_taken = int(cursor.fetchall()[0][0])
        return int((total_taken / (total_required + extras) * 100))

    @staticmethod
    def add_department(dept_dict, std_google_id):
        db = get_db()
        cursor = db.cursor()
        for enrolment_type in dept_dict:
            try:
                cursor.execute("INSERT INTO student_department "
                               "VALUES (%s, %s, %s); ", (std_google_id, dept_dict[enrolment_type], enrolment_type))
            except mysql.connector.errors.IntegrityError:
                pass
        db.commit()

    @staticmethod
    def add_transcript(section_id, semester, section_year, course_id, std_google_id, grade):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT semester, section_year, course_id, student_google_id "
                           "FROM takes "
                           "WHERE student_google_id = %s AND course_id = %s AND semester = %s AND section_year = %s;", (std_google_id, course_id, semester, int(section_year)))

            data = cursor.fetchall()
            if data == []:
                cursor.execute("INSERT INTO takes "
                               "VALUES (%s, %s, %s, %s, %s, %s);", (section_id, semester, int(section_year), course_id, std_google_id, grade))
            else:
                cursor.execute("UPDATE takes "
                               "SET grade = %s "
                               "WHERE student_google_id = %s AND course_id = %s AND semester = %s AND section_year = %s;", (grade, std_google_id, course_id, semester, int(section_year)))
        except mysql.connector.errors.IntegrityError:
            pass
        db.commit()
    
    @staticmethod
    def add_current_semester(section_id, semester, section_year, course_id, std_google_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT course_id FROM takes WHERE student_google_id = %s AND course_id = %s AND semester = %s AND section_year = %s", (std_google_id, course_id, semester, int(section_year)))
            data = cursor.fetchall()
            if data == []:
                cursor.execute("INSERT INTO takes (section_id, semester, section_year, course_id, student_google_id) "
                               "VALUES (%s, %s, %s, %s, %s);", (section_id, semester, int(section_year), course_id, std_google_id))

        except mysql.connector.errors.IntegrityError:
            pass
        db.commit()

    @staticmethod
    def update_current_semester(section_id, semester, section_year, course_id, std_google_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE takes "
                           "SET section_id = %s "
                           "WHERE student_google_id = %s AND course_id = %s AND semester = %s AND section_year = %s;", (section_id, std_google_id, course_id, semester, int(section_year)))
        except mysql.connector.errors.IntegrityError:
            pass
        db.commit()

    @staticmethod
    def get_unrated_courses(std_google_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT section_id, semester, section_year, t.course_id, title "
                       "FROM takes AS t, course AS c "
                       "WHERE student_google_id = {} AND grade IS NULL AND t.course_id = c.course_id AND "
                       "(t.course_id, section_id, student_google_id, semester, section_year) NOT IN "
                       "(SELECT course_id, section_id, student_google_id, semester, section_year " 
		               "FROM course_rating);".format(std_google_id))
        unrated_courses = cursor.fetchall()
        return unrated_courses

    @staticmethod
    def save_course_rating(course_details, semester_year, rating, will_rec, did_enjoy, take_sim, good_content, was_helpful, std_google_id):
        course_sec = course_details.split('-')[0].strip()
        course_id = ' '.join(course_sec.split()[:2])
        section = course_sec.split()[-1]
        semester = semester_year.split()[0].strip()
        section_year = int(semester_year.split()[1].strip()) - 1
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO course_rating (rating_amount, will_recommend, did_enjoy, take_similar, good_content, was_helpful, student_google_id, section_id, semester, section_year, course_id) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (int(rating), will_rec, did_enjoy, take_sim, good_content, was_helpful, std_google_id, section, semester, section_year, course_id))
        db.commit()

    @staticmethod
    def get_unrated_instructors(std_google_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT tc.section_year, tc.semester, tk.course_id, tk.section_id, (SELECT title FROM course WHERE course_id=tk.course_id), "
                            "(SELECT instructor_name FROM instructor WHERE instructor_email = tc.instructor_email), "
                            "(SELECT instructor_profile_picture FROM instructor WHERE instructor_email = tc.instructor_email), "
                            "tc.instructor_email "
                       "FROM teaches AS tc, takes AS tk "
                       "WHERE tc.course_id=tk.course_id AND tk.grade IS NULL AND tc.section_year=tk.section_year AND tk.student_google_id={} AND "
                            "(tc.course_id, tc.section_year, tc.semester) NOT IN "
                            "(SELECT course_id, section_year, semester FROM instructor_rating);".format(std_google_id))
        
        unrated_instructors = cursor.fetchall()
        return unrated_instructors

    @staticmethod
    def save_instructor_rating(instructor_email, course_details, semester_year, rating, will_rec, is_suitable, grading, explanation, take_again, std_google_id):
        course_sec = course_details.strip().split('-')[0].strip()
        course_id = ' '.join(course_sec.split()[:2])
        section = course_sec.split()[-1]
        semester = semester_year.strip().split()[0]
        section_year = int(semester_year.split()[1]) - 1
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO instructor_rating (rating_amount, will_recommend, is_suitable, grading_policy, explanation_method, take_again, student_google_id, instructor_email, semester, section_year, course_id) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (int(rating), will_rec, is_suitable, grading, explanation, take_again, std_google_id, instructor_email, semester, section_year, course_id))
        db.commit()

    @staticmethod
    def get_user_timetable(std_google_id):
        now = datetime.datetime.now()
        today = now.strftime("%A")
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT t.course_id, c.title, ts.start_hr, ts.start_min, ts.end_hr, ts.end_min, s.building_no, s.room_no "
                       "FROM takes AS t, time_slot AS ts, section AS s, course AS c "
                       "WHERE student_google_id = %s AND grade IS NULL AND t.course_id=ts.course_id AND t.section_id=ts.section_id "
                       "AND t.section_year=ts.section_year AND t.semester=ts.semester AND c.course_id=s.course_id AND "
                       "s.section_id=t.section_id AND s.semester=t.semester AND s.section_year=t.section_year "
                       "AND s.course_id=t.course_id AND ts.section_day=%s;", (std_google_id, today))
        
        time_table = cursor.fetchall()
        for i in range(len(time_table)):
            time_table[i] = list(time_table[i])
            time_table[i].append("flaticon2-open-text-book")
            time_table[i][2] = str(time_table[i][2])
            time_table[i][3] = str(time_table[i][3])
            time_table[i][4] = str(time_table[i][4])
            time_table[i][5] = str(time_table[i][5])
            if len(time_table[i][2]) == 1:
                time_table[i][2] = '0' + time_table[i][2]
            if len(time_table[i][3]) == 1:
                time_table[i][3] = '0' + time_table[i][3]
            if len(time_table[i][4]) == 1:
                time_table[i][4] = '0' + time_table[i][4]
            if len(time_table[i][5]) == 1:
                time_table[i][5] = '0' + time_table[i][5]

        temp = []
        for i in range(len(time_table)):
            start_hr = int(time_table[i][2])
            end_hr = int(time_table[i][4])
            for j in range(start_hr, end_hr+1):
                if j not in temp:
                    temp.append(j)

        for i in range(9, 19):
            if i in temp:
                temp.pop(temp.index(i))
            else:
                temp.append(i)

        if len(temp) > 1:
            coffee = str(random.choice(temp))
            if len(coffee) == 1:
                coffee = '0' + coffee
            temp.pop(temp.index(int(coffee)))
            time_table.append(('Coffee Break', '', coffee, '00', '', '', 'Student Center', 'Zem Mekan', 'fas fa-mug-hot'))
        
        if len(temp) > 1:
            gym = str(random.choice(temp))
            if len(gym) == 1:
                gym = '0' + gym
            temp.pop(temp.index(int(gym)))
            time_table.append(('Gym', '', gym, '00', '', '', 'Student Center', 'Sports Center', 'fas fa-dumbbell'))
        
        if len(temp) > 1:
            lib = str(random.choice(temp))
            if len(lib) == 1:
                lib = '0' + lib
            temp.pop(temp.index(int(lib)))
            time_table.append(('Study Time', '', lib, '00', '', '', 'Library', 'East Wing', 'fas fa-book'))
                
        return sorted(time_table, key=lambda x: x[2])
