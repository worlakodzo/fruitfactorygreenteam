from flask import Flask, jsonify, request
from db import connection, mycursor
from controllers.rates import rates

app = Flask(__name__)

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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    