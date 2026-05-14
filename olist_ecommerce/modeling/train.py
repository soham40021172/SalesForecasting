# train.py

import joblib
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from xgboost import XGBRegressor
from loguru import logger
from olist_ecommerce.config import MODELS_DIR


def train_model():
    logger.info("🚀 Training Pipeline Started")

    # -------------------------------
    # 1. Load Data
    # -------------------------------
    engine = create_engine(
        'postgresql://postgres:soham%4027@localhost:5432/Olist_Ecommerce'
    )

    df = pd.read_sql('data_engineered_weekly', engine)

    # Fix column types (IMPORTANT BUG FIX)
    df.columns = [str(col) for col in df.columns]

    df = df.sort_values(['category', 'state', 'date'])

    logger.info(f"Data loaded: {df.shape}")

    # -------------------------------
    # 2. Train-Test Split (Time-based)
    # -------------------------------
    split_date = df['date'].quantile(0.8)

    train = df[df['date'] <= split_date]
    test = df[df['date'] > split_date]

    X_train = train.drop(columns=['sales', 'date'])
    y_train = train['sales']

    X_test = test.drop(columns=['sales', 'date'])
    y_test = test['sales']

    # -------------------------------
    # 3. Encoding
    # -------------------------------
    X_train = pd.get_dummies(X_train, columns=['category', 'state'])
    X_test = pd.get_dummies(X_test, columns=['category', 'state'])

    X_train, X_test = X_train.align(X_test, join='left', axis=1, fill_value=0)

    feature_cols = X_train.columns.tolist()

    # -------------------------------
    # 4. Model Training
    # -------------------------------
    model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.05,
        max_depth=5,
        random_state=42
    )

    logger.info("Training XGBoost...")
    model.fit(X_train, y_train)

    logger.success("Model training completed")

    # -------------------------------
    # 5. Save Artifacts
    # -------------------------------
    artifacts = {
        "model": model,
        "feature_cols": feature_cols,
        "data": df
    }

    save_path = MODELS_DIR / "xgb_model.pkl"
    joblib.dump(artifacts, save_path)

    logger.success(f"Model saved at: {save_path}")