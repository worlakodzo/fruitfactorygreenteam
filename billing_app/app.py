from flask import Flask, jsonify, request, abort
from db import connection, mycursor
import os.path
# import pandas as pd
# import xlrd
from openpyxl import Workbook, load_workbook
import datetime


app = Flask(__name__)
@app.route("/billing-api/health")
def index_test_bd():
    # with connection.cursor() as mycursor:
    #             mycursor = connection.cursor(dictionary=True)
    #             stmt = "select 1"
    #             mycursor.execute(stmt)
    #             connection.commit()
    return jsonify({"message":"billing server health check successful"}), 200





@app.route('/', methods = ["GET", "POST", "PUT"])
def billing_index():

    try:

        data = {
            "billing_index" "This is the home page"
        }


        return jsonify(data)

    except Exception as err:
        abort(500)

@app.route('/provider', methods=['GET', 'POST', 'PUT'])
def provider():
    if request.method == 'POST':
        body = request.get_json()
        id = body['id']
        name = body['name']
        if id != '' and name != '':
            with connection.cursor() as provider:
                provider = connection.cursor(dictionary=True)
                do = "INSERT INTO Provider (`name`) VALUES (%s)"
                provider.execute(do)
                connection.commit()
                return jsonify(id), 201
        else:
            return jsonify({"msg": " Unsuccessfull!!!"}), 204
            
    else:
        with connection.cursor() as provider:
            do = "SELECT * FROM Provider"
            provider.execute(do)
            result = provider.fetchall()
            return jsonify(result)



@app.route('/provider/<id>', methods=['GET', 'POST', 'PUT'])
def update_provider_name(id):
    if request.method == 'PUT':
        body = request.args.get()
        name = body['name']
        if name != '':
            with connection.cursor() as provider:
                provider = connection.cursor(dictionary=True)
                do = "INSERT INTO Provider (`name`) VALUES (%s)"
                provider.execute(do)
                connection.commit()
                return jsonify(name), 201
        else:
            return jsonify({"msg": " Unsuccessfull!!!"}), 204
            


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
        # receive post parameters
        body = request.get_json()
        # name = body['name']
        file = body['file']
        print(os.path.isfile(file))
        # check if file exist
        if os.path.isfile(file):
            # df = pd.read_excel(file)
            data = []
            df = load_workbook(file)
            sheet = df.active
            row_count = sheet.max_row
            for rows in sheet.iter_rows():
                row_cells = []
                for cell in rows:
                    row_cells.append(cell.value)
                data.append(tuple(row_cells))
                
            # establish db connection
            with connection.cursor() as mycursor:
                mycursor = connection.cursor(dictionary=True)
                stmt = "INSERT INTO Rates (`product_id`, `rate`, `scope`) VALUES (%s, %s, %s)"
                mycursor.executemany(stmt, data[1:])
                connection.commit()
                return jsonify({"msg": "Rates uploaded successfully!"}), 201
        else:
            return jsonify({"msg": "Unsupported file format!!!"}), 204
    else:
        with connection.cursor() as mycursor:
            # mycursor = connection.cursor(dictionary=True)
            stmt = "SELECT * FROM Rates"
            mycursor.execute(stmt)
            stmt_result = mycursor.fetchall()
            # export data to excel file
            wb = Workbook()
            ws = wb.active
            ws.title = "rates"

            ws.append(['Product', 'Rate', 'Scope'])

            for row in stmt_result:
                ws.append(list(row))
            wb.save(f"in/rates-{datetime.datetime.now().strftime('%Y%m%d')}.xlsx")
            
            return jsonify({"msg": "Rates downloaded successfully!"})


@app.route('/bill/<id>')
def getbill(id):
    t1 = request.args.get('t1')
    t2 = request.args.get('t2')

    # expected return
    return jsonify({"id": 12,"name": "<str>","from": "<str>","to": "<str>","truckCount": "<int>","sessionCount": "<int>","products": [{ "product":"<str>","count": "<str>", "amount": "<int>", "rate": "<int>", "pay": "<int>"}],"total": "<int>" })



@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    })


    

if __name__ == '__main__':
    app.run(debug=True, port=5000)