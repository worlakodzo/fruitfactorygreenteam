# IMPORTS
import csv
import json
import sys
from datetime import datetime

import MySQLdb.cursors
from calculateNeto import sum_container_weights
from flask import Flask, jsonify, request, session
from flask_mysqldb import MySQL

app = Flask(__name__)

# Just a little alteraiton of this to the main db on the server
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'weight_app'

mysql = MySQL(app)


@app.route("/weight", methods=["POST"])
def get_weight():
    data = []
    bruto = None
    neto = None
    resp = None
    if request.method == "POST":
        json_data = request.get_json()
        direction = json_data["direction"]
        truck = json_data["truck"]
        if len(truck) == 0:
            truck = "na"
        containers = json_data["containers"]
        weight = json_data["weight"]
        force = json_data["force"]
        produce = json_data["produce"]

        # Date and time of saving the weight data
        date = datetime.now()

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        if direction == "in":
            #Check previous session of the truck
            qry = f'SELECT * FROM transactions WHERE truck = "{truck}" order by id DESC LIMIT 1'
            cursor.execute(qry)
            resp = cursor.fetchone()
            if resp["direction"]=="in" and not force:
                resp = jsonify({"success": False, "message": "IN-IN error"})
                resp.status_code=404
                return resp  

            elif resp["direction"]=="in" and force:
                # DIRECTION ( <in> & force=True)  after <in> ::: --> Saves the data 
                cursor.execute("UPDATE transactions SET produce=%s, containers=%s,  bruto=%s,  datetime=%s WHERE id=%s ",(produce,containers,weight,date, resp["id"]))
                mysql.connection.commit()
                record_id = resp["id"]
                bruto = weight

                response = jsonify({"id": record_id, "truck": truck,  "bruto": bruto})
                response.status_code=200
                return response


            else:
                cursor.execute('INSERT INTO transactions  (direction, truck, containers, bruto, truckTara, produce, datetime, neto) VALUES(%s, %s, %s, %s, %s,%s,%s,%s)',
                           (direction, truck, containers, weight, neto, produce, date, neto))
                record_id = cursor.lastrowid
                mysql.connection.commit()
                bruto = weight
                resp = {"id": record_id, "truck": truck, "bruto": bruto}



        # DIRECTION <out>
        elif direction == "out":
            # select * from getLastRecord ORDER BY id DESC LIMIT 1;
            qry = f'SELECT * FROM transactions WHERE truck = "{truck}" order by id DESC LIMIT 1'
            cursor.execute(qry)
            resp = cursor.fetchone()

            # DIRECTION <out> FOLLOWED BY None:  Error
            if resp is None:
                resp = jsonify({"success": False, "message": "OUT-NONE error"})
                resp.status_code=404
                return resp

            # DIRECTION <out> FOLLOWED BY EITHER (<out> & force=True) OR <in>
            elif (resp["direction"] == "out" and force) or resp["direction"]=="in":
                #Converting the ids of the containers into tuple with distinct elements hence the set
                c_ids = tuple(x for x in resp['containers'].split(','))

                # UPDATE TRUNSACTION DATA

                qry = f"SELECT * FROM containers_registered  WHERE container_id IN {c_ids}"
                cursor.execute(qry)
                containers = cursor.fetchall()
                neto = sum_container_weights(containers)

                update_query = f"UPDATE transactions SET neto={neto}, truckTara={weight} WHERE id={resp.get('id')}"
                cursor.execute(update_query)
                mysql.connection.commit()
                record_id = resp["id"]
                bruto = resp["bruto"]

                response = jsonify({"id": record_id, "truck": truck, 
                    "bruto": bruto, "truckTara": weight, "neto": neto if neto != 0 else "na"})
                response.status_code=200
                return response
            

            # DIRECTION <out> FOLLOWED BY ( <out> & force=false )  --->  This generates and error
            elif resp["direction"] == "out" and not force:
                resp = jsonify({"success": False, "message": "OUT-OUT error"})
                resp.status_code=404
                return resp

            else:
                resp= jsonify({"success": "False", "message": "Contact your administrator on this"})
                resp.status_code=500
                return resp

        elif direction == "none":
            # FETCHING PREVIOUS DATA OF THE truck and CHECKING DIRECTION
            qry = f'SELECT * FROM transactions WHERE truck = "{truck}" order by id DESC LIMIT 1'
            cursor.execute(qry)
            resp = cursor.fetchone()

            # DIRECTION <none> AFTER PREVIOUS DIRECTION <in>    ---> Error
            if resp["direction"]=="in":
                resp = jsonify({"success": False, "message": "IN-NONE error"})
                resp.status_code=404
                return resp
            
            # DIRECTION <none> AFTER ANY OTHER DIRECTION ---> Saves data in database
            cursor.execute('INSERT INTO transactions  (direction, truck, containers, bruto, truckTara, produce, datetime, neto) VALUES(%s, %s, %s, %s, %s,%s,%s,%s)',
                           (direction, truck, containers, weight, neto, produce, date, neto))
            record_id = cursor.lastrowid
            mysql.connection.commit()
            bruto = weight
            resp = {"id": record_id, "truck": truck, "bruto": bruto}

            return resp



         # Data structure of JSON format
        # Converts your data strcuture into JSON format
        reponse = jsonify(resp)
        reponse.status_code = 200  # Provides a response status code of 202 which is "Accepted"
        return reponse  # Returns the HT

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

# This function saves the container records in the DB
def save_container_record(c_id, c_weight, c_unit):
    try:

        print(c_id, c_unit, c_weight)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            'INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)', (c_id, c_weight, c_unit))
        mysql.connection.commit()
    except Exception as e:
        print(e)

# Reads line by lines the container records to be saved
def read_file_save(a, ext):
    sum = 0
    unit = None

    # Reading csv
    if ext == "csv":
        # When unit is in kg
        try:
            for i in a:
                c_weight = int(i.get('kg')) if i.get('kg') != None else None
                c_unit = "kg"
                c_id = i['id']
                save_container_record(c_id, c_weight, c_unit)
                sum += int(i['kg'])
            unit = 'kg'
        # When unit is in lbs
        except Exception as e:
            print(e)
            for i in a:
                c_weight = int(i.get('lbs')) if i.get('lbs') != None else None
                c_unit = "lbs"
                c_id = i['id']
                sum += int(i['lbs'])
                save_container_record(c_id, c_weight, c_unit)
            unit = 'lbs'
        return sum, unit
    # Reading json file
    elif ext == "json":
        for i in a:
         
            c_unit = i["unit"]
            c_weight = int(i.get('weight')) if i.get('weight') != None else None
            c_id = i['id']
            save_container_record(c_id, c_weight, c_unit)
            sum += int(i['weight'])
        unit = i['unit']
        return sum, unit


@app.route("/batch-weight/<file_name>", methods=["POST"])
def get_batch_weight(file_name):

    # Getting extension of file
    extension = (file_name.split('.'))[1]

    data = None

    try:  # Trying to read the file
        with open(f"./in/{file_name}", 'r') as file:
            if extension == "csv":
                data = [{k: v for k, v in reader.items()}
                        for reader in csv.DictReader(file, skipinitialspace=True)]
                print(data)
            elif extension == "json":
                data = json.load(file)

        # Getting sum of the sum of weight from the containers read from the file.
        sum, unit = read_file_save(data, extension)

        response= jsonify(success=True)
        response.status_code=200
        return response
    # Throwing an exception because file read failed...
    except IOError as e:
        print(e)
        resp = jsonify(
            "File not found, better check the extention or filename")
        resp.status_code = 404
        return resp


@app.route("/unknown")
def get_unknown():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    qry = ('SELECT * FROM containers_registered where weight is null')

    cursor.execute(qry)
    data = cursor.fetchall()
    response = jsonify(data)
    response.status_code = 200
    return response


if __name__ == "__main__":
    app.run()
