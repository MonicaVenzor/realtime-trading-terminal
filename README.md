# 📈 Real-Time Trading Terminal — Dash & Yahoo Finance

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)]()
[![Plotly](https://img.shields.io/badge/Plotly-Dash-00cc96?logo=plotly&logoColor=white)]()
[![pandas](https://img.shields.io/badge/pandas-Data_Cleaning-150458?logo=pandas)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A modern, Yahoo Finance–styled real-time trading terminal built with Dash, Plotly, and pandas.
Includes dynamic KPIs, sparklines, volatility metrics, and interactive visual analytics.

## 🎬 Live Demo (Preview)

<p align="center"> <img src="assets/demo_dashboard.gif" width="90%" alt="Real-Time Trading Terminal demo"> </p>

## 📖 Project Overview

This project demonstrates a full interactive analytics workflow:

Data Fetch (yfinance) → Transform (pandas) → Visualize (Dash + Plotly)

The app connects directly to Yahoo Finance APIs to retrieve live OHLCV market data and compute rolling KPIs such as cumulative returns and volatility.

## 📂 Project Structure

realtime-trading-terminal/
├─ app/
│  ├─ __init__.py           # Dash app factory
│  ├─ layout.py             # UI layout, components, navbar
│  └─ callbacks.py          # Callbacks & reactive logic
│
├─ src/
│  ├─ __init__.py           # Public API for transforms
│  ├─ fetch.py              # Data download (yfinance)
│  ├─ transform.py          # Returns & volatility calculations
│  ├─ forecast.py           # Simple linear forecast (demo)
│  └─ metrics.py            # Extra Plotly chart builders
│
├─ assets/
│  ├─ styles.css            # Custom theme & branding
│  └─ logo.png              # Yahoo-style logo
│
├─ notebooks/               # Exploratory notebooks
│
├─ run.py                   # App entry point
├─ requirements.txt
├─ .gitignore
├─ LICENSE
└─ README.md

## ⚙️ Core Features

### 🧩 Key Modules

| Module         | Description                                              |
| -------------- | -------------------------------------------------------- |
| `fetch.py`     | Fetches OHLCV data for multiple tickers via yfinance     |
| `transform.py` | Computes returns, cumulative performance, and volatility |
| `callbacks.py` | Defines all Dash callbacks and interactivity             |
| `layout.py`    | Builds responsive UI with Bootstrap components           |
| `metrics.py`   | Optional reusable Plotly chart generators                |

### 📊 Dashboard Components

| Section               | Description                                        |
| --------------------- | -------------------------------------------------- |
| 💹 **Main Chart**     | Price, Cumulative Return, or Candlestick (per tab) |
| ⚙️ **Controls**       | Ticker selector, date range, and time interval     |
| 📈 **KPI Cards**      | Last Close, Cumulative Return, and 20D Volatility  |
| 🔍 **Mini Analytics** | Daily returns bar chart and correlation heatmap    |
| 🌗 **Theme Toggle**   | Seamless switch between light and dark mode        |

### 🧮 Calculations

Returns & Volatility

daily_return = close.pct_change()
cum_return = (1 + daily_return).cumprod() - 1
vol_20d_ann = daily_return.rolling(20).std() * (252 ** 0.5)

Forecast (optional)

from sklearn.linear_model import LinearRegression
model = LinearRegression().fit(X_time, close_prices)
preds = model.predict(future_time_index)

### 🧠 Tech Stack

| Area          | Tools Used                                          |
| ------------- | --------------------------------------------------- |
| Frontend      | Dash, Plotly, Bootstrap (dash-bootstrap-components) |
| Data          | pandas, numpy, yfinance                             |
| Forecasting   | scikit-learn (LinearRegression)                     |
| Visualization | Plotly Express, Graph Objects                       |
| Environment   | Python 3.11, virtualenv or conda                    |

## ▶️ Quick Start

1️⃣ Clone this repository
git clone https://github.com/MonicaVenzor/realtime-trading-terminal.git
cd realtime-trading-terminal

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the Dash app
python run.py

4️⃣ Open in browser
http://127.0.0.1:8050/

## 🖼️ Dashboard Preview

<p align="center"> <img src="assets/demo_light.png" width="45%" alt="Light theme preview"> <img src="assets/demo_dark.png" width="45%" alt="Dark theme preview"> </p>

## 💡 Key Highlights

✅ Live market data directly from Yahoo Finance

✅ KPI sparklines with custom Plotly templates

✅ Dual-theme design (light/dark) with smooth transitions

✅ Correlation heatmap for cross-ticker analysis

✅ Modular architecture (src + app separation)

## 🧩 Next Steps

🚀 Add moving averages & Bollinger Bands

🧠 Integrate advanced ML-based forecasting

📈 Include portfolio backtesting features

☁️ Deploy on Render / AWS EC2 with HTTPS

💾 Add caching layer for improved performance

## 👩‍💻 Author

Mónica Venzor
📍 Data Analyst Jr | SQL | Excel | Power BI | Python | Data Visualization | Machine Learning Enthusiast

🔗[LinkedIn](https://www.linkedin.com/in/monicavenzor/) |  — [GitHub](https://github.com/MonicaVenzor)  

## 📜 License

This project is licensed under the MIT License — free for educational and personal use.

---
⭐ If you found this project useful or inspiring, please give it a star!
It helps others discover it and supports more open projects like this 💫
---
