from main import run_price_optimization_for_sku, run_batch_pricing
from data import load_data, clean_data
from features import build_features


class PricingAgent:
    def __init__(self):
        df = load_data("data/OnlineRetail.csv")
        df = clean_data(df)
        self.df_feat = build_features(df)

    def run(self, query):
        query = query.lower()

        # --- TOOL SELECTION ---
        if "top" in query or "best" in query:
            results = run_batch_pricing(self.df_feat, top_n=5)
            return self._format_batch(results)

        elif "sku" in query:
            # naive extraction
            sku = query.split()[-1]
            result = run_price_optimization_for_sku(self.df_feat, sku)
            return self._format_single(sku, result)

        else:
            return "I can help with pricing decisions. Ask about a SKU or top opportunities."

    def _format_single(self, sku, r):
        if r is None or "error" in r:
            return f"No data for SKU {sku}"

        return (
            f"SKU {sku}: Recommended price {round(r['price'],2)}. "
            f"Expected profit {round(r.get('avg_profit',0),2)}. "
            f"Confidence {r.get('confidence')}, Risk {r.get('risk')}."
        )

    def _format_batch(self, results):
        output = "Top pricing opportunities:\n"

        for r in results:
            output += (
                f"- SKU {r['sku']}: price {round(r['price'],2)}, "
                f"profit {round(r.get('avg_profit',0),2)}\n"
            )

        return output