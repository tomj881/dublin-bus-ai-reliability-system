# dublin-bus-ai-reliability-system
Real-time AI system for detecting bus bunching, predicting service disruptions, and generating operational decisions using ML and Gemini 2.5 Flash.

# 🚍 AI-Driven Bus Reliability System (Dublin Bus)

## 📌 Overview
This project was developed as part of the **Dublin Bus Innovation Challenge**, focusing on the **Data & Visualisation** pillar.

The goal is to transform raw operational data into **real-time AI-powered decision support**, improving service reliability and passenger experience.

---

## ⚠️ Problem Statement
Urban bus systems face several critical challenges:

- Bus bunching (multiple buses arriving together)
- Service gaps (long waiting times)
- Irregular headways
- Lack of real-time decision support

---

## 💡 Solution
This project builds a **real-time AI-assisted system** that:

- Detects service conditions (normal, bunching, gap)
- Predicts disruption risk using Machine Learning
- Recommends operational actions (HOLD BUS, MONITOR, NO ACTION)
- Generates AI explanations using **Gemini 2.5 Flash**
- Visualizes everything in a **Gradio dashboard**

---

## 🧠 System Architecture

Data → Processing → Detection → Prediction → Decision → AI Insight → Dashboard

---

## ⚙️ Tech Stack

- Python
- Pandas
- Scikit-learn (Logistic Regression)
- Plotly
- Gradio
- FastAPI
- Gemini 2.5 Flash

---

## 📊 Features

- Real-time data simulation
- ML-based bunching prediction
- Decision engine for operations
- AI-generated insights
- Interactive dashboard

---

## 📸 Dashboard Preview

![Dashboard](assets/dashboard.png)

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/yourusername/dublin-bus-ai-reliability-system.git

# Navigate into project
cd dublin-bus-ai-reliability-system

# Install dependencies
pip install -r requirements.txt

# Run system
python -m app.synthetic_generator

#Run dashboard
python -m app.dashboard
