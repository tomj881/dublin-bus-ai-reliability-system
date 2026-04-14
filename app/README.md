# Dublin Bus AI-Assisted Reliability System

This is a VS Code–friendly real-time prototype for bus reliability monitoring.

## What it does
- loads historical synthetic bus data for model training
- detects bunching and service gaps
- predicts bunching risk with a simple ML model
- recommends control actions
- optionally uses Gemini for explanations
- exposes a FastAPI backend
- shows a Gradio dashboard
- supports a synthetic live event generator

## Setup

1. Create and activate a virtual environment
2. Install requirements:
   pip install -r requirements.txt

3. Put your training dataset here:
   data/synthetic_dublin_bus_mixed_routes.csv

4. Train the model:
   python -m app.train_model

5. Start the API:
   uvicorn app.api:app --reload --host 127.0.0.1 --port 8000

6. Start one event source:
   python -m app.producer
   OR
   python -m app.synthetic_generator

7. Start dashboard:
   python -m app.dashboard

## Optional Gemini
Set environment variable:

Windows CMD:
set GEMINI_API_KEY=key_here

PowerShell:
$env:GEMINI_API_KEY="key_here"

Mac/Linux:
export GEMINI_API_KEY=key_here