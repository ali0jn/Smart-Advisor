import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


parent = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.chdir(parent)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(executable_path=os.getcwd()+'/Smart-Advisor/drivers/chromedriver', options=chrome_options)
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

def fetch_sap_data(username, password):
    driver = change_language(username, password)
    driver.find_element_by_id('__tile3').click()
    driver.implicitly_wait(10)
    element = driver.find_element_by_id('__panel0')
    department = element.find_element_by_xpath("//div[@id='__panel0']/div").text.strip()[:-11]
    element = driver.find_element_by_id('__panel1')
    advisor = element.find_element_by_xpath("//div[@id='__panel1']/div").text.strip()[:-10]

    # driver.find_element_by_id('application-Student-MyInformation-component---worklist--iconTabAcademic-icon').click()
    # driver.implicitly_wait(10)

    # student_number = driver.find_element_by_id('__header1-innerTitle-content').text.strip()
    # element = driver.find_element_by_id('__label3-bdi').split()
    # standing = element[0].strip()
    # semester_of_student = element[1][2].strip()

    # for i in range(9, 5, -1):
    #     for k in range(8):
    #         try:
    #             course_grade = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, '__status{}-dynamicAcademicCourseTable{}-{}-text'.format(i-4, i-5, k))))
    #             course_code = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, '__identifier{}-dynamicAcademicCourseTable{}-{}-txt'.format(i, i-5, k))))            
    #             print(course_code.text, course_grade.text)
    #         except:
    #             pass

    return department, advisor
print(fetch_sap_data('aliibrahimzada', 'Larkimarki109$#%'))


# wait = WebDriverWait(driver, 14).until(EC.element_to_be_clickable((By.ID, '__tile3')))
# wait.click()
# wait = WebDriverWait(driver, 14).until(EC.element_to_be_clickable((By.ID, 'application-Student-MyInformation-component---worklist--iconTabAcademic-icon')))
# wait.click()


# for i in range(9, 5, -1):
#     for k in range(8):
#         try:
#             course_grade = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, '__status{}-dynamicAcademicCourseTable{}-{}-text'.format(i-4, i-5, k))))
#             course_code = WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, '__identifier{}-dynamicAcademicCourseTable{}-{}-txt'.format(i, i-5, k))))            
#             print(course_code.text, course_grade.text)
#         except:
#             pass

# print('Overall GPA', WebDriverWait(driver, 1).until(EC.element_to_be_clickable((By.ID, '__label5-bdi'))).text)

# # ENGR 101
# # '__identifier9-dynamicAcademicCourseTable4-0-txt'
# # '__status5-dynamicAcademicCourseTable4-0-text'
# # ENGR 105
# # __identifier9-dynamicAcademicCourseTable4-1-txt
# # __status5-dynamicAcademicCourseTable4-1-text



# # ENGR 100
# # __identifier8-dynamicAcademicCourseTable3-0-txt
# # __status4-dynamicAcademicCourseTable3-0-text


