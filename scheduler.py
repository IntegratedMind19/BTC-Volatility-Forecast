from datetime import datetime, timezone
from llm.client import generate_report
from forecast_store import load_report, save_report, save_status

model_version = "1.0"

def generate_scheduled_report() -> None:
  previous_report = load_report()
  save_status(
    {
      "status": "updating",
      "started_at": datetime.now(timezone.utc).isoformat(),
      "model_version": model_version,
      "previous_report_available": previous_report is not None
    }
  )

  try:
    result = generate_report()
    if result.get("status") != "success":
      raise RuntimeError("Forecast generation failed.")
    result["model_version"] = model_version
    save_report(result)
    save_status(
      {
        "status": "ready",
        "model_version": model_version
      }
    )
  except Exception as exc:
    save_status(
      {
        "status": "error",
        "error": str(exc),
        "model_version": model_version,
        "previous_report_available": previous_report is not None
      }
    )
