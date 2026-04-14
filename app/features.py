def build_feature_vector(record: dict) -> dict:
    return {
        "delay_sec": float(record.get("delay_sec", 0) or 0),
        "waiting_passengers": float(record.get("waiting_passengers", 0) or 0),
        "dwell_time_sec": float(record.get("dwell_time_sec", 0) or 0),
        "headway_min": float(record.get("headway_min", 0) or 0),
        "stop_sequence": int(record.get("stop_sequence", 0) or 0),
        "hour": int(record.get("hour", 0) or 0),
    }