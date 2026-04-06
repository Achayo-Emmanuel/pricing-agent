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


if __name__ == "__main__":
    df = load_data("data/OnlineRetail.csv")
    df = clean_data(df)
    df_feat = build_features(df)

    results = run_batch_pricing(df_feat, top_n=5)

    from memory import save_memory
    import datetime

    for r in results:
        import random

        actual_profit = float(r.get("avg_profit", 0)) * random.uniform(0.8, 1.2)
        actual_demand = float(r.get("avg_demand", 0)) * random.uniform(0.8, 1.2)
        print("\n---")
        print("SKU:", r["sku"])
        print("Price:", float(r["price"]))
        print("Profit:", float(r.get("avg_profit", 0)))
        print("Reason:", r["reason"])
        print("Confidence:", r.get("confidence"))
        print("Risk:", r.get("risk"))

        # ✅ SAVE EACH SKU
        save_memory({
            "sku": r["sku"],
            "recommended_price": float(r["price"]),
            "expected_demand": float(r.get("avg_demand", 0)),
            "expected_profit": float(r.get("avg_profit", 0)),
            "actual_demand": actual_demand,
            "actual_profit": actual_profit,
            "confidence": r.get("confidence"),
            "risk": r.get("risk"),
            "timestamp": datetime.datetime.now()
 })
import random

# simulate real-world noise (±20%)
actual_profit = float(r.get("avg_profit", 0)) * random.uniform(0.8, 1.2)
actual_demand = float(r.get("avg_demand", 0)) * random.uniform(0.8, 1.2)