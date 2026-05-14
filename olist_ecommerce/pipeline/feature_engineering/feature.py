# feature.py

import pandas as pd
from loguru import logger
from olist_ecommerce.db.connection import engine

# =============================
# LOAD DATA
# =============================
def load_data():
    """Loads the weekly cleaned data from the database."""
    logger.info("Loading weekly sales data...")
    # Note: Ensure the table name matches what you saved in the previous step
    query = "SELECT * FROM olist_weekly_sales" 
    df = pd.read_sql(query, engine)
    df['date'] = pd.to_datetime(df['date'])
    return df

# =============================
# FEATURE ENGINEERING
# =============================
def create_features(df):
    logger.info("Creating weekly features...")

    # Sort to ensure time series integrity
    df = df.sort_values(['category', 'state', 'date']).reset_index(drop=True)

    # 1. TIME FEATURES
    df['month'] = df['date'].dt.month
    df['week_of_year'] = df['date'].dt.isocalendar().week.astype(int)

    # 2. LAG FEATURES (Weeks 1, 2, 4, and 8)
    logger.info("Calculating lag features...")
    group_cols = ['category', 'state']
    df['lag_1'] = df.groupby(group_cols)['sales'].shift(1)
    df['lag_2'] = df.groupby(group_cols)['sales'].shift(2)
    df['lag_4'] = df.groupby(group_cols)['sales'].shift(4)
    df['lag_8'] = df.groupby(group_cols)['sales'].shift(8)
    
    # Revenue lag (matching notebook)
    df['revenue_lag_1'] = df.groupby(group_cols)['revenue'].shift(1)

    # 3. ROLLING FEATURES (4-week window)
    logger.info("Calculating rolling statistics...")
    df['rolling_mean_4'] = df.groupby(group_cols)['sales'] \
                             .shift(1).rolling(4).mean()
    
    df['rolling_std_4'] = df.groupby(group_cols)['sales'] \
                            .shift(1).rolling(4).std()

    # 4. EVENT FEATURES
    logger.info("Adding holiday flags...")
    # Black Friday Week (Usually weeks 47-48)
    df['is_black_friday_week'] = (
        (df['date'].dt.month == 11) & 
        (df['week_of_year'].between(47, 48))
    ).astype(int)

    # Christmas Week
    df['is_christmas_week'] = (
        (df['date'].dt.month == 12) & 
        (df['date'].dt.day >= 20)
    ).astype(int)

    # 5. CLEANUP
    # Drop rows where lag/rolling features are NaN
    initial_shape = df.shape
    df = df.dropna(subset=[
        'lag_1', 'lag_2', 'lag_4', 'lag_8', 
        'rolling_mean_4', 'rolling_std_4'
    ])
    
    logger.info(f"Dropped {initial_shape[0] - df.shape[0]} rows due to NaN values.")
    logger.success("Feature engineering completed")

    return df

# =============================
# SAVE TO DB
# =============================
def save_to_db(df):
    table_name = 'data_engineered_weekly'
    logger.info(f"Saving features to {table_name}...")
    df.to_sql(
        table_name,
        engine,
        if_exists='replace',
        index=False
    )
    logger.success(f"{table_name} saved successfully!")

# =============================
# RUN PIPELINE
# =============================
def run_feature_pipeline():
    try:
        df = load_data()
        df = create_features(df)
        save_to_db(df)
    except Exception as e:
        logger.error(f"Pipeline failed: {e}")

if __name__ == "__main__":
    run_feature_pipeline()