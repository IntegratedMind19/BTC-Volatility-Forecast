from flask import Flask, jsonify, render_template
from llm.client import generate_report
from llm.analysis_module import get_analysis_data, get_latest_vol_and_price
from datetime import date, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import generate_scheduled_report
from forecast_store import load_report, load_status

scheduler = BackgroundScheduler(timezone = "UTC")
print("Hello")

scheduler.add_job(
  generate_scheduled_report,
  trigger = "cron",
  hour = "0,4,8,12,16,20",
  minute = 0,
  id = "forecast_generation",
  replace_existing = True
)

if load_report() is None:
  generate_scheduled_report()

app = Flask(__name__, template_folder = "template")

@app.route("/")
def index():
  return render_template("index.html")
'''
@app.get("/api/forecast")
def forecast():
  result = analysis
  if result.get("status") != "success":
    return jsonify(result), 500
  return jsonify(result), 200
'''

@app.get("/api/forecast/latest")
def get_latest_report():
  latest_report = load_report()
  if not latest_report or latest_report is None:
    return jsonify(
      {
        "status": "unavailable",
        "error": "No report available at the moment"
      }
    ), 400
  return jsonify(latest_report), 200

@app.get("/api/forecast/status")
def get_status():
  status = load_status()
  if not status or status is None:
    return jsonify({"information": "status is not available"}), 400
  return jsonify(status), 200

@app.get("/api/chart-data")
def get_chart_data():
  chart_data = get_latest_vol_and_price()
  chart_data["dates"] = [(date.today() - timedelta(days = t)).strftime("%d/%m/%Y") for t in range(29,-1,-1)]
  chart_data["tomorrow_date"] = (date.today() - timedelta(days = -1)).strftime("%d/%m/%Y")
  return jsonify(chart_data)

@app.route("/forecast")
def forecast_explanation():
  return render_template("forecast.html")

@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == "__main__":
  scheduler.start()
  app.run(debug = True, use_reloader = False)
