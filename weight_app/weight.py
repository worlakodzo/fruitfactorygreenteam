from flask import Flask, request, jsonify
 
app=Flask(__name__)

@app.route('/')
def home():
    return ("hello green weight")

@app.route('/weight')
def get_weight():
    return ("weight is green")


@app.route("/health", methods=["GET"])
def get_health():
	
	# cur = mysql.connection.cursor()
	# result = cur.execute("Select * from users")
	# if result > 0:
	# 	return "OK", 200
	# else:
	# 	return "Data not found", 404

	# services = []
	# # result = ""
	# for service in services:
	# 	req = request.get(f"http://localhost:5000/{service}")
	# 	status_code = req.status_code
	# 	if status_code < 200 or status_code > 299:
	# 		result += f"\n service {service} : ... failed - {status_code} \n"
	# 	else:
	# 		result += f"\n Service {service} : {status_code}... ok \n"
	return jsonify({
        "message": "Health check successful"
    })

  
if __name__=="__main__":
    app.run()