# app.py
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/greet', methods=['GET'])
def greet():
    value = request.get_json()
    print(value)
    return True,200

if __name__ == '__main__':
    app.run(debug=True)
