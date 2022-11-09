import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="mypd",
    database="billdb"
)

mycursor = connection.cursor()