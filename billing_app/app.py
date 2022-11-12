from flask import Flask, jsonify, request, abort, render_template, redirect, url_for
#from db import connection
import os.path
from openpyxl import Workbook, load_workbook
import datetime
# import requests


app = Flask(__name__)

# Remove this dummy data
provider_list = [
    {
        "id": 1,
        "name": "worlako",

    },            {
        "id": 2,
        "name": "Seth",

    },            {
        "id": 3,
        "name": "Kofi",

    },            {
        "id": 4,
        "name": "Makafua",

    },
]



 
@app.route('/billing-api/health')
def health_db_status():
    
    try:
        
        with connection.cursor() as mycursor:
            mycursor = connection.cursor(dictionary=True)
            stmt = "select 1"
            mycursor.execute(stmt)
            stmt_result = mycursor.fetchone()
            return jsonify({"status": "OK"}), 200

    except Exception as e:
        
        return jsonify({"status":"failure"}), 500
    

@app.route('/', methods = ["GET"])
def billing_index():
    try:
        provider_count = 0
        truck_count = 0
        rate_count = 0

        return render_template(
            'index.html',
            provider_count  = provider_count,
            truck_count  = truck_count,
            rate_count  = rate_count
            )
    except Exception as err:
        abort(500)



@app.route('/provider', methods=['GET', 'POST'])
def provider():
    if request.method == 'POST':
        body = request.get_json()
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


@app.route('/provider/<id>', methods=['GET', 'PUT'])
def update_provider_name(id):
    if request.method == 'PUT':
        body = request.get_json()
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


    if request.method == 'GET':

        # retrieve specific provider here 
        pass



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
        filepath = f'./in/{file}'
        print(os.path.isfile(f'./in/{file}'))
        # check if file exist
        if os.path.isfile(f'./in/{file}'):
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
    return jsonify({
        "id": 12,
        "name": "<str>",
        "from": "<str>",
        "to": "<str>",
        "truckCount": "<int>",
        "sessionCount": "<int>",
        "products": [{ "product":"<str>","count": "<str>", "amount": "<int>", "rate": "<int>", "pay": "<int>"}],
        "total": "<int>" 
    })


#Endpoint for post truck    
@app.route("/truck",methods=['POST'])
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
                    return jsonify({"message": "Truck data saved successfully!"}), 201
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


@app.route("/truck/",methods=['PUT'])
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

@app.route('/truck/<id>')
def get_truckid(id):
    t1 = request.args.get('t1')
    t2 = request.args.get('t2')
    param={'id':id,"from":t1,"to":t2}
    reqResp=requests.get("url://weight_server:8081/item/<id>?from=t1&to=t2",params=param)
    assert reqResp.status_code == 200
    data=reqResp.json
    return data





@app.route('/provider-list', methods = ["GET"])
def get_provider_list():
    try:

        return render_template('provider-list.html', providers = provider_list)
    except Exception as err:
        abort(500)


@app.route('/truck-list', methods = ["GET"])
def get_truck_list():
    try:

        
        return render_template('index.html')
    except Exception as err:
        abort(500)


@app.route('/rate-list', methods = ["GET"])
def get_rate_list():
    try:

        
        return render_template('index.html')
    except Exception as err:
        abort(500)





@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    })




if __name__ == '__main__':
    app.run(debug=True, port=5000)