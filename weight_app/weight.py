from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
import MySQLdb.cursors
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
    if request.method=="POST":
        json_data = request.get_json()
        direction = json_data["direction"]
        license = json_data["license"]
        containers = json_data["containers"]
        weight = json_data["weight"]
        unit = json_data["unit"]
        force = json_data["force"]
        if force == "true":
            force='TRUE'
        elif force=="false":
            force='FALSE'
        produce=json_data["produce"]

        if direction == "IN":
            bruto = weight

        elif direction == "OUT":
            neto = weight

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO tbl_weight  (direction, license, containers, weight, unit, produce) VALUES(%s, %s, %s, %s, %s, %s)', (direction, license, containers, weight, unit, produce))        
        mysql.connection.commit()

        data.extend((license, direction, containers, unit, force, produce))
        
         # Data structure of JSON format
        _data = jsonify(data) # Converts your data strcuture into JSON format
        
       
        _data.status_code = 202 # Provides a response status code of 202 which is "Accepted" 

        return _data # Returns the HT

    elif request.method=="GET":
        return "<h1>weight<h1>"
    return 404
if __name__=="__main__":
    app.run()

  