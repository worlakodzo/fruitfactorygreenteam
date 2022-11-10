import mysql.connector
import socket
dbhost=socket.gethostbyname('billdb')
connection = mysql.connector.connect(
    host=dbhost,
    user="billing",
    password="billing1password",
    database="billdb",
    port=3306
)

mycursor = connection.cursor()