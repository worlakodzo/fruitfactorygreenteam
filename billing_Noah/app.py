from flask import Flask, jsonify, request
from db import connection, mycursor


app = Flask(__name__)

#Endpoint for post truck    
@app.route("/Truck",methods=['POST'])
def Truck_Post():
        
    if request.method == 'POST':
        body = request.get_json()
        truck_id = body['id']
        provider_id = body['provider_id']
        if truck_id != '' and provider_id != '' :
            
            
             with connection.cursor() as mycursor:
                mycursor = connection.cursor(dictionary=True)
                stmt, val = "INSERT INTO Trucks (id, provider_id) VALUES (%s, (select id from Provider where id=%s))", (truck_id, provider_id)
               
               #trap Database Error
                try:            
                    mycursor.execute(stmt, val)
                    connection.commit()
                    return jsonify({"msg": "Truck saved successfully!"}), 201
                except:
                    return jsonify({"msg": "error posting "}), 204
                    
             

        else:
            return jsonify({"msg": "Enter Truck ID and Provider ID "}), 204
    else:
        with connection.cursor() as mycursor:
             mycursor = connection.cursor(dictionary=True)
            # stmt = "SELECT * FROM Truck"
            # mycursor.execute(stmt)
            # stmt_result = mycursor.fetchall()
            # return jsonify(stmt_result)


@app.route("/Truck/",methods=['PUT'])
def Truck_Put():
    
    if request.method == 'PUT':
        body = request.get_json()
        truck_id = body['id']
        provider_id = body['provider_id']

        
        if truck_id !='' and provider_id !='':    
            with connection.cursor() as mycursor:
                mycursor = connection.cursor(dictionary=True)
                stmt = "update Trucks set provider_id = %s where id=%s" 
                val=(provider_id, truck_id)
                mycursor.execute(stmt,val)
                connection.commit
                return jsonify ({"msg": "provider ID updated successfully! "}+truck_id), 201
    else:
            return jsonify({"msg": "Truck ID not found in the database "}), 204


    
    
    
    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    