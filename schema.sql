CREATE TABLE student (
  student_google_id VARCHAR(),
  student_id CHAR(),
  student_name VARCHAR(),
  student_email VARCHAR(),
  student_semester INTEGER
  standing VARCHAR(),
  completed_credits INTEGER,
  completed_ects INTEGER,
  gpa FLOAT(3, 2)
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
