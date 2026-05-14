# predict.py

import joblib
import numpy as np
import pandas as pd
from scipy.stats import poisson
from loguru import logger
from olist_ecommerce.config import MODELS_DIR


def predict_segment(category, state, weeks=6):
    logger.info(f"🔮 Predicting for {category} - {state}")

    # -------------------------------
    # 1. Load Artifacts
    # -------------------------------
    artifacts = joblib.load(MODELS_DIR / "xgb_model.pkl")

    model = artifacts["model"]
    feature_cols = artifacts["feature_cols"]
    df = artifacts["data"]

    # -------------------------------
    # 2. Filter Segment
    # -------------------------------
    segment = df[(df['category'] == category) & (df['state'] == state)].copy()

    if segment.empty:
        logger.error("❌ No data found for this segment")
        return None

    segment = segment.sort_values('date')
    history = segment.tail(8).copy()

    results = []

    # -------------------------------
    # 3. Iterative Forecast
    # -------------------------------
    for i in range(weeks):

        last_row = history.iloc[-1:].copy()
        next_date = last_row['date'].iloc[0] + pd.Timedelta(days=7)

        new_row = last_row.copy()
        new_row['date'] = next_date

        # ---- Lag Features ----
        new_row['lag_1'] = history['sales'].iloc[-1]
        new_row['lag_2'] = history['sales'].iloc[-2]
        new_row['lag_4'] = history['sales'].iloc[-4]
        new_row['lag_8'] = history['sales'].iloc[-8]

        # ---- Time Features ----
        new_row['month'] = next_date.month
        new_row['week_of_year'] = int(next_date.isocalendar().week)

        # ---- Rolling ----
        new_row['rolling_mean_4'] = history['sales'].tail(4).mean()
        new_row['rolling_std_4'] = history['sales'].tail(4).std()

        # ---- Events ----
        new_row['is_black_friday_week'] = int(
            (next_date.month == 11) and (20 <= next_date.day <= 30)
        )

        new_row['is_christmas_week'] = int(
            (next_date.month == 12) and (next_date.day >= 20)
        )

        # -------------------------------
        # 4. Prepare Model Input
        # -------------------------------
        X_pred = new_row.drop(columns=['sales', 'date', 'revenue'], errors='ignore')

        X_pred = pd.get_dummies(X_pred, columns=['category', 'state'])
        X_pred = X_pred.reindex(columns=feature_cols, fill_value=0)

        # -------------------------------
        # 5. Prediction
        # -------------------------------
        pred = model.predict(X_pred)[0]
        pred = max(0, pred)

        # -------------------------------
        # 6. Poisson Probability
        # -------------------------------
        lam = max(pred, 1e-6)

        prob_increase = 1 - poisson.cdf(pred, lam)
        prob_decrease = poisson.cdf(pred, lam)

        results.append({
            "week": i + 1,
            "date": next_date,
            "predicted_sales": round(pred, 2),
            "increase_prob (%)": round(prob_increase * 100, 2),
            "decrease_prob (%)": round(prob_decrease * 100, 2)
        })

        # -------------------------------
        # 7. Update History
        # -------------------------------
        new_row['sales'] = pred
        history = pd.concat([history, new_row], ignore_index=True)

    logger.success("✅ Forecast Completed")

    return pd.DataFrame(results)