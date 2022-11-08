import mysql.connector

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="root",
    database="billdb",
    port=3307
)

mycursor = connection.cursor()