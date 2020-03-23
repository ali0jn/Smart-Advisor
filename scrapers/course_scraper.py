import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.common.exceptions import StaleElementReferenceException

parent = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.chdir(parent)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(executable_path=os.getcwd()+'/Smart-Advisor/drivers/chromedriver', options=chrome_options)
    return driver

def fetch_department(dept_name):
    driver = setup_driver()
    url = 'https://www.sehir.edu.tr/en/academics/all-programs'
    driver.get(url)
    driver.implicitly_wait(10)
    driver.find_element_by_link_text(dept_name).click()
    driver.implicitly_wait(10)
    elements = driver.find_elements_by_xpath("//a[@class='static menu-item ms-core-listMenu-item ms-displayInline ms-navedit-linkNode']/span/span")
    curriculum_tag = ''
    course_details = []
    for a_tag in elements:
        if a_tag.text == 'Curriculum':
            curriculum_tag = a_tag
    curriculum_tag.click()
    driver.implicitly_wait(10)
    categories = driver.find_elements_by_xpath("//div[@class='panel panel-default']")
    for cat in categories:
        id_ = cat.get_attribute('id')
        if not id_.startswith(('1', '2', '3', '4', '5', '6', '7', '8')):
            panel = cat.find_elements_by_xpath('.//div/h4/span')
            panel[0].click()
        course_info = cat.find_elements_by_css_selector('td.text-left')
        course_credits = cat.find_elements_by_css_selector('td.text-center')
        counter_1 = 0
        counter_2 = 0
        for i in range(len(course_info)//2):
            course_code = course_info[counter_1].text
            course_title = course_info[counter_1+1].text
            pre_req = course_credits[counter_2].text
            theoritical = course_credits[counter_2+1].text
            practical = course_credits[counter_2+2].text
            course_credit = course_credits[counter_2+3].text
            ects = course_credits[counter_2+4].text
            course_details.append([course_code, course_title, pre_req, theoritical, practical, course_credit, ects])
            counter_1 += 2
            counter_2 += 6
    driver.close()
    return course_details

df = pd.DataFrame(columns=['Department Name', 'Course Code', 'Course Title', 'Prerequisites', 'Theoritical', 'Practical', 'Course Credits', 'ECTS'])

departments = ['Political Science and International Relations Department (in English)', 'Psychology Department (in English)',
              'Sociology Department', 'Philosophy Department', 'History Department', 'Turkish Language and Literature Department',
              'English Language and Literature Department', 'Translation and Interpretation Department', 'Industrial Engineering Department (in English)',
              'Computer Science and Engineering Department', 'Civil Engineering Department', 'Mechanical Engineering Department', 'Management Department', 
              'International Trade and Management Department', 'Entrepreneurship Department', 'Management Information Systems Department',
              'Economics Department', 'International Finance Department', 'Cinema and Television Department (in English)', 'Public Relations and Advertising Department',
              'New Media and Communication Department', 'Islamic Studies', 'Law']

c = 0
while c < len(departments):
    try:
        courses = fetch_department(departments[c])
        for course in courses:
            if course[0] != '--' and course[0] not in df.iloc[:, 1]:
                course.insert(0, departments[c])
                df.loc[len(df)] = course
        print(departments[c])
        c += 1
    except StaleElementReferenceException:
        print(departments[c])


df.to_csv('course_details.csv', index=False)
