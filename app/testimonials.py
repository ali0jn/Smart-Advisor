from flask import Markup
from app.db import get_db
import random

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

def fetch_testifiers():
	db = get_db()
	cursor = db.cursor()
	cursor.execute("SELECT student_name, testimonial_text, testifier_position, google_profile_picture FROM testimonial AS t, student AS s WHERE t.student_google_id = s.student_google_id;")
	result = cursor.fetchall()
	html_ = ''
	random_testimonies = []
	c = 0
	while c < 4:
		random_idx = random.randint(0, len(result)-1)
		if result[random_idx] not in random_testimonies:
			random_testimonies.append(result[random_idx])
			c += 1
	for res in random_testimonies:
		html_ += slide_content(res[1], res[3], res[0], res[2])
	radio_button_block = create_radio_button(4)
	label_block = create_label_button(4)
	return html_, radio_button_block, label_block

def save_testimony(testimony, headline, std_google_id):
	db = get_db()
	cursor = db.cursor()
	cursor.execute("INSERT INTO testimonial (testimonial_text, testifier_position, student_google_id) VALUES(%s, %s, %s);", (testimony, headline, std_google_id))
	db.commit()
