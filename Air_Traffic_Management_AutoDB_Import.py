import os
from sys import platform
import mysql.connector
try:
    global con,cursor
    print("Connecting to the MySQL DataBase...")
    con = mysql.connector.connect(
    host="localhost", user="root",
    password="")
    cursor = con.cursor()
    qry="create database dbms"
    cursor.execute(qry)
    con.commit()
    print("Starting the Importing process...")
    if platform == "linux" or platform == "linux2":
        print("Linux based OS detected.")
        print("Uploading the Database")
        os.system('sudo /opt/lampp/bin/mysql -u root dbms<airtrafficmanagementdb.sql')
        print("Uploading Done")
    elif platform == "win32":
        print("Windows based OS detected.")
        print("Uploading the Database")
        os.system('C:/xampp/mysql/bin/mysql -u root dbms<airtrafficmanagementdb.sql')
        print("Uploading Done")
    else:
        print("Other OS detected,Please install manually the required files.")
except Exception as e:
    print("Unable to connect to MySql Database,Check the Server Status")
    print("Can't connect to MySQL server on 'localhost:3306' (111 Connection refused)")
    raise e
