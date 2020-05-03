from flask_login import UserMixin
from flaskr.db import get_db
import mysql.connector

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
                       "SET student_id = %s, student_semester = %s, advisor = (select instructor_google_id from instructor where instructor_name = %s), standing = %s, gpa = %s, completed_credits = %s, completed_ects = %s "
                       "WHERE student_google_id = %s;", (student_number, int(student_semester), advisor, standing, float(gpa), int(completed_credits), int(completed_ects), std_google_id))
        db.commit()

    @staticmethod
    def get_details(std_google_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT student_id, student_semester, (SELECT instructor_name FROM instructor WHERE instructor_google_id = advisor), standing, gpa, completed_credits, completed_ects "
                       "FROM student "
                       "WHERE student_google_id = {};".format(std_google_id))
        details = cursor.fetchall()[0]
        cursor.execute("SELECT department_name FROM student_department WHERE enrolled_type = 'Main Prg' AND student_google_id = {};".format(std_google_id))
        if cursor == []:
            dept = None
        else:        
            dept = cursor.fetchall()
        return details[0], details[1], details[2], details[3], details[4], details[5], details[6], dept

    @staticmethod
    def add_department(dept_dict, std_google_id):
        db = get_db()
        cursor = db.cursor()
        for enrolment_type in dept_dict:
            try:
                cursor.execute("INSERT INTO student_department "
                               "VALUES (%s, %s, %s);", (std_google_id, dept_dict[enrolment_type], enrolment_type))
            except:
                pass
        db.commit()

    @staticmethod
    def add_transcript(section_id, semester, section_year, course_id, std_google_id, grade):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("INSERT INTO takes "
                           "VALUES (%s, %s, %s, %s, %s, %s);", (section_id, semester, int(section_year), course_id, std_google_id, grade))
        except mysql.connector.errors.IntegrityError:
            pass
        db.commit()
