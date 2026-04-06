import streamlit as st

from main import run_price_optimization_for_sku, run_batch_pricing
from data import load_data, clean_data
from features import build_features

# --- Load data once ---
@st.cache_data
def load_pipeline():
    df = load_data("data/OnlineRetail.csv")
    df = clean_data(df)
    df_feat = build_features(df)
    return df_feat

df_feat = load_pipeline()

st.title("📈 Pricing Optimization Agent")

# --- Tabs ---
tab1, tab2 = st.tabs(["Single SKU", "Top Opportunities"])

# -----------------------------
# TAB 1: Single SKU
# -----------------------------
with tab1:
    st.header("Optimize Single SKU")

    sku = st.text_input("Enter SKU")

    if st.button("Run Optimization"):
        if sku:
            result = run_price_optimization_for_sku(df_feat, sku)

            if result is None or "error" in result:
                st.error("No data for this SKU")
            else:
                st.success("Recommendation")

                st.metric("Recommended Price", round(result["price"], 2))
                st.metric("Expected Profit", round(result.get("avg_profit", 0), 2))

                st.write("Confidence:", result.get("confidence"))
                st.write("Risk:", result.get("risk"))
                st.write("Reason:", result.get("reason"))
        else:
            st.warning("Enter a SKU")

# -----------------------------
# TAB 2: Batch
# -----------------------------
with tab2:
    st.header("Top Pricing Opportunities")

    top_n = st.slider("Number of SKUs", 1, 20, 5)

    if st.button("Find Opportunities"):
        results = run_batch_pricing(df_feat, top_n=top_n)

        for r in results:
            st.markdown("---")
            st.subheader(f"SKU: {r['sku']}")

            st.metric("Price", round(r["price"], 2))
            st.metric("Profit", round(r.get("avg_profit", 0), 2))

            st.write("Confidence:", r.get("confidence"))
            st.write("Risk:", r.get("risk"))
            st.write("Reason:", r.get("reason"))


            
