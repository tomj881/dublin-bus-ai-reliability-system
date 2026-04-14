import time
import pandas as pd
from .config import RAW_DATASET_PATH
from .database import create_db
from .processor import process_event

def stream_from_csv(delay_seconds: float = 0.5):
    df = pd.read_csv(RAW_DATASET_PATH)

    for col in ["scheduled_arrival", "actual_arrival", "actual_departure"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    create_db()
    print("Streaming events from CSV...")

    for _, row in df.iterrows():
        record = row.to_dict()

        for col in ["scheduled_arrival", "actual_arrival", "actual_departure"]:
            if col in record and pd.notna(record[col]):
                record[col] = pd.Timestamp(record[col]).to_pydatetime()
            else:
                record[col] = None

        processed = process_event(record)
        print(
            f"[{processed['route_id']}] {processed['stop_name']} | "
            f"status={processed['status']} | "
            f"prob={processed['bunching_probability']:.3f} | "
            f"action={processed['recommended_action']}"
        )
        time.sleep(delay_seconds)

if __name__ == "__main__":
    stream_from_csv()