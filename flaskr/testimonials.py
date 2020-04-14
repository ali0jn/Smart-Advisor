from flask import Markup
from flaskr.db import get_db


def create_radio_button(n):
	radio_html = ''
	check = True
	for i in range(n):
		if check:
			radio_html += Markup("<input type='radio' name='slider_2' id='slide_2_{}' checked />".format(i+1))
			check = False
		else:
			radio_html += Markup("<input type='radio' name='slider_2' id='slide_2_{}' />".format(i+1))
	return radio_html
	
def create_label_button(n):
	label_html = ''
	for i in range(n):
		label_html += Markup("<label for='slide_2_{}'></label>".format(i+1))
	return label_html

def slide_content(testimony, image, name, desc):
    content = Markup("<div class='slide_content'>\
                        <div class='testimonial_2'>\
					        <div class='content_2'>\
						        <p><i class='fas fa-quote-left' style='margin-right: 5px; size: 10px;'></i>{}<i class='fas fa-quote-right' style='margin-left: 5px; size: 10px;'></i></p>\
					        </div>\
					    <div class='profile_pic'>\
    						<img src='{}' alt='testifier'>\
					    </div>\
					    <div class='author_2'>\
						    <h3>{}</h3>\
						    <h4>{}</h4>\
					    </div>\
				        </div>\
			        </div>".format(testimony, image, name, desc))
    return content

def get_testimonies():
	testifiers = {}
	db = get_db()
	cursor = db.cursor()
	testimonies = cursor.execute("SELECT student_name, testimonial_text, testifier_position, google_profile_picture FROM testimonial AS t, student AS s WHERE t.student_google_id = s.student_google_id;")
	result = cursor.fetchall()
	for res in result:
		testifiers[res[0]] = [res[1], res[3], res[2]]
	return testifiers

def fetch_testifiers():
	db = get_db()
	cursor = db.cursor()
	testimonies = cursor.execute("SELECT student_name, testimonial_text, testifier_position, google_profile_picture FROM testimonial AS t, student AS s WHERE t.student_google_id = s.student_google_id;")
	result = cursor.fetchall()
	html_ = ''
	c = 0
	for res in result:
		html_ += slide_content(res[1], res[3], res[0], res[2])
		c += 1
	radio_button_block = create_radio_button(c)
	label_block = create_label_button(c)
	return html_, radio_button_block, label_block, c

def save_testimony(testimony, headline, std_google_id):
	db = get_db()
	cursor = db.cursor()
	cursor.execute("INSERT INTO testimonial (testimonial_text, testifier_position, student_google_id) VALUES(%s, %s, %s);", (testimony, headline, std_google_id))
	db.commit()
