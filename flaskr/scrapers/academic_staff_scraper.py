import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  

parent = os.path.normpath(os.getcwd() + os.sep + os.pardir)
os.chdir(parent)

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument('window-size=1920x1080')
    driver = webdriver.Chrome(executable_path=os.getcwd()+'/Smart-Advisor/flaskr/drivers/chromedriver', options=chrome_options)
    return driver

def fetch_academic_staff(url):
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

fetch_academic_staff('https://www.sehir.edu.tr/en/academics/academic-staff')

