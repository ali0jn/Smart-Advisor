from flask_login import UserMixin
from flaskr.db import get_db
import mysql.connector
import datetime
import random
import json
import os

with open(os.getcwd() + '/flaskr/data/course_reqs.json') as jr:
    dept_course_reqs = json.load(jr)

with open(os.getcwd() + '/flaskr/data/parameters.json') as jr:
    parameters = json.load(jr)

class Instructor(UserMixin):
    def __init__(self, instructor_google_id, instructor_name, instructor_email, instructor_profile_pic):
        self.instructor_google_id = instructor_google_id
        self.instructor_name = instructor_name
        self.instructor_email = instructor_email
        self.instructor_profile_pic = instructor_profile_pic

    def get(self):
        db = get_db()
        cursor = db.cursor()
        inst = cursor.execute("SELECT * FROM instructor WHERE instructor_email = '{}';".format(self.instructor_email))
        inst = cursor.fetchone()

        if inst != None:
            cursor.execute("UPDATE instructor "
                           "SET instructor_google_id = %s, instructor_profile_picture = %s "
                           "WHERE instructor_email = %s;", (self.instructor_google_id, self.instructor_profile_pic, self.instructor_email))
            db.commit()
            return self

        return None

    def create(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO instructor (instructor_email, instructor_name, instructor_google_id, instructor_profile_picture) "
                       "VALUES(%s, %s, %s, %s);", (self.instructor_email, self.instructor_name, self.instructor_google_id, self.instructor_profile_picture))
        db.commit()
    
    def get_department(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT department_name FROM instructor_department WHERE instructor_email = '{}';".format(self.instructor_email))
        instructor_department = cursor.fetchone()[0]
        return instructor_department        

    def get_timetable(self):
        now = datetime.datetime.now()
        today = now.strftime("%A")
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT ts.course_id, sd.title, ts.start_hr, ts.start_min, ts.end_hr, ts.end_min, sd.building_no, sd.room_no "
                       "FROM time_slot as ts, (SELECT s.section_id, s.semester, s.section_year, s.course_id, s.building_no, s.room_no, c.title "
                                              "FROM course AS c, (SELECT * "
                                                                 "FROM section "
                                                                 "WHERE (section_id, course_id, semester, section_year) IN (SELECT section_id, course_id, semester, section_year "
                                                                                                                           "FROM teaches "
                                                                                                                           "WHERE instructor_email = %s "
                                                                                                                           "AND section_year = %s "
                                                                                                                           "AND semester = %s)) as s "
                                              "WHERE c.course_id = s.course_id) as sd "
                        "WHERE ts.section_id=sd.section_id "
                        "AND ts.section_year=sd.section_year "
                        "AND ts.semester=sd.semester "
                        "AND ts.course_id=sd.course_id "
                        "AND ts.section_day = %s;", (self.instructor_email, parameters['current_year'], parameters['current_semester'], today))
        
        time_table = cursor.fetchall()
        for i in range(len(time_table)):
            time_table[i] = list(time_table[i])
            time_table[i].append("flaticon-presentation")
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
            research = str(random.choice(temp))
            if len(research) == 1:
                research = '0' + research
            temp.pop(temp.index(int(research)))
            time_table.append(('Research', '', research, '00', '', '', 'Istanbul Sehir University', 'Office', 'flaticon2-open-text-book'))
                        
        return sorted(time_table, key=lambda x: x[2])
    
    def get_advisees(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM student WHERE advisor='{}';".format(self.instructor_email))
        advisees = cursor.fetchall()
        return advisees
    
    def get_course_stats(self):
        colors = ['gold', 'green', 'blue', 'yellow', 'red', 'grey', 'purple', 'lavendar', 'lightblue',
                  'lightgreen', 'cyan', 'magenta']
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT res.course_id, c.title, res.department_code, res.total_enrolled, res.avg_gpa "
                       "FROM course AS c, (SELECT res.course_id, res.department_code, count(*) AS total_enrolled, avg(s.gpa) AS avg_gpa "
                                          "FROM student AS s, (SELECT t.course_id, d.department_code, t.student_google_id "
							                                  "FROM takes AS t, student_department AS sd, department AS d "
							                                  "WHERE section_year = %s "
							                                  "AND semester=%s "
							                                  "AND course_id IN (SELECT course_id "
											                                    "FROM teaches "
											                                    "WHERE instructor_email=%s) "
                                                                                "AND t.student_google_id=sd.student_google_id "
                                                                                "AND d.department_name=sd.department_name) AS res "
                                                                                "WHERE res.student_google_id=s.student_google_id "
                                                                                "GROUP BY res.course_id, res.department_code) AS res "
                      "WHERE res.course_id=c.course_id;", (parameters['current_year'], parameters['current_semester'], self.instructor_email))
        current_teaching = cursor.fetchall()
        course_stats = {}
        gpa_stats = {}
        for course_id, title, department_code, total_enrolled, avg_gpa in current_teaching:
            course_id = course_id + ' ' + title
            course_stats.setdefault(course_id, [['Department Code', 'Ratios']])
            gpa_stats.setdefault(course_id, [["Department", "Avg. GPA", {"role": "style"}]])
            course_stats[course_id].append([department_code, total_enrolled])
            random_color = random.randint(0, len(colors)-1)
            gpa_stats[course_id].append([department_code, round(float(avg_gpa), 2), colors.pop(random_color)])
        for key in course_stats:
            course_stats[key] = json.dumps(course_stats[key])
            gpa_stats[key] = json.dumps(gpa_stats[key])
        return course_stats, gpa_stats

class Student(UserMixin):
    def __init__(self, student_google_id, student_name, student_email, student_profile_picture):
        self.student_google_id = student_google_id
        self.student_name = student_name
        self.student_email = student_email
        self.student_profile_picture = student_profile_picture

    @staticmethod
    def get(student_google_id):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM student WHERE student_google_id = {};".format(student_google_id))
        std = cursor.fetchall()

        if std == []:
            return None

        return Student(std[0][0], std[0][2], std[0][3], std[0][4])

    def create(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO student (student_google_id, student_name, student_email, student_profile_picture) "
                       "VALUES(%s, %s, %s, %s);", (self.student_google_id, self.student_name, self.student_email, self.student_profile_picture))
        db.commit()

    def update_profile(self, student_number, student_semester, advisor, standing, gpa, completed_credits, completed_ects):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("UPDATE student "
                       "SET student_id = %s, student_semester = %s, advisor = (select instructor_email from instructor where instructor_name = %s), standing = %s, gpa = %s, completed_credits = %s, completed_ects = %s "
                       "WHERE student_google_id = %s;", (student_number, int(student_semester), advisor, standing, float(gpa), int(completed_credits), int(completed_ects), self.student_google_id))
        db.commit()

    def get_details(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT student_id, student_semester, (SELECT instructor_name FROM instructor WHERE instructor_email = advisor), standing, gpa, completed_credits, completed_ects "
                       "FROM student "
                       "WHERE student_google_id = {};".format(self.student_google_id))
        return cursor.fetchone()

    def get_department(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT department_name FROM student_department WHERE enrolled_type = 'Main Prg' AND student_google_id = {};".format(self.student_google_id))
        dept_name = cursor.fetchone()
        if dept_name != None:
            dept_name = dept_name[0]
        return dept_name

    def graduation_progress(self):
        db = get_db()
        cursor = db.cursor()
        department_name = self.get_department()
        cursor.execute("SELECT COUNT(*) "
                       "FROM course_department "
                       "WHERE course_type='Required' AND department_name = '{}';".format(department_name))
        total_required = int(cursor.fetchone()[0])
        extras = sum(list(dept_course_reqs[department_name].values()))
        cursor.execute("SELECT COUNT(*) "
                       "FROM takes "
                       "WHERE student_google_id = '{}' "
                       "AND grade IS NOT NULL "
                       "AND grade NOT IN ('F', 'IA', 'W');".format(self.student_google_id))
        total_taken = int(cursor.fetchone()[0])
        return int((total_taken / (total_required + extras) * 100))

    def add_department(self, dept_dict):
        db = get_db()
        cursor = db.cursor()
        for enrolment_type in dept_dict:
            try:
                cursor.execute("INSERT INTO student_department "
                               "VALUES (%s, %s, %s); ", (self.student_google_id, dept_dict[enrolment_type], enrolment_type))
            except mysql.connector.errors.IntegrityError:
                pass
        db.commit()

    def add_transcript(self, section_id, semester, section_year, course_id, grade):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT semester, section_year, course_id, student_google_id "
                           "FROM takes "
                           "WHERE student_google_id = %s AND course_id = %s AND semester = %s AND section_year = %s;", (self.student_google_id, course_id, semester, int(section_year)))

            data = cursor.fetchall()
            if data == []:
                cursor.execute("INSERT INTO takes "
                               "VALUES (%s, %s, %s, %s, %s, %s);", (section_id, semester, int(section_year), course_id, self.student_google_id, grade))
            else:
                cursor.execute("UPDATE takes "
                               "SET grade = %s "
                               "WHERE student_google_id = %s AND course_id = %s AND semester = %s AND section_year = %s;", (grade, self.student_google_id, course_id, semester, int(section_year)))
        except mysql.connector.errors.IntegrityError:
            pass
        db.commit()
    
    def add_current_semester(self, section_id, semester, section_year, course_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("SELECT course_id FROM takes WHERE student_google_id = %s AND course_id = %s AND semester = %s AND section_year = %s", (self.student_google_id, course_id, semester, int(section_year)))
            data = cursor.fetchall()
            if data == []:
                cursor.execute("INSERT INTO takes (section_id, semester, section_year, course_id, student_google_id) "
                               "VALUES (%s, %s, %s, %s, %s);", (section_id, semester, int(section_year), course_id, self.student_google_id))

        except mysql.connector.errors.IntegrityError:
            pass
        db.commit()

    def update_current_semester(self, section_id, semester, section_year, course_id):
        db = get_db()
        cursor = db.cursor()
        try:
            cursor.execute("UPDATE takes "
                           "SET section_id = %s "
                           "WHERE student_google_id = %s AND course_id = %s AND semester = %s AND section_year = %s;", (section_id, self.student_google_id, course_id, semester, int(section_year)))
        except mysql.connector.errors.IntegrityError:
            pass
        db.commit()

    def get_unrated_courses(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT res.section_id, res.semester, res.section_year, res.course_id, c.title "
                       "FROM course AS c, (SELECT section_id, semester, section_year, course_id "
                                          "FROM takes AS t "
                                          "WHERE student_google_id = {} "
                                          "AND grade IS NULL "
                                          "AND (course_id, section_id, semester, section_year) NOT IN "
                                          "(SELECT course_id, section_id, semester, section_year "
                                          "FROM course_rating AS cr "
                                          "WHERE cr.student_google_id = t.student_google_id)) AS res "
                       "WHERE res.course_id = c.course_id;".format(self.student_google_id))
        unrated_courses = cursor.fetchall()
        return unrated_courses

    def save_course_rating(self, course_details, semester_year, rating, will_rec, did_enjoy, take_sim, good_content, was_helpful):
        course_sec = course_details.split('-')[0].strip()
        course_id = ' '.join(course_sec.split()[:2])
        section = course_sec.split()[-1]
        semester = semester_year.split()[0].strip()
        section_year = int(semester_year.split()[1].strip()) - 1
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO course_rating (rating_amount, will_recommend, did_enjoy, take_similar, good_content, was_helpful, student_google_id, section_id, semester, section_year, course_id) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (int(rating), will_rec, did_enjoy, take_sim, good_content, was_helpful, self.student_google_id, section, semester, section_year, course_id))
        db.commit()

    def get_unrated_instructors(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT res.section_year, res.semester, res.course_id, res.section_id, (SELECT title "
																	                          "FROM course "
                                                                                              "WHERE course_id = res.course_id), "
	                          "(SELECT instructor_name FROM instructor WHERE instructor_email = res.instructor_email), "
                              "(SELECT instructor_profile_picture FROM instructor WHERE instructor_email = res.instructor_email), "
                              "res.instructor_email "
                       "FROM (SELECT * "
                             "FROM teaches "
                             "WHERE (section_id, semester, section_year, course_id) IN (SELECT section_id, semester, section_year, course_id "
                                                                                       "FROM takes as t "
                                                                                       "WHERE student_google_id = {} "
                                                                                       "AND t.grade IS NULL "
                                                                                       "AND (course_id, semester, section_year) NOT IN "
                                                                                           "(SELECT course_id, semester, section_year "
                                                                                            "FROM instructor_rating AS ir "
                                                                                            "WHERE t.student_google_id = ir.student_google_id))) as res;".format(self.student_google_id))
        
        unrated_instructors = cursor.fetchall()
        return unrated_instructors

    def save_instructor_rating(self, instructor_email, course_details, semester_year, rating, will_rec, is_suitable, grading, explanation, take_again):
        course_sec = course_details.strip().split('-')[0].strip()
        course_id = ' '.join(course_sec.split()[:2])
        section = course_sec.split()[-1]
        semester = semester_year.strip().split()[0]
        section_year = int(semester_year.split()[1]) - 1
        db = get_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO instructor_rating (rating_amount, will_recommend, is_suitable, grading_policy, explanation_method, take_again, student_google_id, instructor_email, semester, section_year, course_id) "
                       "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (int(rating), will_rec, is_suitable, grading, explanation, take_again, self.student_google_id, instructor_email, semester, section_year, course_id))
        db.commit()

    def get_timetable(self):
        now = datetime.datetime.now()
        today = now.strftime("%A")
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT ts.course_id, sd.title, ts.start_hr, ts.start_min, ts.end_hr, ts.end_min, sd.building_no, sd.room_no "
                       "FROM time_slot AS ts, (SELECT c.course_id, res.semester, res.section_year, res.section_id, c.title, res.building_no, res.room_no "
                                                "FROM course as c, (SELECT * "
                                                                    "FROM section "
                                                                    "WHERE (section_id, semester, section_year, course_id) IN (SELECT section_id, semester, section_year, course_id "
                                                                                                                                "FROM takes "
                                                                                                                                "WHERE student_google_id = %s "
                                                                                                                                "AND grade IS NULL)) AS res "
					                           "WHERE c.course_id = res.course_id) AS sd "
                       "WHERE ts.section_id = sd.section_id "
                       "AND ts.course_id=sd.course_id "
                       "AND ts.section_year=sd.section_year "
                       "AND ts.semester=sd.semester "
                       "AND ts.section_day = %s;", (self.student_google_id, today))
        
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

    def get_completed_courses(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT t.course_id, t.title, t.semester, t.section_year, t.grade, cd.course_type "
                       "FROM course_department as cd, (SELECT c.course_id, c.title, res.semester, res.section_year, res.grade "
                                                      "FROM course AS c, (SELECT semester, section_year, course_id, grade "
                                                                         "FROM takes "
                                                                         "WHERE student_google_id = %s "
                                                                         "AND grade IS NOT NULL) AS res "
                                                      "WHERE c.course_id = res.course_id) AS t "
                       "WHERE cd.course_id = t.course_id "
                       "AND cd.department_name = (SELECT department_name "
						                         "FROM student_department "
                                                 "WHERE student_google_id = %s "
                                                 "AND enrolled_type = 'Main Prg') "
                       "ORDER BY t.section_year, t.semester, t.course_id;", (self.student_google_id, self.student_google_id))
        
        completed_courses = cursor.fetchall()
        cc = {}
        for row in completed_courses:
            cc[row[0]] = {"title": row[1], "semester": row[2], "year": str(row[3]), "grade": row[4], "course_type": row[5]}
        return cc
    
    def get_incompleted_required_courses(self):
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT cd.course_id, c.title, cd.course_type, c.credit, c.ects, c.course_year "
                       "FROM course_department AS cd, course AS c "
                       "WHERE cd.course_id = c.course_id "
                       "AND cd.course_type = 'Required' "
                       "AND cd.course_id NOT IN (SELECT course_id "
                                                "FROM takes "
                                                "WHERE student_google_id=%s AND grade IS NOT NULL) "
                        "AND (SELECT department_name "
                             "FROM student_department "
                             "WHERE student_google_id=%s) = cd.department_name "
                       "ORDER BY c.course_year;", (self.student_google_id, self.student_google_id))
        
        incompleted_required_courses = cursor.fetchall()
        ic = {}
        for row in incompleted_required_courses:
            ic[row[0]] = {"title": row[1], "course_type": row[2], "credit": str(row[3]), "ects": row[4], "course_year": row[5]}
        return ic
