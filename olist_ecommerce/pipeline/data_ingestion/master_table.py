# master_table.py

import pandas as pd
from loguru import logger
from olist_ecommerce.db.connection import engine


def fetch_raw_tables():
    try:
        logger.info("Fetching raw tables from database...")

        customers = pd.read_sql("SELECT * FROM customers", engine)
        orders = pd.read_sql("SELECT * FROM orders", engine)
        items = pd.read_sql("SELECT * FROM order_items", engine)
        products = pd.read_sql("SELECT * FROM products", engine)
        sellers = pd.read_sql("SELECT * FROM sellers", engine)
        translation = pd.read_sql("SELECT * FROM product_category_name_translation", engine)

        logger.success("All tables fetched successfully")

        return customers, orders, items, products, sellers, translation

    except Exception as e:
        logger.error(f"Error fetching tables: {e}")
        raise


def preprocess_tables(customers, orders, items, products, sellers, translation):

    logger.info("Preprocessing tables...")

    # Convert datetime
    orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

    # Filter delivered orders
    orders_clean = orders[orders['order_status'] == 'delivered'][
        ['order_id', 'customer_id', 'order_purchase_timestamp']
    ]

    customers_clean = customers[['customer_id', 'customer_state', 'customer_city']]
    items_clean = items[['order_id', 'product_id', 'seller_id', 'order_item_id', 'price', 'freight_value']]
    products_clean = products[['product_id', 'product_category_name']]
    sellers_clean = sellers[['seller_id', 'seller_state']]

    return orders_clean, customers_clean, items_clean, products_clean, sellers_clean, translation


def create_master_table():

    customers, orders, items, products, sellers, translation = fetch_raw_tables()

    orders_clean, customers_clean, items_clean, products_clean, sellers_clean, translation = preprocess_tables(
        customers, orders, items, products, sellers, translation
    )

    logger.info("Creating master table...")

    df = items_clean.merge(orders_clean, on='order_id', how='inner') \
        .merge(products_clean, on='product_id', how='left') \
        .merge(translation, on='product_category_name', how='left') \
        .merge(customers_clean, on='customer_id', how='left') \
        .merge(sellers_clean, on='seller_id', how='left')

    # Create date column
    df['date'] = df['order_purchase_timestamp'].dt.date
    df['date'] = pd.to_datetime(df['date'])

    logger.success(f"Master table created with shape: {df.shape}")

    return df


def save_master_table(df):

    try:
        logger.info("Saving master table to database...")

        df.to_sql(
            'olist_master_table',
            engine,
            if_exists='replace',
            index=False
        )

        logger.success("Master table saved successfully")

    except Exception as e:
        logger.error(f"Error saving master table: {e}")
        raise


def run_data_pipeline():
    df = create_master_table()
    save_master_table(df)


if __name__ == "__main__":
    run_data_pipeline()