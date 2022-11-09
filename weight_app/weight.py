from flask import Flask,request
from flask_mysqldb import MySQL
import datetime
 
 
app=Flask(__name__)

 
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='passwd'
app.config['MYSQL_DB']='weight'

mysql=MySQL(app)

@app.route('/')
def home():
    return ("hello green weight")

@app.route('/session/<id>')
def get_session(id):
    id=request.view_args['id']
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
    return [temp_dict]
        


@app.route('/weight')
def get_weight():
    cur=mysql.connection.cursor()
    if request.args.get('from'):
        begin=request.args.get('from')        
    else:
        begin='2022-11-08 00:00:00.000000' 
    if request.args.get('to'):
        end=request.args.get('to')
    else:
        end=datetime.datetime.now() 
    if request.args.get('filter'):
        fil=request.args.get('filter')
    else:
        fil='' 
    # if fil=='':    
    #     results=cur.execute("SELECT id,direction,bruto,neto,produce,containers FROM transactions ORDER BY direction WHERE datetime BETWEEN %s AND %s",(begin,end))
    # else:
    #     results=cur.execute("SELECT id,direction,bruto,neto,produce,containers FROM transactions ORDER BY direction WHERE direction=%s AND datetime BETWEEN DATE(%s) AND DATE(%s)",(begin,end,fil))
    results=cur.execute("SELECT id,direction,bruto,neto,produce,containers FROM transactions ORDER BY direction")
    if results>0:         
        transanction_Details=cur.fetchall()
        final_output=[]
        temp_dict={'id':'','direction':'','bruto':'','neto':'','produce':'','containers':[]}
        for row in transanction_Details:
            for i,item in enumerate(temp_dict):
                temp_dict[item]=row[i]
                if i==len(row)-1:
                    temp_dict[item]=list(row[i].split(','))
            final_output.append(temp_dict)
        return final_output
 
    return ("weight is empty")
  
if __name__=="__main__":
    app.run()