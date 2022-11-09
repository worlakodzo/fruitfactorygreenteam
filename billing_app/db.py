import mysql.connector
import os

connection = mysql.connector.connect(
    host="127.0.0.1",
    user="billing",
    password="billing1password",
    database="billdb",
    port=3307
)

mycursor = connection.cursor()