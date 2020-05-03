from flaskr.db import get_db

dept_info = {'Political Science and International Relations (English)': 'POLS',
             'Political Science and International Relations (Turkish)': 'SYS',
             'Psychology (Turkish)': 'PSI',
             'Psychology (English)': 'PSY',
             'Sociology (English)': 'SOC',
             'Philosophy (English)': 'PHIL',
             'History (English)': 'HIST',
             'Turkish Language and Literature': 'LIT',
             'English Language and Literature (English)': 'ELIT',
             'Translation and Interpretation (English)': 'TRI',
             'Industrial Engineering (English)': 'IE',
             'Industrial Engineering (Turkish)': 'EM',
             'Electrical and Electronics Engineering (English)': 'EE',
             'Computer Science and Engineering (English)': 'CS',
             'Civil Engineering (English)': 'CE',
             'Mechanical Engineering (English)': 'ME',
             'Management (English)': 'MGT',
             'International Trade and Management (English)': 'ITM',
             'Entrepreneurship (Turkish)': 'GIR',
             'Management Information Systems (Turkish)': 'YBS',
             'International Finance (English)': 'IF',
             'Economics (English)': 'ECON',
             'Cinema and Television (Turkish)': 'STV',
             'Cinema and Television (English)': 'CTV',
             'Public Relations and Advertising (Turkish)': 'HIL',
             'New Media and Communication (Turkish)': 'YMI',
             'Islamic Studies (English)': 'ISS',
             'Law': 'LAW',
             'Justice (Turkish)': 'ADP',
             'Justice (Evening Education) (Turkish)': 'ADP',
             'Computer Programming (Turkish)': 'BPP',
             'Computer Programming (Evening Education) (Turkish)': 'BPP',
             'Child Development (Turkish)': 'CGP',
             'Child Development (Evening Education) (Turkish)': 'CGP',
             'Photography and Videography (Turkish)': 'FKP',
             'Graphic Design (Turkish)': 'GTP',
             'Graphic Design (Evening Education) (Turkish)': 'GTP',
             'Construction Technology (Turkish)': 'ITP',
             'Occupational Health and Safety (Turkish)': 'ISP',
             'Social Services (Turkish)': 'SOP',
             'Public Relations and Publicity (Turkish)': 'HTP',
             'Interior Design (Turkish)': 'ICP'}

def insert_dept_names():
    db = get_db()
    cursor = db.cursor()
    for dept_name in dept_info:
        cursor.execute("INSERT INTO department (department_name, department_code) "
                       "VALUES(%s, %s);", (dept_name, dept_info[dept_name]))
    db.commit()

insert_dept_names()
