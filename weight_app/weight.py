from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route("/weight", methods=["POST", "GET"])
def get_weight():
    data = []
    if request.method=="POST":
        direction = request.form["direction"]
        truck = request.form["license"]
        containers = request.form.getlist("containers")
        unit = request.form["unit"]
        force = request.form["force"]
        produce=request.form["produce"]

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