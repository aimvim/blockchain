from flask import Flask, jsonify

app =Flask(__name__)

@app.route("/")
def i():
    x={"a":"z"}
    return jsonify({"a":1},x)

app.run()