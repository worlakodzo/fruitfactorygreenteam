import mysql.connector
import socket
dbhost=socket.gethostbyname('billdb')
connection = mysql.connector.connect(

    host=dbhost,
    user="billing",
    password="billing1password",
    database="billdb",
    port=8879
)

mycursor = connection.cursor()

#0.0.0.0: