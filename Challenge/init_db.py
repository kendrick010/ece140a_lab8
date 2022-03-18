# Import necessary mysql libraries
import mysql.connector as mysql
import os
from dotenv import load_dotenv

# Loads all details from the "credentials.env"
load_dotenv('credentials.env')
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
        object_name varchar(32),
        hue_lower INT NOT NULL,
        hue_upper INT NOT NULL,
        saturation_lower INT NOT NULL,
        saturation_upper INT NOT NULL,
        brightness_lower INT NOT NULL,
        brightness_upper INT NOT NULL,
        sides INT NOT NULL
        );
    """)
    query = "INSERT INTO objects (object_name, hue_lower, hue_upper, saturation_lower, saturation_upper, brightness_lower, brightness_upper, sides) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = [('red_hexagon', 0, 10, 150, 255, 20, 255, 5),
              ('red_hexagon', 160, 179, 100, 255, 20, 255, 5),
              ('green_square', 40, 75, 100, 255, 20, 255, 4),
              ('blue_triangle', 100, 125, 100, 255, 20, 255, 3)]
    cursor.executemany(query, values)
    db.commit()

def found_objects():
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS found_objects(
        object_name varchar(32) NOT NULL,
        address varchar(50) NOT NULL,
        text varchar(32)
        );
    """)

def main():
    setup()
    objects()
    found_objects()