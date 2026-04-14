def recommended_action(prob: float) -> str:
    if prob >= 0.70:
        return "HOLD_BUS"
    if prob >= 0.40:
        return "MONITOR"
    return "NO_ACTION"

def hold_time_sec(prob: float) -> int:
    if prob >= 0.85:
        return 120
    if prob >= 0.70:
        return 60
    return 0

def priority_level(prob: float) -> str:
    if prob >= 0.85:
        return "CRITICAL"
    if prob >= 0.70:
        return "HIGH"
    if prob >= 0.40:
        return "MEDIUM"
    return "LOW"