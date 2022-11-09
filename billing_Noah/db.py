import mysql.connector

connection = mysql.connector.connect(
    host="localhost",
    user="root",
<<<<<<< HEAD:billing_Noah/db.py
    password="mypd",
    database="billdb"
=======
    password="root",
    database="billdb",
    port=3307
>>>>>>> d60316dd232916757de72238a2fa6c42ed6eae32:billing_app/db.py
)

mycursor = connection.cursor()