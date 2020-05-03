import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
import re
from flaskr.db import get_db

parent = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.chdir(parent)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(executable_path=os.getcwd()+'/Smart-Advisor/flaskr/drivers/chromedriver', options=chrome_options)
    return driver

def fetch_timetable(url, semester, year):
    db = get_db()
    cursor = db.cursor()
    driver = setup_driver()
    driver.get(url)
    driver.implicitly_wait(10)
    elements = driver.find_elements_by_tag_name('tr')
    for i in range(1, len(elements)):
        sub_elements = elements[i].find_elements_by_tag_name('td')
        course_sec = sub_elements[0].text.split()
        if len(course_sec) > 2:
            course_id = ' '.join(course_sec[:2])
            section_id = course_sec[2]
        else:
            course_id = ' '.join(course_sec)
            section_id = '01'
        
        days = get_days(sub_elements[2])
        time_slots = get_time_slots(sub_elements[3])
        location = get_locations(sub_elements[4].text)
        event_details = get_event_detail(days, time_slots, location)
        if event_details != None:
            for detail in event_details:
                building = detail[2].split('#')[0].strip()
                room = detail[2].split('#')[1].strip()
                day = detail[0].strip()
                start_hr = int(detail[1][:2].strip())
                start_min = int(detail[1][3:5].strip())
                end_hr = int(detail[1][6:8].strip())
                end_min = int(detail[1][9:].strip())
    
                try:
                    cursor.execute("INSERT INTO classroom "
                                   "VALUES (%s, %s);", (building, room))
                except mysql.connector.errors.IntegrityError:
                    pass

                try:
                    cursor.execute("INSERT INTO section "
                                   "VALUES (%s, %s, %s, %s, %s, %s);", (section_id, semester, year, course_id, building, room))
                except mysql.connector.errors.IntegrityError:
                    pass

                try:
                    cursor.execute("INSERT INTO time_slot (section_day, start_hr, start_min, end_hr, end_min, section_id, semester, section_year, course_id) "
                                   "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);", (day, start_hr, start_min, end_hr, end_min, section_id, semester, year, course_id))
                except mysql.connector.errors.IntegrityError:
                    pass
        else:
            try:
                cursor.execute("INSERT INTO section (section_id, semester, section_year, course_id) "
                                "VALUES (%s, %s, %s, %s);", (section_id, semester, year, course_id))
            except mysql.connector.errors.IntegrityError:
                pass
        db.commit()

def get_event_detail(days, time_slots, location):
    details = []
    if location == []:
        return None

    if len(days) == len(time_slots):
        if len(days) == len(location):
            for i in range(len(days)):
                details.append([days[i], time_slots[i], location[i]])
            return details
        else:
            for i in range(len(days)):
                details.append([days[i], time_slots[i], location[0]])
            return details

    elif len(days) > len(time_slots):
        if len(days) == len(location):
            for i in range(len(days)):
                details.append([days[i], time_slots[0], location[i]])
            return details
        else:
            for i in range(len(days)):
                details.append([days[i], time_slots[0], location[0]])
            return details

    elif len(days) < len(time_slots):
        if len(time_slots) == len(location):
            for i in range(len(time_slots)):
                details.append([days[0], time_slots[i], location[i]])
            return details
        else:
            for i in range(len(time_slots)):
                details.append([days[0], time_slots[i], location[0]])
            return details

def get_locations(location):
    pat = re.compile(r'\w+\s\w+\s\w+\s#\w+|\w+\s\w+\s#\w+|\w+\s\w+\s\w+\s\w+\s#\w+')
    return pat.findall(location)

def get_days(days):
    return days.text.split()

def get_time_slots(time_slot):
    return time_slot.text.split()

fetch_timetable('https://www.sehir.edu.tr/en/Announcements/2019_2020_Akademik_Yili_Bahar_Donemi_Ders_Programi', 'Spring', 2019)
