from flask_mysqldb import MySQL
import MySQLdb.cursors





def save_container_record(c_id, c_weight, c_unit):
    qry = ("INPUT INTO containers registered(container_id, weight, unit) values(%s, %s, %s,)", c_id, c_weight, c_unit)
    return qry



def read_file(a, ext):
    sum = 0
    unit = None
    
    #Reading csv
    if ext=="csv":
        # When unit is in kg
        try: 
            for i in a:
                save_container_record()
                sum+=int(i['kg'])
            unit = 'kg'
        # When unit is in lbs
        except:
            for i in a:
                sum+=int(i['lbs'])
            unit='lbs'
        return sum, unit
    # Reading json file    
    elif ext=="json":
        for i in a:
            sum+=int(i['weight'])
        unit = i['unit']
        return sum, unit

