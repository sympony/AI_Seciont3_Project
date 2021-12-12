import os
import sqlite3
import csv
from datetime import datetime

DATABASE_PATH = os.path.join(os.getcwd(), 'BikeData.db')

conn = sqlite3.connect(DATABASE_PATH)
cur = conn.cursor()

# Table Create
my_table = """CREATE Table Bike (
    Id INTEGER NOT NULL Primary Key AUTOINCREMENT,
    Date DATETIME, Hour INTEGER,
    Temperature FLOAT, Humidity FLOAT,
    WIndspeed FLOAT, Visibility INTEGER,
    Dewpoint FLOAT, Solarrad FLOAT,
    Rain FLOAT, Snow FLOAT,
    Season VARCHAR(16),
    Holiday VARCHAR(16),
    Workingday VARCHAR(8),
    Rental_Count INTEGER
)"""
drop_table = "DROP TABLE IF EXISTS Bike;"

cur.execute(drop_table)
cur.execute(my_table)
with open('SeoulBikeData.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    next(csvfile)
    for row in reader:
        cur.execute("""INSERT INTO Bike('Date', 'Hour', 'Temperature', 'Humidity', 'WIndspeed', 'Visibility', 'Dewpoint', 'Solarrad', 'Rain', 'Snow', 'Season', 'Holiday', 'Workingday', 'Rental_Count') 
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
        (str(datetime.strptime(row[0], '%d/%m/%Y').date()), 
        row[2], row[3], row[4], row[5], row[6], 
        row[7], row[8], row[9], row[10], row[11], 
        row[12], row[13], row[1]))

conn.commit()
cur.close()
conn.close()