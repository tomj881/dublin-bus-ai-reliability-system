from datetime import datetime
from sqlalchemy import (
    create_engine,
    MetaData,
    Table,
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    select,
    func,
)
from .config import DB_PATH

engine = create_engine(f"sqlite:///{DB_PATH}", future=True)
metadata = MetaData()

events = Table(
    "events",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("route_id", String),
    Column("bus_id", String),
    Column("bus_name", String),
    Column("stop_sequence", Integer),
    Column("stop_name", String),
    Column("scheduled_arrival", DateTime),
    Column("actual_arrival", DateTime),
    Column("delay_sec", Float),
    Column("waiting_passengers", Float),
    Column("dwell_time_sec", Float),
    Column("actual_departure", DateTime),
    Column("hour", Integer),
    Column("headway_min", Float),
    Column("status", String),
    Column("bunching_flag", Integer),
    Column("gap_flag", Integer),
    Column("reliability_score", Float),
    Column("bunching_probability", Float),
    Column("risk_band", String),
    Column("recommended_action", String),
    Column("hold_time_sec", Integer),
    Column("priority_level", String),
    Column("ai_explanation", Text),
    Column("processed_at", DateTime, default=datetime.utcnow),
)

def create_db():
    metadata.create_all(engine)

def insert_event(record: dict):
    with engine.begin() as conn:
        conn.execute(events.insert().values(**record))

def fetch_latest(limit: int = 50):
    with engine.connect() as conn:
        rows = conn.execute(
            select(events).order_by(events.c.id.desc()).limit(limit)
        ).mappings().all()
    return [dict(r) for r in rows]

def fetch_summary():
    with engine.connect() as conn:
        total = conn.execute(select(func.count()).select_from(events)).scalar_one()
        bunching = conn.execute(
            select(func.count()).select_from(events).where(events.c.status == "bunching")
        ).scalar_one()
        gaps = conn.execute(
            select(func.count()).select_from(events).where(events.c.status == "gap")
        ).scalar_one()
        avg_delay = conn.execute(select(func.avg(events.c.delay_sec))).scalar()
        avg_prob = conn.execute(select(func.avg(events.c.bunching_probability))).scalar()

    return {
        "total_events": int(total or 0),
        "bunching_events": int(bunching or 0),
        "gap_events": int(gaps or 0),
        "avg_delay_sec": round(float(avg_delay or 0), 2),
        "avg_bunching_probability": round(float(avg_prob or 0), 4),
    }

def fetch_routes():
    with engine.connect() as conn:
        rows = conn.execute(
            select(events.c.route_id).distinct().order_by(events.c.route_id)
        ).all()
    return [r[0] for r in rows]

def fetch_stops():
    with engine.connect() as conn:
        rows = conn.execute(
            select(events.c.stop_name).distinct().order_by(events.c.stop_name)
        ).all()
    return [r[0] for r in rows]

def fetch_risk_by_stop():
    with engine.connect() as conn:
        rows = conn.execute(
            select(
                events.c.stop_name,
                func.avg(events.c.bunching_probability),
                func.count()
            )
            .group_by(events.c.stop_name)
            .order_by(func.avg(events.c.bunching_probability).desc())
        ).all()

    return [
        {"stop_name": r[0], "avg_prob": float(r[1] or 0), "count": int(r[2] or 0)}
        for r in rows
    ]

def fetch_action_counts():
    with engine.connect() as conn:
        rows = conn.execute(
            select(
                events.c.recommended_action,
                func.count()
            )
            .group_by(events.c.recommended_action)
            .order_by(func.count().desc())
        ).all()

    return [{"recommended_action": r[0], "count": int(r[1])} for r in rows]