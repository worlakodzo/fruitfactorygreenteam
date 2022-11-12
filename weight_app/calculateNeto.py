from flask_mysqldb import MySQL
import MySQLdb.cursors


def sum_container_weights(data):
    sum = 0
    try:
        for record in data:
            sum+=record['weight']
        return sum
    except Exception as e:
        return "na" 
    
