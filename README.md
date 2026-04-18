# 🖥️ Real-Time Server Monitoring Pipeline

A real-time data streaming pipeline that ingests server metrics, detects anomalies using machine learning, and displays a live updating dashboard.

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python threading** | Real-time data streaming |
| **Isolation Forest** | Unsupervised anomaly detection |
| **SQLite** | Lightweight data persistence |
| **Plotly Dash** | Live dashboard (updates every 2s) |

## ✨ Features

- 📡 Streams CPU, memory, and network metrics every second
- 🚨 Detects anomalies in real-time (5% contamination rate)
- 📊 Live dashboard with anomaly markers
- 💾 Persists all data to SQLite

## 🚀 Getting Started

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install pandas numpy scikit-learn plotly dash
python dashboard.py
```

Open http://localhost:8050

## 📊 Results

- Monitored 3 metrics: CPU usage, memory usage, network I/O
- Detected ~5% anomalies in real-time stream
- Dashboard refreshes every 2 seconds

## 👤 Author

Karthik Mudenahalli Ashoka  
MS Applied AI, Stevens Institute of Technology
