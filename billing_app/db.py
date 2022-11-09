import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="billdb",
    port=8879
)

mycursor = connection.cursor()

#0.0.0.0: