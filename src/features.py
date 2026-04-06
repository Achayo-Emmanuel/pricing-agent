import pandas as pd
import numpy as np

def build_features(df):
    df = df.copy()

    # convert date
    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

    # create week
    df['week'] = df['InvoiceDate'].dt.to_period('W')

    # aggregate to SKU-week
    sku_week = df.groupby(['StockCode', 'week']).agg(
        total_quantity=('Quantity', 'sum'),
        avg_price=('UnitPrice', 'mean'),
        revenue=('Revenue', 'sum')
    ).reset_index()

    # convert week to datetime
    sku_week['week_start'] = sku_week['week'].dt.start_time

    # time features
    sku_week['year'] = sku_week['week_start'].dt.year
    sku_week['month'] = sku_week['week_start'].dt.month
    sku_week['week_of_year'] = sku_week['week_start'].dt.isocalendar().week.astype(int)
    sku_week['quarter'] = sku_week['week_start'].dt.quarter

    # sort
    sku_week = sku_week.sort_values(['StockCode', 'week_start'])

    # lag features
    sku_week['last_week_sales'] = sku_week.groupby('StockCode')['total_quantity'].shift(1)
    sku_week['two_week_sales'] = sku_week.groupby('StockCode')['total_quantity'].shift(2)
    sku_week['four_week_sales'] = sku_week.groupby('StockCode')['total_quantity'].shift(4)

    # rolling average
    sku_week['rolling_4_week_avg_sales'] = (
        sku_week.groupby('StockCode')['total_quantity']
        .transform(lambda x: x.rolling(4).mean())
    )

    # drop NA AFTER features
    sku_week = sku_week.dropna()

    # --- SYNTHETIC FEATURES (FIXED) ---
    sku_week["cost"] = sku_week["avg_price"] * np.random.uniform(0.6, 0.8, len(sku_week))
    sku_week["inventory"] = np.random.randint(50, 500, len(sku_week))
    sku_week["min_margin"] = 0.2

    return sku_week