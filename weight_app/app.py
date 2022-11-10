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
        truck = json_data["license"]
        if len(truck)==0:
            truck = "na"
        containers = json_data["containers"]
        weight = json_data["weight"]
   
        produce=json_data["produce"]

        # Date and time of saving the weight data
        date=datetime.now()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        if direction == "IN":
            cursor.execute('INSERT INTO transactions  (direction, truck, containers, bruto, truckTara, produce, datetime, neto) VALUES(%s, %s, %s, %s, %s,%s,%s,%s)', (direction, truck, containers, weight, neto, produce, date, neto))    
            record_id = cursor.lastrowid
            mysql.connection.commit()
            bruto = weight
            resp = { "id": record_id, "truck": truck, "bruto": bruto }

        elif direction == "OUT":
            neto = weight
            resp = { "id": record_id, "truck": truck, "neto": neto }
        
         # Data structure of JSON format
        reponse = jsonify(resp) # Converts your data strcuture into JSON format
        reponse.status_code = 202 # Provides a response status code of 202 which is "Accepted" 
        return reponse # Returns the HT

    # THE CODE BELOW HAS BEEN IMPLEMENTED BY NOBEL PERHAPS EVEN BETTER THERE SO USE THAT VERSION
    # elif request.method=="GET":
        # query = None
        # # Getting the parameters passed        
        # date_from = request.args.get('from', None)
        # date_to = request.args.get('to', None)
        # _filter = request.args.get('filter', None) # None here means there is no filter. It does not mean NONE which is a parameter

        # # Replacing default defaulf parameters with passed parameters if avaiilable
        # _from = date_from if date_from != None else datetime.today().replace(hour=0, minute=0, microsecond=0, second=0)
        # _to = date_to if date_to != None else datetime.now()


        # if _filter == None:
        #     query = f"SELECT * FROM tbl_weight WHERE date between {_from} AND {_to}"

        # else:
        #     query = ("SELECT * FROM tbl_weight WHERE direction= ,(upper(%s)) AND date between %s AND %s", str(_filter), _from, _to)

        # try:
        #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #     cursor.execute(query)    
        #     records = cursor.fetchall()
        # except IOError as e:
        #     print("Filter or date parameters might be wrong")
            
        #     resp = jsonify({"from": _from, "to": _to, "filter": request.args.get('filter')})
        #     resp.status_code=404
        #     return resp
             


        # return "<h1>weight<h1>"
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
        sum,unit=read_file_save(data, extension)

        return jsonify({"neto":sum, "unit":unit})
    # Throwing an exception because file read failed...
    except IOError as e:
        print(e)
        resp = jsonify("File not found, better check the extention or filename")
        resp.status_code=404
        return resp




if __name__=="__main__":
    app.run()

  