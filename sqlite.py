import sqlite3

connection = sqlite3.connect("student.db")
cursor = connection.cursor()

table_infos="""
create table STUDENTS(NAME VARCHAR(25),CLASS VARCHAR(25),
SECTION VARCHAR(25),MARKS INT)

"""


cursor.execute(table_infos)


cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('John Smith', '10th', 'A', 85)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Emma Wilson', '10th', 'B', 92)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Michael Brown', '11th', 'A', 78)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Sarah Davis', '11th', 'B', 95)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('James Johnson', '12th', 'A', 88)")
cursor.execute("INSERT INTO STUDENT (NAME, CLASS, SECTION, MARKS) VALUES ('Emily Taylor', '12th', 'B', 90)")

print("Data inserted successfully")
data = cursor.execute("SELECT * FROM STUDENT")
for row in data:
    
    print(row)
connection.commit()
connection.close()
