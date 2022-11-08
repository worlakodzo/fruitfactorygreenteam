from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/weight", methods=["POST", "GET"])
def get_weight():
    data = []
    bruto = None
    neto = None
    if request.method=="POST":
        json_data = request.get_json()
        direction = json_data["direction"]
        truck = json_data["license"]
        containers = json_data["containers"]
        weight = json_data["weight"]
        unit = json_data["unit"]
        force = json_data["force"]
        produce=json_data["produce"]

        if direction == "IN":
            bruto = weight

        elif direction == "OUT":
            neto = weight


        data.extend((truck, direction, containers, unit, force, produce))
        
         # Data structure of JSON format
        _data = jsonify(data) # Converts your data strcuture into JSON format
        
       
        _data.status_code = 202 # Provides a response status code of 202 which is "Accepted" 

        return _data # Returns the HT

    elif request.method=="GET":
        return "<h1>weight<h1>"
    return 404
if __name__=="__main__":
    app.run()

  