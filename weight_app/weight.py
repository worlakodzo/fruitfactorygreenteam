from flask import Flask,render_template,request
from flask_mysqldb import MySQL
import datetime
 
 
app=Flask(__name__)

with open('db.yaml','r') as file:
    db=yaml.safe_load(file)
 
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='passwd'
app.config['MYSQL_DB']='weight'

mysql=MySQL(app)

@app.route('/')
def home():
    return ("hello green weight")

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