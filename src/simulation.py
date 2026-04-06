
import numpy as np

def simulate_prices(model, features, df, price_grid):
    results = []

    for price in price_grid:
        temp = df.copy()
        temp["avg_price"] = price

        pred_demand = model.predict(temp[features])

        cost = temp["cost"]

        profit = (price - cost) * pred_demand
        margin = (price - cost) / price

        results.append({
            "price": price,
            "avg_demand": pred_demand.mean(),
            "avg_profit": profit.mean(),
            "avg_margin": margin.mean()
        })

    return results

def recommend_price(sim_results, df, last_price=None, last_profit=None, min_margin=0.2):
    valid = []

    for r in sim_results:
        if r["avg_margin"] < min_margin:
            continue
        if r["price"] <= 0:
            continue
        valid.append(r)

    if not valid:
        return {"error": "No valid pricing options"}

    best = max(valid, key=lambda x: x["avg_profit"])

    # --- baseline ---
    current_price = df["avg_price"].mean()
    current_demand = df["total_quantity"].mean()
    current_profit = (current_price - df["cost"]).mean() * current_demand

    improvement = (best["avg_profit"] - current_profit) / max(current_profit, 1)

    # --- performance memory ---
    performance_factor = 1.0

    if last_profit is not None:
        error = abs(last_profit - best["avg_profit"]) / max(last_profit, 1)

        if error > 0.3:
            performance_factor = 0.5
        elif error < 0.1:
            performance_factor = 1.2

    # --- learning from past (controlled pricing) ---
    if last_price is not None:
        price_change = (best["price"] - last_price) / last_price
        max_change = 0.2 * performance_factor

        if abs(price_change) > max_change:
            best["price"] = last_price * (1 + max_change * (1 if price_change > 0 else -1))
            best["reason"] = best.get("reason", "") + " | Limited price change"

    # --- confidence ---
    data_size = len(df)

    if data_size > 100:
        data_score = 1
    elif data_size > 50:
        data_score = 0.7
    else:
        data_score = 0.4

    confidence = round((data_score + min(improvement, 1)) / 2, 2)
    confidence = min(confidence * performance_factor, 1)

    # --- risk ---
    price_change = abs(best["price"] - current_price) / current_price
    demand_change = abs(best["avg_demand"] - current_demand) / current_demand

    risk = round((price_change + demand_change) / 2, 2)

    # --- reasoning ---
    reason = (
        f"Max profit {round(best['avg_profit'],2)} | "
        f"Margin {round(best['avg_margin']*100,1)}%"
    )

    if last_profit is not None and best["avg_profit"] < last_profit:
        reason += " | Previous profit was higher"

    if performance_factor < 1:
        reason += " | Conservative due to past error"
    elif performance_factor > 1:
        reason += " | Aggressive due to good performance"

    # --- final output ---
    best["confidence"] = confidence
    best["risk"] = risk
    best["reason"] = reason

    return best