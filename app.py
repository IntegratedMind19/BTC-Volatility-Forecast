from flask import Flask, jsonify, render_template
from llm.client import generate_report
from llm.analysis_module import get_analysis_data, get_latest_vol_and_price
from datetime import date, timedelta

app = Flask(__name__, template_folder = "template")

@app.route("/")
def index():
  return render_template("index.html")

@app.get("/api/forecast")
def forecast():
  result = generate_report()
  if result.get("status") != "success":
    return jsonify(result), 500
  return jsonify(result), 200

@app.get("/api/chart-data")
def get_chart_data():
  chart_data = get_latest_vol_and_price()
  chart_data["dates"] = [date.today() - timedelta(days = t) for t in range(29,-1,-1)]
  return jsonify(chart_data)

@app.route("/forecast")
def forecast_explanation():
  return render_template("forecast.html")

@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == "__main__":
  app.run(debug = True)
