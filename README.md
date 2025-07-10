# 🌐 Global Market Pulse — Crypto Metrics Dashboard

A full-stack crypto dashboard app that fetches real-time data from CoinGecko, stores it in a PostgreSQL database, computes metrics, and visualizes them using Dash.

---

## 🚀 Features

- ⏱ Scheduled ingestion every 10 minutes (via `schedular.py`)
- 📊 Real-time Dash dashboard UI
- 📥 Data from CoinGecko + ExchangeRate API
- 🧠 Computes volatility, CV, and other analytics
- 📧 Email alerts on failure (via Gmail SMTP)
- 🧪 Fully tested: unit, integration, and smoke tests

---

## 🧠 Why Separate Dashboard & Scheduler?

| Component     | Role                                 |
|---------------|--------------------------------------|
| `server.py`   | Runs the **Dash UI (Web Service)**   |
| `schedular.py`| Runs the **Background Scheduler**    |

We separate them because:
- They can scale or crash independently
- Avoids blocking the UI
- Render supports 2 clean services: Web & Worker
- Follows modern microservice best practices

---

## 🏗 Tech Stack

| Layer         | Tools Used                                    |
|---------------|-----------------------------------------------|
| UI            | Python Dash + Bootstrap (Cyborg Theme)        |
| Backend       | Python, SQLAlchemy, CoinGecko API             |
| Scheduler     | `schedule` library (every 10 mins)            |
| DB            | SQLite (local) / PostgreSQL (cloud via Render)|
| Email Alerts  | `smtplib` + Gmail                             |
| Testing       | `pytest` (unit, integration, e2e)             |
| Deployment    | Render (free tier)                            |
| CI/CD         | GitHub Actions                                |

---

## 📁 Project Structure
```
global_market_pulse/
│
├── server.py # Main Dash app (entry point)
├── ingestion/
│ └── schedular.py # Runs data fetch + metric computation
│ └── email_alerts.py # Sends email alerts
├── database/
│ └── db_engine.py # DB connection (via SQLAlchemy)
│ └── db_handler.py # Create tables, insert data
├── dashboard/
│ └── layout.py # Tabbed UI layout
│ └── callbacks/ # Dropdowns, graphs, interactivity
├── processing/
│ └── compute_metrics.py # Calculates volatility, CV, etc.
├── scripts/ # Backfill and fetch helpers
├── config/
│ └── .env.example # Example env vars (no secrets)
│ └── settings.py # Reads from OS or .env
├── tests/ # unit/, integration/, e2e/
└── requirements.txt
```

---

## 🧪 Run Locally

### 1. Clone the repo

```bash
git clone https://github.com/your-username/global_market_pulse.git
cd global_market_pulse
```

### 2. Set up environment variables
```bash
cp config/.env.example config/.env
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```


### 4. Run the dashboard (UI)
```bash
python server.py
```


### 5. Run the scheduler (optional for local dev)
```bash
python ingestion/schedular.py
```