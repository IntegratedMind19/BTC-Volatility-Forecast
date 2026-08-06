from apscheduler.schedulers.background import BackgroundScheduler
from scheduler import generated_scheduled_report

scheduler = BackgroundScheduler(timezone = "UTC")

scheduler.add_job(
  generate_scheduled_report,
  trigger = "cron",
  hour = "0,4,8,12,16,20",
  minute = 0,
  id = "forecast_generation",
  replace_existing = True
)
