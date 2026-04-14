import pandas as pd
from .config import BUNCHING_THRESHOLD_MIN, GAP_THRESHOLD_MIN


def classify_status(headway):
    if pd.isna(headway):
        return "first_bus"
    if headway < BUNCHING_THRESHOLD_MIN:
        return "bunching"
    if headway > GAP_THRESHOLD_MIN:
        return "gap"
    return "normal"


def reliability_score(status: str) -> float:
    if status == "normal":
        return 100.0
    if status == "bunching":
        return 35.0
    if status == "gap":
        return 20.0
    return 80.0


def detect_event(record: dict) -> dict:
    h = record.get("headway_min")

    record["bunching_flag"] = int(pd.notna(h) and h < BUNCHING_THRESHOLD_MIN)
    record["gap_flag"] = int(pd.notna(h) and h > GAP_THRESHOLD_MIN)
    record["status"] = classify_status(h)
    record["reliability_score"] = reliability_score(record["status"])

    return record