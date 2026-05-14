# 🛒 Olist E-Commerce Sales Forecasting & Business Intelligence Platform

An end-to-end Machine Learning and Analytics platform built on the Brazilian Olist E-Commerce dataset.

This project combines:

- Advanced Time Series Forecasting
- Automated ML Pipelines
- PostgreSQL Data Warehousing
- Streamlit Web Application
- Power BI Executive Dashboards
- Business Intelligence & Operational Insights

The system predicts future weekly sales for each product category and customer state combination using lag-based forecasting and probabilistic demand analysis.

---

# 🚀 Project Overview

This platform helps businesses:

- Forecast future product demand
- Identify high-growth categories
- Monitor operational KPIs
- Analyze delivery performance
- Detect seasonal sales surges
- Support inventory & logistics planning

The project simulates a production-ready ML forecasting workflow used in modern e-commerce companies.

---

# 🏗️ System Architecture

```text
Raw Olist Dataset
       ↓
Data Ingestion Pipeline
       ↓
Data Cleaning Pipeline
       ↓
Feature Engineering Pipeline
       ↓
PostgreSQL Data Warehouse
       ↓
Machine Learning Training
       ↓
Forecasting Engine
       ↓
Streamlit Application
       ↓
Power BI Executive Dashboard
```

---

# 📊 Features

## ✅ Machine Learning Forecasting

- Weekly sales forecasting
- Category + State level predictions
- XGBoost forecasting model
- Lag-based temporal learning
- Rolling statistics features
- Seasonal event detection
- Future recursive forecasting

---

## ✅ Probabilistic Forecasting

Poisson distribution based:

- Demand surge probability
- Demand drop probability
- Sales risk estimation

---

## ✅ Automated ML Pipelines

CLI pipeline execution:

```bash
python -m olist_ecommerce.runpipeline --mode all
```

Supports:

- Data ingestion
- Cleaning
- Feature engineering
- Model training
- Forecasting

---

## ✅ Executive Power BI Dashboard

Interactive dashboards including:

- Revenue Analysis
- Operational KPIs
- Delivery Performance
- Product Category Insights
- Monthly Sales Trends
- Review Analytics

---

## ✅ Streamlit Application

Interactive web application:

- Forecast by category/state
- Visual demand predictions
- KPI cards
- Trend charts
- Probabilistic forecasting insights
- Dashboard embedding support

---

# 🧠 Machine Learning Approach

## Forecasting Problem

This is a supervised regression problem where:

### Target Variable

```python
sales
```

### Key Features

```python
lag_1
lag_2
lag_4
lag_8
rolling_mean_4
rolling_std_4
month
week_of_year
is_black_friday_week
is_christmas_week
```

---

## Why Lag Features?

Lag features help the model learn:

- Historical demand patterns
- Seasonality
- Momentum shifts
- Sales trends
- Weekly dependencies

Example:

```text
Sales this week depends heavily on previous weeks' sales.
```

---

## Why XGBoost?

XGBoost was selected because it:

- Handles nonlinear patterns
- Works well on tabular data
- Captures feature interactions
- Handles sparse data efficiently
- Performs strongly on forecasting tasks

---

# 🛠️ Tech Stack

## Backend & ML

- Python
- Pandas
- NumPy
- Scikit-Learn
- XGBoost
- SciPy

---

## Database

- PostgreSQL
- SQLAlchemy

---

## Visualization

- Power BI
- Matplotlib
- Plotly

---

## Deployment

- Streamlit
- GitHub

---

# 📂 Project Structure

```text
olist_ecommerce/
│
├── data/
│
├── models/
│
├── notebooks/
│
├── logs/
│
├── reports/
│
├── tests/
│
├── olist_ecommerce/
│   │
│   ├── pipeline/
│   │   ├── cleaning/
│   │   ├── data_ingesation/
│   │   └── feature_engineering/
│   │
│   ├── modeling/
│   │   ├── train.py
│   │   └── predict.py
│   │
│   ├── db/
│   │
│   ├── config.py
│   └── runpipeline.py
│
└── README.md
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone <your-repo-link>
cd olist-ecommerce-forecasting
```

---

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

Activate:

### Windows

```bash
venv\Scripts\activate
```

### Linux/Mac

```bash
source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🗄️ PostgreSQL Setup

Create database:

```sql
CREATE DATABASE Olist_Ecommerce;
```

Update database credentials inside:

```python
config.py
```

---

# ▶️ Running Pipelines

## Run Full Pipeline

```bash
python -m olist_ecommerce.runpipeline --mode all
```

---

## Train Model Only

```bash
python -m olist_ecommerce.runpipeline --mode train
```

---

## Generate Forecast

```bash
python -m olist_ecommerce.runpipeline --mode predict --category bed_bath_table --state SP
```

---

# 📈 Forecast Example

| Week | Forecast Sales | Surge Probability |
|------|-----------------|------------------|
| 1 | 112 | 71% |
| 2 | 118 | 76% |
| 3 | 125 | 81% |

---

# 📊 Power BI Dashboard

The project includes:

- Executive KPI dashboard
- Revenue trend analysis
- Product category performance
- Logistics & delivery analysis
- Customer satisfaction insights

---

# 🌐 Streamlit App

Run locally:

```bash
streamlit run app.py
```

---

# 📌 Key Business Insights

- Health & Beauty is the top revenue-driving category
- Delivery delays negatively affect review scores
- Black Friday weeks show major demand spikes
- Seasonal trends strongly impact product categories

---

# 🔮 Future Improvements

- LSTM / Deep Learning Forecasting
- Prophet Time Series Models
- Real-time Streaming Forecasts
- Docker Deployment
- CI/CD Automation
- AWS/GCP Deployment
- Inventory Optimization Engine

---

# 📚 Learning Outcomes

This project demonstrates:

- End-to-End ML Engineering
- Time Series Forecasting
- Production ML Pipelines
- Data Warehousing
- Business Intelligence
- Dashboard Engineering
- Model Deployment

---

# 👨‍💻 Author

## Soham

Machine Learning | Data Science | Analytics Engineering

---

# ⭐ If You Like This Project

Give this repository a ⭐ on GitHub.