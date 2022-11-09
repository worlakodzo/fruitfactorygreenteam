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
            return final_output

    else:         
        results=cur.execute("SELECT id,direction,bruto,neto,produce,containers FROM transactions WHERE datetime BETWEEN %s AND %s  ORDER BY direction",(begin,end))    
        if results>0:                   
            transanction_Details=cur.fetchall()
            final_output=[]
            for row in transanction_Details:
                dict=row_to_dict(row)
                final_output.append(dict)
            return final_output

            
    return ("weight is empty")
def row_to_dict(row):
    temp_dict_list=['id','direction','bruto','neto','produce','containers']
    temp_dict={}
    for i,item in enumerate(row):
        temp_dict[temp_dict_list[i]]=item
        if i==len(row)-1:
            temp_dict[temp_dict_list[i]]=list(item.split(','))
    return temp_dict
  
if __name__=="__main__":
    app.run()