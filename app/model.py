import os
import joblib
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from .config import (
    RAW_DATASET_PATH,
    MODEL_PATH,
    BUNCHING_THRESHOLD_MIN,
    GAP_THRESHOLD_MIN,
    SEED,
)

FEATURES = [
    "delay_sec",
    "waiting_passengers",
    "dwell_time_sec",
    "headway_min",
    "stop_sequence",
]

TARGET = "bunching_flag"


def ensure_detection_columns(df: pd.DataFrame) -> pd.DataFrame:
    df["bunching_flag"] = df["headway_min"].apply(
        lambda x: 1 if pd.notna(x) and x < BUNCHING_THRESHOLD_MIN else 0
    )

    df["gap_flag"] = df["headway_min"].apply(
        lambda x: 1 if pd.notna(x) and x > GAP_THRESHOLD_MIN else 0
    )

    return df


def train_and_save_model():
    print("Loading dataset...")

    if not RAW_DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {RAW_DATASET_PATH}")

    df = pd.read_csv(RAW_DATASET_PATH)
    print(f"Dataset shape: {df.shape}")

    required_columns = FEATURES + ["status"]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Dataset is missing required columns: {missing_columns}")

    df = ensure_detection_columns(df)

    # Remove first_bus rows because headway is missing / not meaningful there
    df = df[df["status"] != "first_bus"].copy()

    data = df[FEATURES + [TARGET]].dropna()
    print(f"Usable rows after filtering: {data.shape[0]}")

    if data.empty:
        raise ValueError("No usable rows found after filtering and dropping missing values.")

    X = data[FEATURES]
    y = data[TARGET]

    print("Target distribution:")
    print(y.value_counts())

    if y.nunique() < 2:
        raise ValueError(
            "Target has only one class. The model cannot train unless both 0 and 1 exist in bunching_flag."
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=SEED,
        stratify=y,
    )

    print("Training Logistic Regression model...")
    model = LogisticRegression(max_iter=1000, random_state=SEED)
    model.fit(X_train, y_train)

    print("Evaluating model...")
    y_pred = model.predict(X_test)

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "confusion_matrix": confusion_matrix(y_test, y_pred).tolist(),
        "classification_report": classification_report(y_test, y_pred, zero_division=0),
    }

    os.makedirs(MODEL_PATH.parent, exist_ok=True)
    joblib.dump(model, MODEL_PATH)

    print(f"Model saved to: {MODEL_PATH}")
    return model, metrics


def load_model():
    if not MODEL_PATH.exists():
        model, _ = train_and_save_model()
        return model
    return joblib.load(MODEL_PATH)


def predict_probability(model, feature_vector: dict) -> float:
    X = pd.DataFrame([feature_vector], columns=FEATURES)
    return float(model.predict_proba(X)[:, 1][0])


def risk_band(prob: float) -> str:
    if prob >= 0.70:
        return "High"
    if prob >= 0.40:
        return "Medium"
    return "Low"