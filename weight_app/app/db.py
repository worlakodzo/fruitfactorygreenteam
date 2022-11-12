from flask_app import app
from flask_mysqldb import MySQL

mysql=MySQL()
#MySQL configurations
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='root'
app.config['MYSQL_DB']='weight'
app.config['MYSQL_HOST']='db'
app.config['MYSQL_CURSORCLASS']='DictCursor'
mysql.init_app(app)

