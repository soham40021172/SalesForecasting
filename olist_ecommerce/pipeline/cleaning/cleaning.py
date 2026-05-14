# cleaning.py

import pandas as pd
from loguru import logger
from olist_ecommerce.db.connection import engine

# =============================
# LOAD DATA
# =============================
def load_master_table():
    logger.info("Loading master table...")
    query = "SELECT * FROM olist_master_table"
    df = pd.read_sql(query, engine)
    return df

# =============================
# CLEANING
# =============================
def clean_data(df):
    logger.info("Cleaning data...")
    # Remove null categories and invalid prices/freight
    df = df.dropna(subset=['product_category_name_english'])
    df = df[df['price'] > 0]
    df['date'] = pd.to_datetime(df['date'])
    return df

# =============================
# PARETO FILTERING (80% THRESHOLD)
# =============================
def apply_pareto_grouping(df, threshold=80):
    logger.info(f"Applying Pareto grouping (Threshold: {threshold}%)...")

    # 1. Top Categories Logic
    cat_sales = df.groupby('product_category_name_english')['order_item_id'].count().sort_values(ascending=False)
    cum_perc_cat = (cat_sales.cumsum() / cat_sales.sum()) * 100
    head_val_cat = (cum_perc_cat <= threshold).sum() + 1
    top_categories = cum_perc_cat.head(head_val_cat).index.tolist()

    # 2. Top States Logic
    state_sales = df.groupby('customer_state')['order_item_id'].count().sort_values(ascending=False)
    cum_perc_state = (state_sales.cumsum() / state_sales.sum()) * 100
    head_val_state = (cum_perc_state <= threshold).sum() + 1
    top_states = cum_perc_state.head(head_val_state).index.tolist()

    # Apply "Other" labeling
    df['product_category_name_english'] = df['product_category_name_english'].apply(
        lambda x: x if x in top_categories else 'Other'
    )
    df['customer_state'] = df['customer_state'].apply(
        lambda x: x if x in top_states else 'Other'
    )

    return df

# =============================
# AGGREGATE DAILY SALES
# =============================
def aggregate_daily_sales(df):
    logger.info("Aggregating daily sales...")
    
    daily_sales = df.groupby(
        ['date', 'product_category_name_english', 'customer_state']
    ).agg(
        sales=('order_item_id', 'count'),
        revenue=('price', 'sum')
    ).reset_index()

    daily_sales = daily_sales.rename(columns={
        'product_category_name_english': 'category',
        'customer_state': 'state'
    })
    return daily_sales

# =============================
# FILL MISSING DATES
# =============================
def fill_missing_dates(daily_sales):
    logger.info("Filling missing dates in time series...")
    
    full_date_range = pd.date_range(
        start=daily_sales['date'].min(),
        end=daily_sales['date'].max()
    )

    filled_list = []
    for (category, state), group in daily_sales.groupby(['category', 'state']):
        group = group.set_index('date').reindex(full_date_range)
        group['category'] = category
        group['state'] = state
        group['sales'] = group['sales'].fillna(0)
        group['revenue'] = group['revenue'].fillna(0)
        
        filled_list.append(group.reset_index().rename(columns={'index': 'date'}))

    final_df = pd.concat(filled_list, ignore_index=True)
    return final_df.sort_values(['category', 'state', 'date']).reset_index(drop=True)

# =============================
# WEEKLY RESAMPLING
# =============================
def resample_to_weekly(df):
    logger.info("Resampling data to weekly frequency...")
    df['date'] = pd.to_datetime(df['date'])
    
    # Set index for resampling
    df_weekly = df.set_index('date').groupby(['category', 'state']).resample('W').agg({
        'sales': 'sum',
        'revenue': 'sum'
    }).reset_index()
    
    return df_weekly

# =============================
# SAVE TO DATABASE
# =============================
def save_to_db(df, table_name):
    logger.info(f"Saving {len(df)} rows to {table_name}...")
    df.to_sql(table_name, engine, if_exists='replace', index=False)
    logger.success(f"Table {table_name} saved successfully!")

# =============================
# RUN FULL PIPELINE
# =============================
def run_cleaning_pipeline():
    # 1. Load & Clean
    df = load_master_table()
    df = clean_data(df)

    # 2. Apply Notebook Logic (Pareto + Othering)
    df = apply_pareto_grouping(df, threshold=80)

    # 3. Aggregate Daily
    daily_sales = aggregate_daily_sales(df)
    
    # 4. Fill gaps (zeros for missing dates)
    daily_filled = fill_missing_dates(daily_sales)
    save_to_db(daily_filled, "olist_daily_sales_filled")

    # 5. Resample to Weekly (New Notebook Step)
    weekly_sales = resample_to_weekly(daily_filled)
    save_to_db(weekly_sales, "olist_weekly_sales")

if __name__ == "__main__":
    run_cleaning_pipeline()