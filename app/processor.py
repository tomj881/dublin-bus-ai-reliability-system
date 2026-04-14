from datetime import datetime
from .detection import detect_event
from .features import build_feature_vector
from .model import load_model, predict_probability, risk_band
from .control import recommended_action, hold_time_sec, priority_level
from .database import insert_event
from .gemini_explainer import explain

_model = None


def get_model():
    global _model
    if _model is None:
        _model = load_model()
    return _model


def process_event(record: dict) -> dict:
    model = get_model()

    # Step 1: detect service condition
    record = detect_event(record)

    # Step 2: predict bunching probability
    if record["status"] == "first_bus":
        prob = 0.0
    else:
        features = build_feature_vector(record)
        prob = predict_probability(model, features)

    # Step 3: assign control outputs
    record["bunching_probability"] = prob
    record["risk_band"] = risk_band(prob)
    record["recommended_action"] = recommended_action(prob)
    record["hold_time_sec"] = hold_time_sec(prob)
    record["priority_level"] = priority_level(prob)

    # Step 4: AI explanation
    record["ai_explanation"] = explain(record)

    # Step 5: processing timestamp
    record["processed_at"] = datetime.utcnow()

    # Step 6: save to database
    insert_event(record)

    return record