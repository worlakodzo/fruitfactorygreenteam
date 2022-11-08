from flask import Flask 
 
app=Flask(__name__)

@app.route('/')
def home():
    return ("hello green weight")

@app.route('/weight')
def get_weight():
    return ("weight is green")
  
if __name__=="__main__":
    app.run()