from __future__ import annotations
import json
import os
from pathlib import Path
from threading import Lock
from typing import Any
from sqlalchemy import (Column, DateTime, Integer, Text, create_engine)
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
  raise RuntimeError("DATABASE_URL is not defined")

engine = create_engine(DATABASE_URL, pool_pre_ping = True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class ForecastState(Base):
    __tablename__ = "forecast_state"
    id = Column(Integer, primary_key=True)
    latest_report = Column(
        Text,
        nullable=True
    )
    current_status = Column(
        Text,
        nullable=True
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

Base.metadata.create_all(engine)

def _get_state(session):
    state = session.get(ForecastState, 1)
    if state is None:
        state = ForecastState(id=1)
        session.add(state)
        session.commit()
        session.refresh(state)
    return state

def save_report(report):
    with SessionLocal() as session:
        state = _get_state(session)
        state.latest_report = json.dumps(report)
        session.commit()

def load_report():
    with SessionLocal() as session:
        state = session.get(ForecastState, 1)
        if (
            state is None
            or state.latest_report is None
        ):
            return None
        return json.loads(
            state.latest_report
        )

def save_status(status):
    with SessionLocal() as session:
        state = _get_state(session)
        state.current_status = json.dumps(status)
        session.commit()
      
def load_status():
    with SessionLocal() as session:
        state = session.get(ForecastState, 1)

        if (
            state is None
            or state.current_status is None
        ):
            return None

        return json.loads(
            state.current_status
        )
      
'''
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
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
    return None
  return json.loads(REPORT_FILE.read_text(encoding = "utf-8"))

def save_status(status: dict[str, Any]) -> None:
  with _store_lock:
    _write_json_atomic(STATUS_FILE, status)

def load_status() -> dict[str, Any] | None:
  if not STATUS_FILE.is_file():
    return None
  return json.loads(STATUS_FILE.read_text(encoding = "utf-8"))
