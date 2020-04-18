from flask_login import UserMixin
from unicode_tr.extras import slugify

from flaskr.db import get_db

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
        cursor.execute(
            "INSERT INTO student (student_google_id, student_name, student_email, google_profile_picture) "
            "VALUES(%s, %s, %s, %s);", (id_, name, email, profile_pic))
        db.commit()

    @staticmethod
    def update_profile(student_number, student_semester, advisor, standing, gpa, completed_credits, completed_ects, std_google_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE student "
                       "SET student_id = %s, student_semester = %d, advisor = (select instructor_google_id from instructor where instructor_name = %s), standing = %s, gpa = %f, completed_credits = %d, completed_ects = %d "
                       "WHERE student_google_id = %s;", (student_number, student_semester, slugify(advisor).upper().replace('-', ' '), standing, gpa, completed_credits, completed_ects, std_google_id))
        db.commit()
