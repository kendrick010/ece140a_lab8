# Import necessary mysql libraries
import mysql.connector as mysql
import os
from dotenv import load_dotenv

# Loads all details from the "credentials.env"
load_dotenv('Challenge/credentials.env')
# Environment Variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

# MySQL cursor
db = mysql.connect(host=db_host, user=db_user, password=db_pass)
cursor = db.cursor()

def setup():
    cursor.execute("CREATE DATABASE IF NOT EXISTS lab8;")
    cursor.execute("USE lab8")
    cursor.execute("DROP TABLE IF EXISTS objects")
    cursor.execute("DROP TABLE IF EXISTS found_objects")

def objects():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS objects(
        object_name varchar(32)
        Hue INT NOT NULL,
        Saturation INT NOT NULL,
        Brightness INT NOT NULL,
        Contours INT NOT NULL
        );
    """)

def found_objects():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS found_objects(
        object_name varchar(32) NOT NULL,
        address varchar(50) NOT NULL
        );
    """)

if __name__ == '__main__':
    setup()
    objects()
    found_objects()