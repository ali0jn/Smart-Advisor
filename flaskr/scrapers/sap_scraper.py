import os
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
    wait = WebDriverWait(driver, 14).until(EC.element_to_be_clickable((By.ID, '__tile3')))
    wait.click()    
    department = driver.find_element_by_xpath("//div[@id='__panel0']/div").text.strip()[:-11]
    advisor = driver.find_element_by_xpath("//div[@id='__panel1']/div").text.strip()[:-10]
    details = driver.find_element_by_xpath("//div[@id='application-Student-MyInformation-component---worklist--ObjectPageLayout-OPHeaderContent']").text.split('\n')
    student_number = details[0].strip()
    standing = details[2].split()[0].strip()
    semester_of_student = details[2].split()[1][2].strip()
    general_gpa = details[6].split()[-1].strip()
    general_credit = details[7].split()[-1].strip().split('.')[0]
    general_ects = details[8].split()[-1].strip().split('.')[0]
    student_object = Student.get(std_google_id)
    student_object.update_profile(student_number, semester_of_student, advisor, standing, general_gpa, general_credit, general_ects, std_google_id)
    wait = WebDriverWait(driver, 14).until(EC.element_to_be_clickable((By.ID, 'application-Student-MyInformation-component---worklist--iconTabAcademic-icon')))
    wait.click()
    driver.implicitly_wait(10)
    return driver

def fetch_transcript(username, password, std_google_id):
    driver = fetch_sap_data(username, password, std_google_id)
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
                    course_name = semester_courses[j+1]
                    grade = semester_courses[j+2].split()[0].strip()
                    credit = semester_courses[j+2].split()[1].strip()
                    print(course_code, course_name, grade, credit, year, semester_name)

