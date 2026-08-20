import json
import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def initialize_store():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS forecast_state (
                    id INTEGER PRIMARY KEY,
                    report JSONB,
                    status JSONB
                )
            """)

            cur.execute("""
                INSERT INTO forecast_state (id)
                VALUES (1)
                ON CONFLICT (id) DO NOTHING
            """)

        conn.commit()

def save_report(report):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE forecast_state
                SET report = %s
                WHERE id = 1
                """,
                (json.dumps(report),)
            )

        conn.commit()

def load_report():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT report FROM forecast_state WHERE id = 1"
            )

            row = cur.fetchone()
    if row is None or row[0] is None:
        return None

    return row[0]

def save_status(status):
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE forecast_state
                SET status = %s
                WHERE id = 1
                """,
                (json.dumps(status),)
            )

        conn.commit()

def load_status():
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT status FROM forecast_state WHERE id = 1"
            )

            row = cur.fetchone()

    if row is None or row[0] is None:
        return None
    return row[0]

'''
from __future__ import annotations
import json
import os
from dotenv import load_dotenv
from pathlib import Path
from threading import Lock
from typing import Any

load_dotenv()
DATA_DIR = Path(os.getenv("FORECAST_DATA_DIR"))
print(DATA_DIR)
DATA_DIR.mkdir(parents=True, exist_ok=True)
REPORT_FILE = DATA_DIR / "latest_report.json"
STATUS_FILE = DATA_DIR / "forecast_status.json"

_store_lock = Lock()

def _write_json_atomic(file_path: Path, payload: dict[str, Any]) -> None:
  DATA_DIR.mkdir(parents=True, exist_ok=True)
  temp_file = file_path.with_suffix(".tmp")
  temp_file.write_text(json.dumps(payload, indent = 2), encoding = "utf-8")
  temp_file.replace(file_path)

def save_report(report: dict[str, Any]) -> None:
  with _store_lock:
    _write_json_atomic(REPORT_FILE, report)

def load_report() -> dict[str, Any] | None:
  if not REPORT_FILE.is_file():
    print("REPORT FILE IS NOT AVAILABLE")
    return None
  print("REPORT FILE IS AVAILABLE")
  return json.loads(REPORT_FILE.read_text(encoding = "utf-8"))

def save_status(status: dict[str, Any]) -> None:
  with _store_lock:
    _write_json_atomic(STATUS_FILE, status)

def load_status() -> dict[str, Any] | None:
  if not STATUS_FILE.is_file():
    print("STATUS FILE IS NOT AVAILABLE")
    return None
  print("STATUS FILE IS AVAILABLE")
  return json.loads(STATUS_FILE.read_text(encoding = "utf-8"))
'''
