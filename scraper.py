import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


url = 'http://mysap.sehir.edu.tr'
chrome_options = Options()
# chrome_options.add_argument("--headless")  
# chrome_options.binary_location = '/Applications/Google Chrome   Canary.app/Contents/MacOS/Google Chrome Canary'  
driver = webdriver.Chrome(executable_path='/chrome/chromedriver', options=chrome_options)
driver.get(url)
username = driver.find_element_by_id('userNameInput')
username.send_keys('aliibrahimzada')
password = driver.find_element_by_id('passwordInput')
password.send_keys('Larkimarki109$#%')
driver.find_element_by_id('submitButton').click()
wait = WebDriverWait(driver, 14).until(EC.element_to_be_clickable((By.ID, '__tile3')))
wait.click()
wait = WebDriverWait(driver, 14).until(EC.element_to_be_clickable((By.ID, 'application-Student-MyInformation-component---worklist--iconTabAcademic-icon')))
wait.click()


for i in range(9, 5, -1):
    for k in range(8):
        try:
            course_grade = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, '__status{}-dynamicAcademicCourseTable{}-{}-text'.format(i-4, i-5, k))))
            course_code = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, '__identifier{}-dynamicAcademicCourseTable{}-{}-txt'.format(i, i-5, k))))            
            print(course_code.text, course_grade.text)
        except:
            pass

# ENGR 101
# '__identifier9-dynamicAcademicCourseTable4-0-txt'
# '__status5-dynamicAcademicCourseTable4-0-text'
# ENGR 105
# __identifier9-dynamicAcademicCourseTable4-1-txt
# __status5-dynamicAcademicCourseTable4-1-text



# ENGR 100
# __identifier8-dynamicAcademicCourseTable3-0-txt
# __status4-dynamicAcademicCourseTable3-0-text


