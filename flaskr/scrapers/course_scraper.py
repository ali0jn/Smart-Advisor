import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.common.exceptions import StaleElementReferenceException, ElementClickInterceptedException
import mysql.connector

parent = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.chdir(parent)

def get_db():
    db = mysql.connector.connect(host="localhost",
                                 user ="root",
                                 password = 'ali109110',
                                 database ="SMART_ADVISOR")
    return db

def setup_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(executable_path=os.getcwd()+'/Smart-Advisor/flaskr/drivers/chromedriver', options=chrome_options)
    return driver

def get_program_page(dept_name, electric_engr=False, architecture=False):
    driver = setup_driver()
    if electric_engr:
        url = 'https://www.sehir.edu.tr/tr/akademik/muhendislik-ve-doga-bilimleri-fakultesi/elektrik-ve-elektronik-muhendisligi/ders-plani'
    elif architecture and dept_name == 'Architecture Department (in Turkish)':
        url = 'https://www.sehir.edu.tr/en/academics/school-of-architecture-and-design/architecture/architecture-in-turkish/curriculum'
    elif architecture and dept_name == 'Architecture Department (in English)':
        url = 'https://www.sehir.edu.tr/en/academics/school-of-architecture-and-design/architecture/architecture-in-english/curriculum'
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
    elif dept_name == 'Architecture Department (in Turkish)' or dept_name == 'Architecture Department (in English)':
        driver = get_program_page(dept_name, architecture=True)
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
            course_details.extend(fetch_course_details(cat, 'Required'))
        
        elif fetch_electives and not id_.startswith(('1', '2', '3', '4', '5', '6', '7', '8')):
            panel = cat.find_elements_by_xpath('.//div/h4/span')
            type_ = panel[0].text
            panel[0].click()
            course_details.extend(fetch_course_details(cat, type_))

    driver.close()
    return course_details

dept_name_mapping = {
    'Political Science and International Relations Department (in Turkish)': 'Political Science and International Relations (Turkish)',
    'Political Science and International Relations Department (in English)': 'Political Science and International Relations (English)',
    'Psychology Department (in Turkish)': 'Psychology (Turkish)',
    'Psychology Department (in English)': 'Psychology (English)',
    'Sociology Department': 'Sociology (English)',
    'Philosophy Department': 'Philosophy (English)',
    'History Department': 'History (English)',
    'Turkish Language and Literature Department': 'Turkish Language and Literature',
    'English Language and Literature Department': 'English Language and Literature (English)', 
    'Translation and Interpretation Department': 'Translation and Interpretation (English)', 
    'Industrial Engineering Department (in English)': 'Industrial Engineering (English)',
    'Industrial Engineering Department (in Turkish)': 'Industrial Engineering (Turkish)',
    'Computer Science and Engineering Department': 'Computer Science and Engineering (English)',
    'Electrical and Electronics Engineering Department': 'Electrical and Electronics Engineering (English)',
    'Civil Engineering Department': 'Civil Engineering (English)',
    'Mechanical Engineering Department': 'Mechanical Engineering (English)',
    'Management Department': 'Management (English)', 
    'International Trade and Management Department': 'International Trade and Management (English)', 
    'Entrepreneurship Department': 'Entrepreneurship (Turkish)', 
    'Management Information Systems Department': 'Management Information Systems (Turkish)',
    'Economics Department': 'Economics (English)', 
    'International Finance Department': 'International Finance (English)',
    'Architecture Department (in Turkish)': 'Architecture (Turkish)',
    'Architecture Department (in English)': 'Architecture (English)',
    'Interior Architecture and Environmental Design Department': 'Interior Architecture and Environmental Design (Turkish)',
    'Industrial Design Department': 'Industrial Design (English)',
    'Cinema and Television Department (in Turkish)': 'Cinema and Television (Turkish)',
    'Cinema and Television Department (in English)': 'Cinema and Television (English)', 
    'Public Relations and Advertising Department': 'Public Relations and Advertising (Turkish)',
    'New Media and Communication Department': 'New Media and Communication (Turkish)', 
    'Islamic Studies': 'Islamic Studies (English)', 
    'Law': 'Law',
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

departments = [
               'Political Science and International Relations Department (in Turkish)',
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
               'Electrical and Electronics Engineering Department',
               'Civil Engineering Department',
               'Mechanical Engineering Department',
               'Management Department', 
               'International Trade and Management Department', 
               'Entrepreneurship Department', 
               'Management Information Systems Department',
               'Economics Department', 
               'International Finance Department',
               'Architecture Department (in Turkish)',
               'Architecture Department (in English)',
               'Interior Architecture and Environmental Design Department',
               'Industrial Design Department',
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
               'Photography and Videography'
               ]
              
vocational_schools = [
                      'Justice',
                      'Justice (Evening education)',
                      'Computer Programming',
                      'Computer Programming (Evening education)',
                      'Child Development',
                      'Child Development (Evening education)',
                      'Graphic Design',
                      'Graphic Design (Evening education)'
                      ]

def insert_to_db(dept_list, fetch_required, fetch_electives, vocational_school):
    c = 0
    while c < len(dept_list):
        print('Now Fetching', dept_list[c])
        try:
            courses = fetch_courses(dept_list[c], fetch_required=fetch_required, fetch_electives=fetch_electives, vocational_school=vocational_school)
            db = get_db()
            cursor = db.cursor()
            for course in courses:
                if course[0] != '--' and course[0] != '':
                    course.insert(0, dept_name_mapping[dept_list[c]])
                    try:
                        cursor.execute("INSERT INTO course (course_id, title, credit, ects, theoritical_credit, practical_credit, course_year) "
                                       "VALUES (%s, %s, %s, %s, %s, %s, %s);", (course[1], course[2], int(course[7]), int(course[8]), int(course[5]), int(course[6]), int(course[1].split()[1][0])))
                    except mysql.connector.errors.IntegrityError:
                        pass

                    try:
                        cursor.execute("INSERT INTO course_department (course_id, department_name, course_type) "
                                       "VALUES (%s, %s, %s);", (course[1], course[0], course[3]))
                    except:
                        pass

                    try:
                        if course[4] != '':
                            pre_reqs = course[4].split(',')
                            for pre_req in pre_reqs:
                                pre_req = pre_req.strip()
                                cursor.execute(
                                    "INSERT INTO prerequisite (course_id, prereq_id) "
                                    "VALUES (%s, %s);", (course[1], pre_req))
                    except:
                        pass
            db.commit()
            print('Successful!')
            c += 1
        except (StaleElementReferenceException, ElementClickInterceptedException):
            print('Failed. Trying Again!')

insert_to_db(departments, True, False, False)
insert_to_db(departments, False, True, False)
insert_to_db(vocational_schools, True, False, True)
insert_to_db(vocational_schools, False, True, True)
