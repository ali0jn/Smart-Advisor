import os
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from flaskr.user import Student

parent = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.chdir(parent)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(executable_path=os.getcwd()+'/Smart-Advisor/flaskr/drivers/chromedriver', options=chrome_options)
    return driver

def login(student_username, student_password):
    driver = setup_driver()
    url = 'http://my.sehir.edu.tr'
    driver.get(url)
    driver.implicitly_wait(10)
    username = driver.find_element_by_id('userNameInput')
    username.send_keys(student_username)
    password = driver.find_element_by_id('passwordInput')
    password.send_keys(student_password)
    driver.find_element_by_id('submitButton').click()
    driver.implicitly_wait(10)
    return driver

def change_language(username, password):
    driver = login(username, password)
    driver.get('https://my.sehir.edu.tr/en')
    driver.implicitly_wait(10)
    driver.find_element_by_id('ctl00_ctl53_g_6a8b8970_2f33_4e2b_9f60_c033bd925c78_csr11_pictureOnTop_dataContainer').click()
    driver.implicitly_wait(10)
    return driver

def fetch_sap_data(username, password, std_google_id):
    driver = change_language(username, password)
    home_page = driver.current_url
    wait = WebDriverWait(driver, 14).until(EC.element_to_be_clickable((By.ID, '__tile3')))
    wait.click()    
    department = driver.find_element_by_xpath("//div[@id='__panel0']/div").text.strip()
    dept_dict = get_department(department)
    advisor = driver.find_element_by_xpath("//div[@id='__panel1']/div").text.split('(Advisor)')[0].strip()
    details = driver.find_element_by_xpath("//div[@id='application-Student-MyInformation-component---worklist--ObjectPageLayout-OPHeaderContent']").text.split('\n')
    student_number = details[0].strip()
    standing = details[2].split()[0].strip()
    semester_of_student = details[2].split()[1][2].strip()
    general_gpa = details[6].split()[-1].strip()
    general_credit = details[7].split()[-1].strip().split('.')[0]
    general_ects = details[8].split()[-1].strip().split('.')[0]
    student_object = Student.get(std_google_id)
    student_object.add_department(dept_dict, std_google_id)
    student_object.update_profile(student_number, semester_of_student, advisor, standing, general_gpa, general_credit, general_ects, std_google_id)
    wait = WebDriverWait(driver, 14).until(EC.element_to_be_clickable((By.ID, 'application-Student-MyInformation-component---worklist--iconTabAcademic-icon')))
    wait.click()
    driver.implicitly_wait(10)
    return driver, home_page

def fetch_transcript(username, password, std_google_id):
    driver, home_page = fetch_sap_data(username, password, std_google_id)
    semesters = driver.find_elements_by_xpath('//div[@id="__xmlview2--PanelRegTables-content"]/div[@role="toolbar"]')
    courses = driver.find_elements_by_xpath('//div[@id="__xmlview2--PanelRegTables-content"]/div[@role="application"]')
    for i in range(len(semesters)):
        sem = semesters[i].text.split('\n')
        if sem[1] == 'Continuing Student':
            year = sem[0].split()[0]
            semester_name = sem[0].split()[1]
            semester_courses = courses[i].text.split('\n')
            for j in range(4, len(semester_courses), 3):
                if len(semester_courses[j+2]) > 4:
                    course_code = semester_courses[j]
                    grade = semester_courses[j+2].split()[0].strip()
                    Student.add_transcript('01', semester_name, year, course_code, std_google_id, grade)
                else:
                    course_code = semester_courses[j]
                    current_sem, current_year = semester_name, year
                    Student.add_current_semester('01', semester_name, year, course_code, std_google_id)
    driver.get(home_page)
    driver.implicitly_wait(10)
    fetch_current_semester(driver, current_sem, current_year, std_google_id)               

def get_department(dept):
    dept_dict = {}
    main_prg, d_major, minor = '', '', ''
    for i in range(len(dept)):
        if dept[i:i+10] == "(Main Prg)":
            main_prg = dept[:i+10].split('(Main Prg)')[0].strip()
            start_idx = i+11
        elif dept[i:i+7] == "(Minor)":
            minor = dept[start_idx:i+7].split('(Minor)')[0].strip()
            start_idx = i+8
        elif dept[i:i+14] == "(Double Major)":
            d_major = dept[start_idx:i+14].split('(Double Major)')[0].strip()
            start_idx = i+15
    
    if main_prg != '':
        dept_dict['Main Prg'] = main_prg
    if d_major != '':
        dept_dict['Double Major'] = d_major
    if minor != '':
        dept_dict['Minor'] = minor
    return dept_dict

def fetch_current_semester(driver, semester, year, std_google_id):
    wait = WebDriverWait(driver, 14).until(EC.element_to_be_clickable((By.ID, '__tile0')))
    wait.click()
    driver.implicitly_wait(10)
    my_courses = driver.find_element_by_xpath('//span[@id="application-ModuleBooking-display-component---object--itfMyCourses-icon"]')
    my_courses.click()
    driver.implicitly_wait(10)
    current_semester = driver.find_element_by_xpath('//*[@id="__table0"]').text.split('\n')
    for i in range(len(current_semester)):
        string = current_semester[i].strip()
        matches = re.findall(r'\d\d\d\s\d\d', string)
        if len(matches) == 1:
            course_code = ' '.join(string.split()[:2])
            section = string.split()[-1]
            Student.update_current_semester(section, semester, year, course_code, std_google_id)
