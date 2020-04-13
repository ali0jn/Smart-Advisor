from flask import Markup


def create_radio_button(n):
	radio_html = ''
	check = True
	for i in range(n):
		if check:
			radio_html += Markup("<input type='radio' name='slider_2' id='slide_2_{}' checked />".format(i+1))
			check = False
		else:
			radio_html += Markup("<input type='radio' name='slider_2' id='slide_2_{}' checked />".format(i+1))
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
	testifiers = {'Asem Okby': ['This app is nice', 'asem', 'Athlete'],
                  'Elon Musk': ['OMG!', 'elon', 'CEO'],
                  'Ibrahim Tigrek': ['Cool', 'ibrahim', 'Data Scientist']}
	html_ = ''
	for test_name in testifiers:
		html_ += slide_content(testifiers[test_name][0], '/static/media/users/{}.jpg'.format(testifiers[test_name][1]), test_name, testifiers[test_name][2])

	radio_button_block = create_radio_button(len(testifiers))
	label_block = create_label_button(len(testifiers))
	return html_, radio_button_block, label_block, len(testifiers)
