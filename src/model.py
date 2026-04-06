from sklearn.ensemble import RandomForestRegressor

def train_demand_model(df):
    features = [
        "avg_price",
        "month",
        "week_of_year",
        "quarter",
        "last_week_sales",
        "two_week_sales",
        "four_week_sales",
        "rolling_4_week_avg_sales"
    ]

    target = "total_quantity"

    X = df[features]
    y = df[target]

    model = RandomForestRegressor(
        n_estimators=300,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X, y)

    return model, features