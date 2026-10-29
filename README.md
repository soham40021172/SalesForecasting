# Olist E-Commerce Sales Forecasting

A forecasting project built on the Brazilian Olist e-commerce dataset. It predicts weekly sales for each product category and customer state, and includes a Streamlit app and a Power BI dashboard for business users.

**Live demo:** https://salesforecasting-ytxxhyydyskckbmyhg5lqk.streamlit.app/

## Results

- Consolidated a 9-table PostgreSQL database into a clean 16,720-row weekly dataset, reducing zero-inflation by about 90%
- XGBoost regressor with MAE 3.27 and RMSE 6.82
- Poisson-based probabilities for demand surges and drops in each forecast week

## Demo

- [Full project explanation](https://youtu.be/EZQIIcms6GI)
- [Power BI dashboard walkthrough](https://youtu.be/YbEaK842h-k)

## How it works

```text
Raw Olist data -> ingestion -> cleaning -> feature engineering -> PostgreSQL -> XGBoost -> forecasts -> Streamlit app / Power BI
```

- **Problem:** a supervised regression task. The target is weekly `sales` for each category and state.
- **Features:** lags (1, 2, 4 and 8 weeks), 4-week rolling mean and standard deviation, month, week of year, and Black Friday and Christmas week flags.
- **Why lag features:** sales in a given week depend heavily on recent weeks, so lags capture trend, momentum and seasonality.
- **Why XGBoost:** it handles nonlinear patterns and feature interactions well on tabular data.
- **Forecasting:** future weeks are predicted recursively, with each prediction feeding the next.

## Dashboards

- **Streamlit app:** forecast by category and state, KPI cards, trend charts and surge probabilities.
- **Power BI:** revenue analysis, operational KPIs, delivery performance, category insights, monthly sales trends and review analytics.

## Key insights

- Health and beauty is the top revenue-driving category
- Delivery delays are linked to lower review scores
- Black Friday weeks show major demand spikes
- Seasonality strongly affects product categories

## Tech stack

Python, Pandas, NumPy, Scikit-learn, XGBoost, SciPy, PostgreSQL, SQLAlchemy, Streamlit, Power BI, Plotly, Matplotlib

## Getting started

**1. Set up the environment**

```bash
git clone <repository-url>
cd olist-ecommerce-forecasting
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Create the database**

```sql
CREATE DATABASE Olist_Ecommerce;
```

Then update the database credentials in `config.py`.

**3. Run the pipeline**

```bash
python -m olist_ecommerce.runpipeline --mode all       # ingestion, cleaning, features, training, forecast
python -m olist_ecommerce.runpipeline --mode train     # train only
python -m olist_ecommerce.runpipeline --mode predict --category bed_bath_table --state SP
```

**4. Launch the app**

```bash
streamlit run app.py
```

## Project structure

```text
olist_ecommerce/
  pipeline/     ingestion, cleaning and feature engineering
  modeling/     training and prediction
  db/           database connection
  config.py
  runpipeline.py
data/  models/  notebooks/  reports/  tests/
```

## Future improvements

- Prophet and LSTM forecasting models
- Docker deployment
- Inventory optimization using the forecasts

## Author

Soham Gaichor
