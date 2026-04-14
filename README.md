# 🚍 AI-Driven Bus Reliability System (Dublin Bus)

## 📌 Overview
This project was developed as part of the **Dublin Bus Innovation Challenge**, under the **Data & Visualisation** pillar.

The goal is to transform raw operational data into **real-time, AI-powered decision support**, improving service reliability and passenger experience.

---

## ⚠️ Problem Statement
Urban bus networks face persistent challenges:

- Bus bunching (multiple buses arriving together)
- Service gaps (long passenger waiting times)
- Irregular headways across routes
- Lack of real-time operational decision support

These issues reduce efficiency, increase delays, and negatively impact passengers.

---

## 💡 Solution
This project builds a **real-time AI-assisted system** that:

- Monitors live bus conditions
- Detects instability (bunching / gaps)
- Predicts disruption risk using Machine Learning
- Recommends operational actions (HOLD BUS, MONITOR, NO ACTION)
- Generates AI explanations using **Gemini 2.5 Flash**
- Visualizes everything through an interactive dashboard

---

## 🧠 System Architecture

Data Ingestion → Processing → Detection → ML Prediction → Decision Engine → AI Insight → Dashboard

---

## ⚙️ Tech Stack

- Python
- Pandas & NumPy
- Scikit-learn (Logistic Regression)
- Plotly
- Gradio (Dashboard UI)
- FastAPI (Backend integration)
- Gemini 2.5 Flash (AI insights)

---

## 📊 Features

- Real-time data simulation
- ML-based bus bunching prediction
- Rule-based detection system
- Decision engine for operational control
- AI-generated insights and explanations
- Interactive dashboard visualization

---

## 🖥️ Dashboard Preview

![Dashboard](assets/dashboard.png)

---

Route: E1 | Stop: Northwood  
Headway: 1.00 min  
Probability: p = 1.00 (100%)  
Action: HOLD BUS (120 sec)

Insight:
Service compression detected. Immediate intervention required to restore spacing.