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


def fetch_timetable(url):
    driver = setup_driver()
    driver.get(url)
    driver.implicitly_wait(10)
    elements = driver.find_elements_by_tag_name('tr')
    for i in range(1, len(elements)):
        sub_elements = elements[i].find_elements_by_tag_name('td')
        for j in range(len(sub_elements)):
            print(sub_elements[j].text.strip())

fetch_timetable('https://www.sehir.edu.tr/en/Announcements/2019_2020_Akademik_Yili_Bahar_Donemi_Ders_Programi')
