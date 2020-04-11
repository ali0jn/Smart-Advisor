CREATE TABLE student (
  student_google_id VARCHAR(),
  student_id CHAR(9),
  student_name VARCHAR(),
  student_email VARCHAR(),
  student_semester INTEGER
  standing VARCHAR(),
  completed_credits INTEGER,
  completed_ects INTEGER,
  gpa FLOAT(3, 2)
  advisor VARCHAR()
  PRIMARY KEY (student_google_id),
  FOREIGN KEY (advisor) REFERENCES instructor
);

CREATE TABLE testimonials (
  test_ID INTEGER AUTO_INCREMENT,
  test_text TEXT,
  test_description VARCHAR(),
  testifier_image IMAGE
  student_google_id VARCHAR(),
  PRIMARY KEY (test_ID),
  FOREIGN KEY (student_google_id) REFERENCES student
);

CREATE TABLE instructor (
  instructor_google_id VARCHAR(),
  instructor_id CHAR(),
  instructor_name VARCHAR(),
  instructor_email VARCHAR(),
  PRIMARY KEY (instructor_google_id),
  FOR
);

CREATE TABLE department (
  department_name VARCHAR(),
  department_code VARCHAR(),
  PRIMARY KEY (department_name)
);

CREATE TABLE course (
  course_id VARCHAR(8),
  title VARCHAR(),
  credit INTEGER,
  ects INTEGER,
  course_level VARCHAR(),
  theoritical_credit INTEGER,
  practical_credit INTEGER,
  course_year INTEGER,
);

CREATE TABLE course_rating (
  rating_id INTEGER AUTO_INCREMENT,
  rating_amount INTEGER,
  will_recommend BIT(1),
  did_enjoy VARCHAR(),
  take_similar VARCHAR(),
  good_content VARCHAR(),
  was_helpful VARCHAR(),
  student_google_id (),
  instructor_google_id (),
  PRIMARY KEY (rating_id)
  FOREIGN KEY (student_google_id) REFERENCES student,
  FOREIGN KEY (instuctor_google_id) REFERENCES instructor 
);


CREATE TABLE instructor_rating (
  rating_id INTEGER AUTO_INCREMENT,
  rating_amount INTEGER,
  will_recommend BIT(1),
  is_suitable BIT(1),
  grading_policy VARCHAR(),
  explanation_method VARCHAR(),
  take_again BIT(1),
  student_google_id (),
  instructor_google_id (),
  PRIMARY KEY (rating_id)
  FOREIGN KEY (student_google_id) REFERENCES student,
  FOREIGN KEY (instuctor_google_id) REFERENCES instructor 
);

CREATE TABLE Classroom (
  building_no VARCHAR(),
  room_no VARCHAR(),
  PRIMARY KEY (building_no, room_no)
);

CREATE TABLE section (
  section_id CHAR(),
  semester VARCHAR(),
  section_year CHAR(4),
  course_id VARCHAR(),
  building_no VARCHAR(),
  room_no VARCHAR(),
  PRIMARY KEY (section_id, semester, section_year, course_id)
  FOREIGN KEY (building_no, room_no) REFERENCES Classroom,
  FOREIGN KEY course_id REFERENCES course ON DELETE CASCADE
);

CREATE TABLE teaches (
  section_id CHAR(),
  semester VARCHAR(),
  section_year CHAR(4),
  course_id VARCHAR(),
  instructor_google_id VARCHAR(),
  PRIMARY KEY (section_id, semester, section_year, course_id, instructor_google_id),
  FOREIGN KEY (section_id, semester, section_year, course_id) REFERENCES section,
  FOREIGN KEY (instructor_google_id) REFERENCES instructor
);

CREATE TABLE takes (
  section_id CHAR(),
  semester VARCHAR(),
  section_year CHAR(4),
  course_id VARCHAR(),
  student_google_id VARCHAR(),
  grade VARCHAR(2)
  PRIMARY KEY (section_id, semester, section_year, course_id, student_google_id)
  FOREIGN KEY (section_id, semester, section_year, course_id) REFERENCES section,
  FOREIGN KEY (student_google_id) REFERENCES student
);

CREATE TABLE time_slot (
  time_slot_id INTEGER AUTO_INCREMENT,
  section_day VARCHAR(),
  start_hr CHAR(),
  start_min CHAR(),
  end_hr CHAR(),
  end_min CHAR(),
  section_id CHAR(),
  semester VARCHAR(),
  section_year CHAR(4),
  course_id VARCHAR(),
  PRIMARY KEY (time_slot_id, section_day, start_hr, start_min, section_id, semester, section_year, course_id)
  FOREIGN KEY (section_id, semester, section_year, course_id) REFERENCES section  
);

CREATE TABLE course_dept (
  course_id VARCHAR(),
  department_name VARCHAR(),
  course_type VARCHAR()
  PRIMARY KEY (course_id, department_name),
  FOREIGN KEY (course_id) REFERENCES course,
  FOREIGN KEY (department_name) REFERENCES department_name
);

CREATE TABLE student_department (
  student_google_id VARCHAR(),
  department_name VARCHAR(),
  PRIMARY KEY (student_google_id, department_name),
  FOREIGN KEY (student_google_id) REFERENCES student,
  FOREIGN KEY (department_name) REFERENCES department
);

CREATE TABLE instructor_department (
  instructor_google_id VARCHAR(),
  department_name VARCHAR(),
  PRIMARY KEY (instructor_google_id, department_name)
);

CREATE TABLE prerequisite (
  course_id VARCHAR(),
  prereq_id VARCHAR(),
  PRIMARY KEY (course_id, prereq_id),
  FOREIGN KEY (course_id) REFERENCES course ON DELETE CASCADE,
  FOREIGN KEY (prereq_id) REFERENCES course
);
