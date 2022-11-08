from flask import Flask, jsonify, request, abort
from db import connection, mycursor
from controllers.rates import rates


app = Flask(__name__)




@app.route('/', methods = ["GET", "POST", "PUT"])
def billing_index():

    try:

        data = {
            "billing_index" "This is the home page"
        }


        return jsonify(data)

    except Exception as err:
        abort(500)


@app.route('/weight', methods = ["POST"])
def add_weight():



    body = request.get_json()

    data = {
        "container": body['container'],
        "weight": body['weight'],
        "truck_id": body['truck_id'],
        "unit": body['unit'],
        "force": body['force']
    }


    return jsonify(data), 201


@app.route('/rates', methods=['GET', 'POST'])
def rates():
    if request.method == 'POST':
        body = request.get_json()
        name = body['name']
        address = body['address']
        if name != '' and address != '':
            with connection.cursor() as mycursor:
                # mycursor = connection.cursor(dictionary=True)
                # stmt, val = "INSERT INTO customers(name, address) VALUES (%s, %s)", (name, address)
                # mycursor.execute(stmt, val)
                # connection.commit()
                return jsonify({"msg": "Customer saved successfully!"}), 201
        else:
            return jsonify({"msg": "Name and Address are required fields!!!"}), 204
    else:
        with connection.cursor() as mycursor:
            mycursor = connection.cursor(dictionary=True)
            stmt = "SELECT * FROM Rates"
            mycursor.execute(stmt)
            stmt_result = mycursor.fetchall()
            return jsonify(stmt_result)




@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    })


    

if __name__ == '__main__':
    app.run(debug=True, port=5000)