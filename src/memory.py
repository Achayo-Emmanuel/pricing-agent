import pandas as pd
import os

MEMORY_FILE = "memory.csv"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        return pd.read_csv(MEMORY_FILE)
    else:
        return pd.DataFrame()

def save_memory(record):
    df = load_memory()

    df = pd.concat([df, pd.DataFrame([record])], ignore_index=True)

    df.to_csv(MEMORY_FILE, index=False)

def evaluate_performance():
    df = load_memory()

    df = df.dropna(subset=["actual_demand", "actual_profit"])

    if df.empty:
        return None

    df["demand_error"] = abs(df["actual_demand"] - df["expected_demand"]) / df["expected_demand"]
    df["profit_error"] = abs(df["actual_profit"] - df["expected_profit"]) / df["expected_profit"]

    return {
        "avg_demand_error": df["demand_error"].mean(),
        "avg_profit_error": df["profit_error"].mean()
    }