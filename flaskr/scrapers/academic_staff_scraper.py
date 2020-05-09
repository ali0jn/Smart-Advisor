import os
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.chrome.options import Options  
import mysql.connector

parent = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.chdir(parent)

def get_db():
    db = mysql.connector.connect(host="localhost",
                                 user ="root",
                                 password = 'ali109110',
                                 database ="SMART_ADVISOR")
    return db

dept_name_mapping = {
    'Political Science and International Relations': 'Political Science and International Relations (English)',
    'Psychology': 'Psychology (English)',
    'Sociology': 'Sociology (English)',
    'Philosophy': 'Philosophy (English)',
    'History': 'History (English)',
    'Turkish Language and Literature': 'Turkish Language and Literature',
    'English Language and Literature': 'English Language and Literature (English)', 
    'Translation and Interpretation': 'Translation and Interpretation (English)', 
    'Industrial Engineering': 'Industrial Engineering (English)',
    'Computer Science and Engineering': 'Computer Science and Engineering (English)',
    'Electrical and Electronics Engineering': 'Electrical and Electronics Engineering (English)',
    'Civil Engineering': 'Civil Engineering (English)',
    'Mechanical Engineering': 'Mechanical Engineering (English)',
    'Management': 'Management (English)', 
    'International Trade and Management': 'International Trade and Management (English)', 
    'Entrepreneurship': 'Entrepreneurship (Turkish)', 
    'Management Information Systems': 'Management Information Systems (Turkish)',
    'Economics': 'Economics (English)', 
    'International Finance': 'International Finance (English)',
    'Architecture': 'Architecture (English)',
    'Interior Architecture and Environmental Design': 'Interior Architecture and Environmental Design (Turkish)',
    'Industrial Design': 'Industrial Design (English)',
    'Cinema and Television': 'Cinema and Television (English)', 
    'Public Relations and Advertising': 'Public Relations and Advertising (Turkish)',
    'New Media and Communication': 'New Media and Communication (Turkish)', 
    'School of Islamic Studies': 'Islamic Studies (English)', 
    'School of Law': 'Law',
    'Public Relations and Publicity': 'Public Relations and Publicity (Turkish)',
    'Social Services': 'Social Services (Turkish)',
    'Occupational Health and Safety': 'Occupational Health and Safety (Turkish)',
    'Construction Technology': 'Construction Technology (Turkish)',
    'Photography and Videography': 'Photography and Videography (Turkish)',
    'Justice': 'Justice (Turkish)',
    'Justice (Evening education)': 'Justice (Evening Education) (Turkish)',
    'Computer Programming': 'Computer Programming (Turkish)',
    'Computer Programming (Evening education)': 'Computer Programming (Evening Education) (Turkish)',
    'Child Development': 'Child Development (Turkish)',
    'Child Development (Evening education)': 'Child Development (Evening Education) (Turkish)',
    'Graphic Design': 'Graphic Design (Turkish)',
    'Graphic Design (Evening education)': 'Graphic Design (Evening Education) (Turkish)'
}

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(executable_path=os.getcwd()+'/Smart-Advisor/flaskr/drivers/chromedriver', options=chrome_options)
    return driver

def profile_parser(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    email = soup.find('div', {'class': 'person-info'}).text.split()
    if len(email) == 1:
        email = email[0].strip()
        return email

def fetch_academic_staff(url):
    db = get_db()
    cursor = db.cursor()
    driver = setup_driver()
    driver.get(url)
    driver.implicitly_wait(10)
    elements = driver.find_elements_by_class_name('academic-staff-content')
    for element in elements:
        staff_name = element.find_element_by_class_name('academic-staff-name').text
        if 'INSTRUCTOR' in staff_name or 'RA' in staff_name:
            staff_name = ' '.join(staff_name.split()[1:]).strip()
        else:
            staff_name = staff_name.split('.')[-1].strip()
        staff_dept = element.find_element_by_class_name('academic-staff-department').text.strip()
        if staff_dept in dept_name_mapping:
            print(staff_name, staff_dept)
            profile_link = element.find_element_by_xpath('..').find_element_by_xpath('..').get_attribute('href')
            email = profile_parser(profile_link)
            if email != None:
                cursor.execute("INSERT INTO instructor (instructor_email, instructor_name) "
                            "VALUES (%s, %s);", (email, staff_name))
                cursor.execute("INSERT INTO instructor_department (instructor_email, department_name) "
                            "VALUES (%s, %s);", (email, dept_name_mapping[staff_dept]))
    db.commit()

fetch_academic_staff('https://www.sehir.edu.tr/en/academics/academic-staff')
