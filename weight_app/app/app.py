from flask import Flask,request,jsonify
from flask_app import app
from db import mysql 
import datetime
 

 
# app.config['MYSQL_HOST']='db'
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']='passwd'
# app.config['MYSQL_DB']='weight'
# app.config['MYSQL_CURSORCLASS']='DictCursor'


# mysql=MySQL(app)
# connection=mysql.connector.connect(user='root',password='root',host='db',port="3306",database='weight')
@app.route('/')
def home():   
    cur=mysql.connection.cursor()
    cur.execute("SELECT * FROM transactions")
    rows=cur.fetchall()
    resp=jsonify(rows)
    resp.status_code=200
    return resp

@app.route('/session/<id>')
def get_session(id):     
    id=int(id) 
    cur=mysql.connection.cursor()
    
    results=cur.execute("SELECT direction,id,truck,bruto,truckTara,neto FROM transactions WHERE id LIKE %s",(id,))
    if results>0:
        session_details=cur.fetchall() 
  
        resp=jsonify(session_details)
        resp.status_code=200
        return resp
    resp=jsonify({"message":"session not found"})
    resp.status_code=404
    return resp
        
@app.route('/weight')
def get_weight():
  
    cur=mysql.connection.cursor()
    
    begin='0000-00-00 00:00:00.000000'
    end=datetime.datetime.now() 
    fil=''
 
    if request.args.get('filter'):
        if request.args.get('from'):
            begin=request.args.get('from')
        if request.args.get('to'): 
            end=request.args.get('to') 
        fil=request.args.get('filter')             
        results=cur.execute("SELECT id,direction,bruto,neto,produce,containers FROM transactions WHERE direction LIKE %s AND datetime BETWEEN %s AND %s",(fil,begin,end))
        if results>0:         
            transanction_Details=cur.fetchall()               
            resp=jsonify(transanction_Details)
            resp.status_code=200
 
            return resp
    else:         
        results=cur.execute("SELECT id,direction,bruto,neto,produce,containers FROM transactions WHERE datetime BETWEEN %s AND %s  ORDER BY direction",(begin,end))    
        if results>0:                   
            transanction_Details=cur.fetchall() 
            resp=jsonify(transanction_Details)
            resp.status_code=200 
            return resp
 
    resp=jsonify({"message":"session not found"})
    resp.status_code=404
    return resp

def row_to_dict(row):
    temp_dict_list=['id','direction','bruto','neto','produce','containers']
    temp_dict={}
    for i,item in enumerate(row):
        temp_dict[temp_dict_list[i]]=item
        if i==len(row)-1:
            temp_dict[temp_dict_list[i]]=list(item.split(','))
    
    return temp_dict


@app.route("/weight-api/health", methods=["GET"])
def get_health():
    # cur = mysql.connection.cursor()
    # result = cur.execute("Select * from users")
    # if result > 0:
    #   return "OK", 200
    # else:
    #   return "Data not found", 404
    # services = []
    # # result = ""
    # for service in services:
    #   req = request.get(f"http://localhost:5000/{service}")
    #   status_code = req.status_code
    #   if status_code < 200 or status_code > 299:
    #       result += f"\n service {service} : ... failed - {status_code} \n"
    #   else:
    #       result += f"\n Service {service} : {status_code}... ok \n"
    return jsonify({
        "message": "Weight server health check successful"
    })
  
if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')