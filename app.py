from flask import Flask, jsonify, render_template
from llm.client import generate_report
from datetime import date, timedelta, timezone, datetime
from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import generate_scheduled_report
from forecast_store import load_report, load_status
import json
from pathlib import Path

ROOT_PATH = Path(__file__).resolve().parent
DEFINITIONS_PATH = Path(ROOT_PATH + "/config/definitions.json")

scheduler = BackgroundScheduler(timezone = "UTC")

scheduler.add_job(
  generate_scheduled_report,
  trigger = "cron",
  hour = "0,4,8,12,16,20",
  minute = 0,
  id = "forecast_generation",
  replace_existing = True,
  misfire_grace_time = 4 * 60 * 60,
  coalesce = True,
  max_instances = 1
)

if load_report() is None:
  generate_scheduled_report()

app = Flask(__name__, template_folder = "template")

@app.route("/")
def index():
  return render_template("index.html")

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
  report = load_report()
  chart_data = dict()
  chart_data["price"] = report["analysis"]["date_vol_and_price"]["price"]
  chart_data["vol"] = report["analysis"]["date_vol_and_price"]["vol"]
  chart_data["prediction"] = report["analysis"]["prediction"]["predicted_volatility"]
  chart_data["date_price"] = report["analysis"]["date_vol_and_price"]["date_price"]
  chart_data["date_vol"] = report["analysis"]["date_vol_and_price"]["date_vol"]
  chart_data["tomorrow_date"] = (datetime.now(timezone.utc).date() - timedelta(days = -1)).strftime("%d/%m/%Y")
  return jsonify(chart_data), 200

@app.route("/forecast")
def forecast_explanation():
  return render_template("forecast.html")

@app.route("/api/definitions")
def get_definitions():
  try:
    definitions = json.loads(DEFINITIONS_PATH.read_text(encoding="utf-8"))
    if not definitions or definitions is None:
      return jsonify({"information": "Unable to retrieve definitions"}), 400
    return jsonify(definitions), 200
  except Exception as exc:
    return jsonify({"error": exc}), 400

@app.route("/about")
def about():
  return render_template("about.html")

if __name__ == "__main__":
  scheduler.start()
  app.run(debug = True, use_reloader = False)
