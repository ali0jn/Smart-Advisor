import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException

parent = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.chdir(parent)

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(executable_path=os.getcwd()+'/Smart-Advisor/drivers/chromedriver', options=chrome_options)
    return driver

def get_program_page(dept_name, electric_engr=False):
    driver = setup_driver()
    if electric_engr:
        url = 'https://www.sehir.edu.tr/tr/akademik/muhendislik-ve-doga-bilimleri-fakultesi/elektrik-ve-elektronik-muhendisligi/ders-plani'
    else:
        url = 'https://www.sehir.edu.tr/en/academics/all-programs'
    driver.get(url)
    driver.implicitly_wait(10)

    # closing modal 'biz bize yeteriz turkiyem'
    modal = driver.find_element_by_id('donationModal')
    modal.find_element_by_tag_name('button').click()

    if not electric_engr:
        driver.find_element_by_link_text(dept_name).click()
        driver.implicitly_wait(10)

    return driver

def get_vocational_school(dept_name, driver):
    elements = driver.find_elements_by_xpath("//a[@class='static menu-item ms-core-listMenu-item ms-displayInline ms-navedit-linkNode']/span/span")
    idx = 0
    dept_name = dept_name.split()
    if len(dept_name) > 2:
        dept_name[-1] = 'Education)'
        if len(dept_name) == 3:
            dept_name.insert(1, 'Program')
        else:
            dept_name.insert(2, 'Program')
    else:
        if len(dept_name) == 2:
            dept_name.insert(2, 'Program')
        else:
            dept_name.append('Program')

    dept_name = ' '.join(dept_name)
    
    while elements[idx].text != dept_name:
        idx += 1
        if idx == len(elements):
            idx = 0
    elements[idx].click()
    driver.implicitly_wait(10)
    return driver

def click_curriculum(curriculum, dept_name, vocational_school=False):
    driver = get_program_page(dept_name)

    if vocational_school:
        driver = get_vocational_school(dept_name, driver)

    elements = driver.find_elements_by_xpath("//a[@class='static menu-item ms-core-listMenu-item ms-displayInline ms-navedit-linkNode']/span/span")

    idx = 0
    while elements[idx].text != curriculum:
        idx +=1
        if idx == len(elements):
            idx = 0

    elements[idx].click()
    driver.implicitly_wait(10)
    return driver

def fetch_course_details(category, type_):
    course_details = []
    course_info = category.find_elements_by_css_selector('td.text-left')
    course_credits = category.find_elements_by_css_selector('td.text-center')
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
        course_details.append([course_code, course_title, type_, pre_req, theoritical, practical, course_credit, ects])
        counter_1 += 2
        counter_2 += 6
    return course_details

def fetch_courses(dept_name, fetch_required=True, fetch_electives=False, vocational_school=False):
    if dept_name == 'Electrical and Electronics Engineering Department':
        driver = get_program_page(dept_name, electric_engr=True)
    elif vocational_school:
        driver = click_curriculum('Curriculum', dept_name, vocational_school=True)
    else:
        driver = click_curriculum('Curriculum', dept_name)

    categories = driver.find_elements_by_xpath("//div[@class='panel panel-default']")
    course_details = []
    for cat in categories:
        id_ = cat.get_attribute('id')
        if fetch_required and id_.startswith(('1', '2', '3', '4', '5', '6', '7', '8')):
            type_ = 'Required'
            course_details = fetch_course_details(cat, 'Required')
        
        elif fetch_electives and not id_.startswith(('1', '2', '3', '4', '5', '6', '7', '8')):
            panel = cat.find_elements_by_xpath('.//div/h4/span')
            type_ = panel[0].text
            panel[0].click()
            course_details = fetch_course_details(cat, type_)

    driver.close()
    return course_details

# df = pd.DataFrame(columns=['Department Name', 'Course Code', 'Course Title', 'Type', 'Prerequisites', 'Theoritical', 'Practical', 'Course Credits', 'ECTS'])
df = pd.read_csv('course_details.csv')

departments = ['Political Science and International Relations Department (in Turkish)',
               'Political Science and International Relations Department (in English)',
               'Psychology Department (in Turkish)', 
               'Psychology Department (in English)',
               'Sociology Department', 
               'Philosophy Department',
               'History Department', 
               'Turkish Language and Literature Department',
               'English Language and Literature Department', 
               'Translation and Interpretation Department', 
               'Industrial Engineering Department (in English)',
               'Industrial Engineering Department (in Turkish)',
               'Computer Science and Engineering Department',
            #    'Electrical and Electronics Engineering Department',
               'Civil Engineering Department',
               'Mechanical Engineering Department',
               'Management Department', 
               'International Trade and Management Department', 
               'Entrepreneurship Department', 
               'Management Information Systems Department',
               'Economics Department', 
               'International Finance Department', 
               'Cinema and Television Department (in Turkish)',
               'Cinema and Television Department (in English)', 
               'Public Relations and Advertising Department',
               'New Media and Communication Department', 
               'Islamic Studies', 
               'Law',
               'Public Relations and Publicity',
               'Social Services',
               'Occupational Health and Safety',
               'Construction Technology',
               'Photography and Videography']
               
vocational_schools = ['Justice',
                      'Justice (Evening education)',
                      'Computer Programming',
                      'Computer Programming (Evening education)',
                      'Child Development',
                      'Child Development (Evening education)',
                      'Graphic Design',
                      'Graphic Design (Evening education)']

c = 0
while c < len(vocational_schools):
    try:
        courses = fetch_courses(vocational_schools[c], fetch_required=False, fetch_electives=True, vocational_school=True)
        for course in courses:
            if course[0] != '--' and course[0] not in df.iloc[:, 1] and course[1] not in df.iloc[:, 2]:
                course.insert(0, vocational_schools[c])
                df.loc[len(df)] = course
        print(vocational_schools[c], 'Successful!')
        c += 1
    except (StaleElementReferenceException, ElementClickInterceptedException):
        print('Failed. Trying Again!')


df.to_csv('course_details_1.csv', index=False)
