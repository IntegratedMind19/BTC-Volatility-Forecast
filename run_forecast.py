from forecast_store import initialize_store
from scheduler import generate_scheduled_report

if __name__ == "__main__":
    initialize_store()
    generate_scheduled_report()
