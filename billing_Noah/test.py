from flask import Flask, request, jsonify, abort



app = Flask(__name__)



@app.route('/')
def index():
    return jsonify({
        "message": "welcome to billing app"
    })






if __name__ == "__main__":
    app.run(debug=True)