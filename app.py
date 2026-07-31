from flask import Flask, jsonify, render_template
from llm.client import generate_report

app = Flask(__name__)

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/api/forecast", methods = ["GET"])
def forecast():
  result = generate_report()
  if result.get("status") != "success":
    return jsonify(result), 500
  return jsonify(result), 200

if __name__ = "__main__":
  app.run(debug = True)
