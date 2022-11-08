from flask import Flask, jsonify, request, abort


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





@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    })



if __name__ == "__main__":
    app.run(debug=True)

