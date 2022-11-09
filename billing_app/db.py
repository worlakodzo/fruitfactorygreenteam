import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="billdb"
)

mycursor = connection.cursor()

#0.0.0.0: