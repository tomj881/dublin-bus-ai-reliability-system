from fastapi import FastAPI, Query
from .database import (
    create_db,
    fetch_latest,
    fetch_summary,
    fetch_routes,
    fetch_stops,
    fetch_risk_by_stop,
    fetch_action_counts,
)

app = FastAPI(title="Dublin Bus AI Reliability API")


@app.on_event("startup")
def startup():
    create_db()


@app.get("/")
def root():
    return {"message": "Dublin Bus AI Reliability API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/summary")
def summary():
    return fetch_summary()


@app.get("/events/latest")
def latest(limit: int = Query(default=50, ge=1, le=500)):
    return fetch_latest(limit=limit)


@app.get("/routes")
def routes():
    return fetch_routes()


@app.get("/stops")
def stops():
    return fetch_stops()


@app.get("/risk/by-stop")
def risk_by_stop():
    return fetch_risk_by_stop()


@app.get("/actions")
def actions():
    return fetch_action_counts()