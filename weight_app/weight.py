#IMPORTS
from flask import Flask, request, jsonify, session
from datetime import datetime
from flask_mysqldb import MySQL
import MySQLdb.cursors
import csv, json
from read_file import *
import sys



app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'weight_app'

mysql = MySQL(app)




@app.route("/weight", methods=["POST", "GET"])
def get_weight():
    data = []
    bruto = None
    neto = None
    resp=None
    if request.method=="POST":
        json_data = request.get_json()
        direction = json_data["direction"]
        license = json_data["license"]
        if len(license)==0:
            license = "na"
        containers = json_data["containers"]
        weight = json_data["weight"]
        unit = json_data["unit"]
        force = json_data["force"]
   
        produce=json_data["produce"]

        # Date and time of saving the weight data
        date=datetime.now()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO tbl_weight  (direction, license, containers, weight, unit, produce, forced, date) VALUES(%s, %s, %s, %s, %s, %s,%s,%s)', (direction, license, containers, weight, unit, produce, force, date))    
        record_id = cursor.lastrowid
        mysql.connection.commit()

        if direction == "IN":
            bruto = weight
            resp = { "id": record_id, "truck": license, "bruto": bruto }

        elif direction == "OUT":
            neto = weight
            resp = { "id": record_id, "truck": license, "neto": neto }
        
         # Data structure of JSON format
        reponse = jsonify(resp) # Converts your data strcuture into JSON format
        
       
        reponse.status_code = 202 # Provides a response status code of 202 which is "Accepted" 

        return reponse # Returns the HT

    elif request.method=="GET":
        return "<h1>weight<h1>"
    return 404

@app.route("/batch-weight/<file_name>", methods=["POST"])
def get_batch_weight(file_name):

    # Getting extension of file
    extension=(file_name.split('.'))[1]
    
    data = None
    
    try: # Trying to read the file
        with open(f"./Samples/{file_name}", 'r') as file:
            if extension == "csv":
                    data = [{k:v for k,v in reader.items()} for reader in csv.DictReader(file, skipinitialspace=True)]
                    print(data)
            elif extension == "json":
                data = json.load(file)

        # Getting sum of the sum of weight from the containers read from the file.
        sum,unit=read_file(data, extension)

        return jsonify({"neto":sum, "unit":unit})
    # Throwing an exception because file read failed...
    except IOError as e:
        print(e)
        resp = jsonify("File not found, better check the extention or filename")
        resp.status_code=404
        return resp



if __name__=="__main__":
    app.run()

  