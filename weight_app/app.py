from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
import datetime
 
 
app=Flask(__name__)

# mysql config needs to be deleted.. 
# app.config['MYSQL_HOST']='localhost'
# app.config['MYSQL_USER']='root'
# app.config['MYSQL_PASSWORD']='passwd'
# app.config['MYSQL_DB']='weight'

mysql=MySQL(app)
@app.route('/')
def home():
    return ("hello green weight")

@app.route('/session/<id>')
def get_session(id):     
    id=int(id)
    temp_dict={}     
    cur=mysql.connection.cursor()
    results=cur.execute("SELECT direction,id,truck,bruto,truckTara,neto FROM transactions WHERE id LIKE %s",(id,))
    if results>0:
        session_details=cur.fetchall()
        if session_details[0][0]=='in':
            temp_dict['id']=session_details[0][1]
            temp_dict['truck']=session_details[0][2]
            temp_dict['bruto']=session_details[0][3]
        if session_details[0][0]=='out':
            temp_dict['id']=session_details[0][1]
            temp_dict['truck']=session_details[0][2]
            temp_dict['bruto']=session_details[0][3]
            temp_dict['truckTara']=session_details[0][4]
            temp_dict['neto']=session_details[0][5]   
    # for item in results:
    #     temp_dict[item]
    resp=jsonify(temp_dict)
    resp.status_code(200)
    return resp
        
@app.route('/weight')
def get_weight():
    begin='0000-00-00 00:00:00.000000'
    end=datetime.datetime.now() 
    fil=''
    cur=mysql.connection.cursor()
   
    if request.args.get('filter'):
        if request.args.get('from'):
            begin=request.args.get('from')
        if request.args.get('to'): 
            end=request.args.get('to') 
        fil=request.args.get('filter')             
        results=cur.execute("SELECT id,direction,bruto,neto,produce,containers FROM transactions WHERE direction LIKE %s AND datetime BETWEEN %s AND %s",(fil,begin,end))
        if results>0:         
            transanction_Details=cur.fetchall()
            final_output=[]
            for row in transanction_Details:
                dict=row_to_dict(row)
                final_output.append(dict)              
            resp=jsonify(final_output)
            resp.status_code(200)
            return resp

    else:         
        results=cur.execute("SELECT id,direction,bruto,neto,produce,containers FROM transactions WHERE datetime BETWEEN %s AND %s  ORDER BY direction",(begin,end))    
        if results>0:                   
            transanction_Details=cur.fetchall()
            final_output=[]
            for row in transanction_Details:
                dict=row_to_dict(row)
                final_output.append(dict)
            resp=jsonify(final_output)
            resp.status_code(200)
            return resp

            
    return ("weight is empty")
def row_to_dict(row):
    temp_dict_list=['id','direction','bruto','neto','produce','containers']
    temp_dict={}
    for i,item in enumerate(row):
        temp_dict[temp_dict_list[i]]=item
        if i==len(row)-1:
            temp_dict[temp_dict_list[i]]=list(item.split(','))
    resp=jsonify(temp_dict)
    resp.status_code(200)
    return resp


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
    app.run()