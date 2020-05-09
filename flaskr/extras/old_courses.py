import mysql.connector

def get_db():
    db = mysql.connector.connect(host="localhost",
                                 user ="root",
                                 password = 'ali109110',
                                 database ="SMART_ADVISOR")
    return db

db = get_db()
cursor = db.cursor()

import pandas as pd
df = pd.read_csv('extracted_dataset.csv')

for i in df.index:
    if df.iloc[i, 19] > 4:
        continue

    try:
        cursor.execute("INSERT INTO student (student_google_id) values ({});".format(df.iloc[i, 2]))
    except mysql.connector.errors.IntegrityError:
        pass
    
    try:
        cursor.execute("INSERT INTO course (course_id, title, credit, ects, theoritical_credit, practical_credit, course_year) "
                       "values (%s, %s, %s, %s, %s, %s, %s);", (df.iloc[i, 0], df.iloc[i, 1], int(df.iloc[i, 17]), int(df.iloc[i, 18]), int(df.iloc[i, 15]), int(df.iloc[i, 16]), int(df.iloc[i, 19])))
    
    except mysql.connector.errors.IntegrityError:
        pass   
    yr = df.iloc[i, 14].split('-')[0].strip()
    sem = df.iloc[i, 14].split('-')[1].strip()
    grade = df.iloc[i, 5].strip()
    try:
        cursor.execute("INSERT INTO section (section_id, semester, section_year, course_id) values (%s, %s, %s, %s);", ('01', sem, int(yr), df.iloc[i, 0]))
    except mysql.connector.errors.IntegrityError:
        pass
    cursor.execute("INSERT INTO takes values (%s, %s, %s, %s, %s, %s);", ('01', sem, int(yr), df.iloc[i, 0], str(df.iloc[i, 2]), grade))
    
db.commit()
