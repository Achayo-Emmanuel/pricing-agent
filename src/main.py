from data import load_data, clean_data
from features import build_features
from model import train_demand_model
from simulation import simulate_prices, recommend_price

import numpy as np
import pandas as pd


def run_price_optimization_for_sku(df_feat, sku):
    sku_df = df_feat[df_feat["StockCode"] == sku]

    from memory import load_memory

    memory = load_memory()
    if "sku" in memory.columns:
     past = memory[memory["sku"] == sku]
    else:
       past = pd.DataFrame()

    last_price = None
    last_profit = None

    if not past.empty:
        last_record = past.iloc[-1]
        last_price = last_record["recommended_price"]
        last_profit = last_record.get("expected_profit", None)

    if len(sku_df) < 20:
        return {"error": "Not enough data for this SKU"}

    model, features = train_demand_model(sku_df)

    # 🔥 FIXED price grid (realistic)
    current_price = sku_df["avg_price"].mean()
    price_grid = np.linspace(current_price * 0.7, current_price * 1.3, 10)

    sim_results = simulate_prices(model, features, sku_df, price_grid)

    # ✅ THIS WAS MISSING
    recommendation = recommend_price(sim_results, sku_df, last_price, last_profit)

    return recommendation


def run_batch_pricing(df_feat, top_n=10):
    results = []

    skus = df_feat["StockCode"].unique()

    for sku in skus:
        rec = run_price_optimization_for_sku(df_feat, sku)

        if rec is None or "error" in rec:
            continue

        rec["sku"] = sku
        results.append(rec)

    results = sorted(
        results,
        key=lambda x: x.get("avg_profit", 0),
        reverse=True
    )

    return results[:top_n]

