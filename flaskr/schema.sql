CREATE TABLE instructor (
  instructor_google_id VARCHAR(50),
  instructor_name VARCHAR(100),
  instructor_email VARCHAR(100),
  instructor_profile_picture VARCHAR(512),
  PRIMARY KEY (instructor_google_id)
);

CREATE TABLE student (
  student_google_id VARCHAR(50),
  student_id CHAR(9),
  student_name VARCHAR(100),
  student_email VARCHAR(100),
  student_profile_picture VARCHAR(512),
  student_semester TINYINT UNSIGNED,
  standing VARCHAR(15),
  completed_credits SMALLINT UNSIGNED,
  completed_ects SMALLINT UNSIGNED,
  gpa DECIMAL(3, 2),
  advisor VARCHAR(50),
  PRIMARY KEY (student_google_id),
  FOREIGN KEY (advisor) REFERENCES instructor(instructor_google_id)
);

CREATE TABLE testimonial (
  testimonial_ID INTEGER UNSIGNED AUTO_INCREMENT,
  testimonial_text TINYTEXT,
  testifier_position VARCHAR(50),
  student_google_id VARCHAR(50),
  PRIMARY KEY (testimonial_ID),
  FOREIGN KEY (student_google_id) REFERENCES student(student_google_id) ON DELETE CASCADE
);

CREATE TABLE instructor_rating (
  rating_id INTEGER UNSIGNED AUTO_INCREMENT,
  rating_amount TINYINT UNSIGNED,
  will_recommend VARCHAR(100),
  is_suitable VARCHAR(100),
  grading_policy VARCHAR(100),
  explanation_method VARCHAR(100),
  take_again VARCHAR(100),
  student_google_id VARCHAR(50),
  instructor_google_id VARCHAR(50),
  PRIMARY KEY (rating_id),
  FOREIGN KEY (student_google_id) REFERENCES student(student_google_id),
  FOREIGN KEY (instructor_google_id) REFERENCES instructor(instructor_google_id) 
);

CREATE TABLE course (
  course_id VARCHAR(15),
  title VARCHAR(255),
  credit TINYINT UNSIGNED,
  ects TINYINT UNSIGNED,
  theoritical_credit TINYINT,
  practical_credit TINYINT,
  course_year TINYINT,
  PRIMARY KEY (course_id)
);

CREATE TABLE prerequisite (
  course_id VARCHAR(15),
  prereq_id VARCHAR(15),
  PRIMARY KEY (course_id, prereq_id),
  FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE,
  FOREIGN KEY (prereq_id) REFERENCES course(course_id)
);

CREATE TABLE classroom (
  building_no VARCHAR(30),
  room_no VARCHAR(15),
  PRIMARY KEY (building_no, room_no)
);

CREATE TABLE section (
  section_id VARCHAR(5),
  semester VARCHAR(6) CHECK (semester IN ('Fall', 'Spring', 'Summer')),
  section_year NUMERIC(4, 0) CHECK (section_year > 2009 and section_year < 2050),
  course_id VARCHAR(15),
  building_no VARCHAR(30),
  room_no VARCHAR(15),
  PRIMARY KEY (section_id, semester, section_year, course_id),
  FOREIGN KEY (building_no, room_no) REFERENCES classroom(building_no, room_no),
  FOREIGN KEY (course_id) REFERENCES course(course_id) ON DELETE CASCADE
);

CREATE TABLE course_rating (
  rating_id INTEGER UNSIGNED AUTO_INCREMENT,
  rating_amount TINYINT UNSIGNED,
  will_recommend VARCHAR(100),
  did_enjoy VARCHAR(100),
  take_similar VARCHAR(100),
  good_content VARCHAR(100),
  was_helpful VARCHAR(100),
  student_google_id VARCHAR(50),
  section_id VARCHAR(5),
  semester VARCHAR(6),
  section_year NUMERIC(4, 0),
  course_id VARCHAR(15),
  PRIMARY KEY (rating_id),
  FOREIGN KEY (student_google_id) REFERENCES student(student_google_id),
  FOREIGN KEY (section_id, semester, section_year, course_id) REFERENCES section(section_id, semester, section_year, course_id) 
);

CREATE TABLE takes (
  section_id VARCHAR(5),
  semester VARCHAR(6),
  section_year NUMERIC(4, 0),
  course_id VARCHAR(15),
  student_google_id VARCHAR(50),
  grade VARCHAR(5),
  PRIMARY KEY (section_id, semester, section_year, course_id, student_google_id),
  FOREIGN KEY (section_id, semester, section_year, course_id) REFERENCES section(section_id, semester, section_year, course_id),
  FOREIGN KEY (student_google_id) REFERENCES student(student_google_id)
);

CREATE TABLE teaches (
  section_id VARCHAR(5),
  semester VARCHAR(6),
  section_year NUMERIC(4, 0),
  course_id VARCHAR(15),
  instructor_google_id VARCHAR(15),
  PRIMARY KEY (section_id, semester, section_year, course_id, instructor_google_id),
  FOREIGN KEY (section_id, semester, section_year, course_id) REFERENCES section(section_id, semester, section_year, course_id),
  FOREIGN KEY (instructor_google_id) REFERENCES instructor(instructor_google_id)
);

CREATE TABLE department (
  department_name VARCHAR(100),
  department_code VARCHAR(10),
  PRIMARY KEY (department_name)
);

CREATE TABLE student_department (
  student_google_id VARCHAR(50),
  department_name VARCHAR(100),
  enrolled_type VARCHAR(50),
  PRIMARY KEY (student_google_id, department_name),
  FOREIGN KEY (student_google_id) REFERENCES student(student_google_id),
  FOREIGN KEY (department_name) REFERENCES department(department_name)
);

CREATE TABLE instructor_department (
  instructor_google_id VARCHAR(50),
  department_name VARCHAR(100),
  PRIMARY KEY (instructor_google_id, department_name),
  FOREIGN KEY (instructor_google_id) REFERENCES instructor(instructor_google_id),
  FOREIGN KEY (department_name) REFERENCES department(department_name)
);

CREATE TABLE course_department (
  course_id VARCHAR(15),
  department_name VARCHAR(100),
  course_type VARCHAR(50),
  PRIMARY KEY (course_id, department_name),
  FOREIGN KEY (course_id) REFERENCES course(course_id),
  FOREIGN KEY (department_name) REFERENCES department(department_name)
);

CREATE TABLE time_slot (
  time_slot_id INTEGER UNSIGNED AUTO_INCREMENT,
  section_day VARCHAR(10),
  start_hr NUMERIC(2, 0) CHECK (start_hr >= 0 and start_hr < 24),
  start_min NUMERIC(2, 0) CHECK (start_min >= 0 and start_min < 60),
  end_hr NUMERIC(2, 0) CHECK (end_hr >= 0 and end_hr < 24),
  end_min NUMERIC(2, 0) CHECK (end_min >= 0 and end_min < 60),
  section_id VARCHAR(5),
  semester VARCHAR(6),
  section_year NUMERIC(4, 0),
  course_id VARCHAR(15),
  PRIMARY KEY (time_slot_id),
  FOREIGN KEY (section_id, semester, section_year, course_id) REFERENCES section(section_id, semester, section_year, course_id) ON DELETE CASCADE
);
