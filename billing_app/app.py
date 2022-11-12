from flask import Flask, jsonify, request, abort
import os.path
from openpyxl import Workbook, load_workbook
import datetime
import requests
from db import connection
import json


app = Flask(__name__)

 
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
    

@app.route('/', methods = ["GET", "POST", "PUT"])
def billing_index():

    try:

        data = {
            "billing_index" "This is the home page"
        }


        return jsonify(data)

    except Exception as err:
        abort(500)


@app.route('/provider', methods=['POST'])
def provider():
    if request.method == 'POST':
        body = request.get_json()
        name1 = body['name']
        if name1 != None:
            with connection.cursor() as mycursor:
                mycursor = connection.cursor(dictionary=True)
                stmt,val = "INSERT INTO Provider (name) VALUES (%s)",[(name1)]
                print (name1)
                print(stmt)
                mycursor.execute(stmt, val)
                connection.commit()
                return jsonify({"record saves provider id: ": mycursor.lastrowid}), 201
        else:
            return jsonify({"msg": " Unsuccessfull!!!"}), 204
            
    else:
        with connection.cursor() as provider:
            do = "SELECT * FROM Provider"
            provider.execute(do)
            result = provider.fetchall()
            return jsonify(result)



@app.route('/provider/<id>', methods=['PUT'])
def update_provider_name(id):
    if request.method == 'PUT':
        id=request.args.get('id')
        body = request.get_json()
        name = body['name']
        if name != '':
            with connection.cursor() as provider:
                provider = connection.cursor(dictionary=True)
                do,val = "UPDATE Provider SET name =%s where id=%s",(name,id)
                provider.execute(do,val)
                connection.commit()
                return jsonify({"message":"update succes:  "}), 201
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


#Endpoint for post truck    
@app.route('/truck', methods=['POST'])
def Truck_Post():
    if request.method == 'POST':
        body = request.get_json()
        truck_id = body['id']
        provider_id = body['provider_id']
        if truck_id != '' and provider_id != None :
                try: 
                    with connection.cursor() as mycursor:
                        mycursor = connection.cursor(dictionary=True)
                        stmt, val = "INSERT INTO Trucks (id, provider_id) VALUES (%s, (select id from Provider where id=%s))", (truck_id, provider_id)
                        mycursor.execute(stmt, val)
                        connection.commit()
                        return jsonify({"message": "data saved successfully!"}), 201
                except Exception as e:
                    return jsonify({"message": "failure posting "}), 400
        else:
            return jsonify({"message": "provide Truck ID and Provider ID "}), 400
    else:
        return jsonify({"message": "method not allowed"}), 405


@app.route('/truck/<id>', methods=['PUT'])
def Truck_Put(id):
    
    if request.method == 'PUT':
        body = request.get_json()
        truck_id = request.args.get('id')
        provider_id = body['provider_id']

        if truck_id !='' and provider_id != None:    
            with connection.cursor() as mycursor:
                mycursor = connection.cursor(dictionary=True)
                stmt = "update Trucks set provider_id = %s where id=%s" 
                val=(provider_id, truck_id)
                mycursor.execute(stmt,val)
                connection.commit
                return jsonify ({"message": "provider ID updated successfully! "}), 201
    else:
            return jsonify({"msg": "Truck ID not found in the database "}), 204

@app.route('/truck',methods=['GET'])
def truck_Get():
    if request.method == 'GET':
        reqResp=requests.get('http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8081')
        assert reqResp.status_code == 200
        data=json.loads(reqResp.content)
        print(data)
        return jsonify(data), 200
        
            # t1 = request.args.get('t1')
            # t2 = request.args.get('t2')
            # param={'id':id,"from":t1,"to":t2}
            # reqResp=requests.get('http://ec2-18-192-110-37.eu-central-1.compute.amazonaws.com:8081/')
            # assert reqResp.status_code == 200
           
           
        # except Exception as e:
        #     #data={ "id": "144-12-510", "tara": "120","sessions": ["sid112220","sid22233","sid10002"]}

        #     return "error inside expection",400
    else:
        return jsonify("message:error"),204

   


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": "Internal Server Error"
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)