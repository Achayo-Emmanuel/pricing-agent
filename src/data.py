import pandas as pd

def load_data(path):
    return pd.read_csv(path, encoding='ISO-8859-1')


def clean_data(df):
    df = df.copy()

    # remove cancellations
    df = df[~df['InvoiceNo'].astype(str).str.startswith('C')]

    # remove bad rows
    df = df[df['Quantity'] > 0]
    df = df[df['UnitPrice'] > 0]

    # drop missing customers
    df = df.dropna(subset=['CustomerID'])

    # create revenue
    df['Revenue'] = df['Quantity'] * df['UnitPrice']

    # 🔥 FILTER SKUs WITH PRICE VARIATION
    price_variation = df.groupby("StockCode")["UnitPrice"].nunique()
    valid_skus = price_variation[price_variation >= 3].index
    df = df[df["StockCode"].isin(valid_skus)]

    return df