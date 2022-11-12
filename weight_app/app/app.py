from flask import Flask, jsonify, request, session
from flask_app import app
from db import mysql 
import datetime
import csv
import json
import sys 
from calculateNeto import sum_container_weights
 
 
@app.route('/')
def home():   
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM transactions")
    rows=cur.fetchall()
    resp=jsonify(rows)
    resp.status_code=200
    return resp

@app.route('/session/<id>')
def get_session(id):     
    id=int(id) 
    cur=mysql.connection.cursor()    
    results=cur.execute("SELECT direction,id,truck,bruto,truckTara,neto FROM transactions WHERE id LIKE %s",(id,))
    if results>0:
        session_details=cur.fetchall()   
        resp=jsonify(session_details)
        resp.status_code=200
        return resp
    resp=jsonify({"message":"session not found"})
    resp.status_code=404
    return resp

@app.route('/weight',methods=['POST']) 
def post_weight():
    data = []
    bruto = None
    neto = None
    resp = None 
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
    date = datetime.datetime.now()
    cursor = mysql.connection.cursor()


    # DIRECTION <in>
    if direction == "in":
        #Check previous session of the truck
        qry = f'SELECT * FROM transactions WHERE truck = "{truck}" order by id DESC LIMIT 1'
        cursor.execute(qry)
        resp = cursor.fetchone()

        # If truck has no previous record: -> Save the new data in the data base..
        if resp is None or resp["direction"]=="out" or resp["direction"]=="none":
            cursor.execute('INSERT INTO transactions  (direction, truck, containers, bruto, truckTara, produce, datetime, neto) VALUES(%s, %s, %s, %s, %s,%s,%s,%s)',
                        (direction, truck, containers, weight, neto, produce, date, neto))
            record_id = cursor.lastrowid
            mysql.connection.commit()
            bruto = weight
            resp = {"id": record_id, "truck": truck, "bruto": bruto}

        elif resp["direction"]=="in" and not force:
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

    # DIRECTION <none>
    elif direction == "none":
        # FETCHING PREVIOUS DATA OF THE truck and CHECKING DIRECTION
        qry = f'SELECT * FROM transactions WHERE truck = "{truck}" order by id DESC LIMIT 1'
        cursor.execute(qry)
        resp = cursor.fetchone()

        # DIRECTION <none> AFTER PREVIOUS DIRECTION <in>    ---> Error
        if  resp is not None and resp["direction"]=="in":
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

    return 404

# This function saves the container records in the DB
def save_container_record(c_id, c_weight, c_unit):
    try:

        print(c_id, c_unit, c_weight)
        cursor = mysql.connection.cursor()

        cursor.execute(
            'INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)', (c_id, c_weight, c_unit))
        mysql.connection.commit()
    except Exception as e:
        print(e)

# Reads line by lines the container records to be saved


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

def save_container_record(c_id, c_weight, c_unit):
    try:

        print(c_id, c_unit, c_weight)
        cursor = mysql.connection.cursor()
        # qry = ("INPUT INTO containers_registered(container_id, weight, unit) VALUES (%s, %s, %s,)", c_id, c_weight, c_unit)
        qry = ('INSERT INTO tbl_container (container_id, weight, unit) VALUES (%s, %s, %s)',
               (c_id, c_weight, c_unit))

        cursor.execute('INSERT INTO tbl_container (container_id, weight, unit) VALUES (%s, %s, %s)',
               (c_id, c_weight, c_unit))
        mysql.connection.commit()
        return qry
    except Exception as e:
        print(e)




@app.route('/weight')
def get_weight(): 
    cur=mysql.connection.cursor()        
    begin='0000-00-00 00:00:00.000000'         
    end=datetime.datetime.now() 
    
        
    if request.args.get('filter'):          
        if request.args.get('from'):
            begin=request.args.get('from')
            
        if request.args.get('to'): 
            end=request.args.get('to') 
                        
        directions=request.args.get('filter') 
        qry = f'SELECT id,direction,bruto,neto,produce,containers FROM transactions WHERE direction = "{directions}" AND datetime BETWEEN "{begin}" AND "{end}"'                                  
        results=cur.execute(qry)                   
        if results>0:
            transanction_Details=cur.fetchall()               
            resp=jsonify(transanction_Details)
            resp.status_code=200    
            return resp
    else:  
        qry = f'SELECT id,direction,bruto,neto,produce,containers FROM transactions WHERE datetime BETWEEN "{begin}" AND "{end}" '
               
        results=cur.execute(qry)    
        if results>0:                   
            transanction_Details=cur.fetchall() 
            resp=jsonify(transanction_Details)
            resp.status_code=200 
            return resp

    resp=jsonify({"message":"session not found"})
    resp.status_code=404
    return resp


def row_to_dict(row):
    temp_dict_list=['id','direction','bruto','neto','produce','containers']
    temp_dict={}
    for i,item in enumerate(row):
        temp_dict[temp_dict_list[i]]=item
        if i==len(row)-1:
            temp_dict[temp_dict_list[i]]=list(item.split(','))
    
    return temp_dict


 
@app.route("/item/<id>")
def get_item(id):
    if not id:
        resp=jsonify({"message":"enter and Id"})
        resp.status_code=404
        return resp
    begin='0000-00-00 00:00:00.000000'
    end=datetime.datetime.now() 
    if request.args.get('from'):
        begin=request.args.get('from')
    if request.args.get('to'):
        end=request.args.get('to')

    cur=mysql.connection.cursor()    
    results=cur.execute("SELECT id,truckTara FROM transactions WHERE truck LIKE %s AND datetime BETWEEN %s AND %s ORDER BY datetime DESC",(id,begin,end))
    if results>0:
        sessions=[]
        first_tara=0
        session_details=cur.fetchall()
        for row in session_details:
            sessions.append(row['id'])
            if first_tara==0:
                first_tara=row['truckTara']
        resp={"id":id,"tara":first_tara,"sessions":sessions}
        resp=jsonify(resp) 
        resp.status_code=200
        return resp
    resp=jsonify({"message":"session not found"})
    resp.status_code=404
    return resp


@app.route("/unknown")
def get_unknown():
    cur=mysql.connection.cursor()    
    results=cur.execute("SELECT container_id FROM containers_registered WHERE weight IS NULL")
    if results>0:
        containers=[]        
        session_details=cur.fetchall()
        for row in session_details:
            containers.append(row['container_id']) 
        resp={"containers":containers}
        resp=jsonify(resp) 
        resp.status_code=200
        return resp
    resp=jsonify({"message":"no such container"})
    resp.status_code=404
    return resp
 

@app.route("/weight-api/health", methods=["GET"])
def get_health():
    # cur = mysql.connection.cursor()
    # result = cur.execute("Select * from users")
    # if result > 0:
    #   return "OK", 200
    # else:
    #   return "Data not found", 404
    # services = []
    # # result = ""
    # for service in services:
    #   req = request.get(f"http://localhost:5000/{service}")
    #   status_code = req.status_code
    #   if status_code < 200 or status_code > 299:
    #       result += f"\n service {service} : ... failed - {status_code} \n"
    #   else:
    #       result += f"\n Service {service} : {status_code}... ok \n"
    # return jsonify({
    #     "message": "Weight server health check successful"
    # })
    cur=mysql.connection.cursor()    
    results=cur.execute("SELECT 1 FROM transactions")
    results2=cur.execute("SELECT 1 FROM containers_registered")
    if results and results2:    
        res=jsonify({"message": "Weight server health check successful"})
        res.status_code=200
        return res
    res=jsonify({"warning":"server down!!!"})
    res.status_code=404
    return res

if __name__=="__main__":
    app.run(host='0.0.0.0')