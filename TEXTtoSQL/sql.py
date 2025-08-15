# This file is responsible for creating database.
import sqlite3

## Connect to SQLite database
connection = sqlite3.connect('student.db')

## Create a cursor object using the connection
cursor= connection.cursor()

## Create a table
table_info = """CREATE TABLE STUDENTS (
    NAME VARCHAR (25),CLASS VARCHAR (25), SECTION VARCHAR (25), MARKS INT 
);"""""
cursor.execute(table_info)

## Insert data into the table
cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, SECTION, MARKS) VALUES ('John Doe', '10', 'A', 85)")
cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, SECTION, MARKS) VALUES ('Jane Smith', '10', 'B', 90)")
cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, SECTION, MARKS) VALUES ('Alice Johnson', '9', 'A', 78)")
cursor.execute("INSERT INTO STUDENTS (NAME, CLASS, SECTION, MARKS) VALUES ('Bob Brown', '9', 'B', 62)")

## Display the data
print ("The inserted records are:")
data = cursor.execute("SELECT * FROM STUDENTS")

for row in data:
    print(row)

## Close the connection
connection.commit()
connection.close()