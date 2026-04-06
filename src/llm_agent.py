from openai import OpenAI
import json

from main import run_price_optimization_for_sku, run_batch_pricing
from data import load_data, clean_data
from features import build_features

client = OpenAI()

df = load_data("data/OnlineRetail.csv")
df = clean_data(df)
df_feat = build_features(df)

tools = [
    {
        "type": "function",
        "name": "run_price_optimization_for_sku",
        "description": "Recommend a price for a single SKU using the pricing engine.",
        "parameters": {
            "type": "object",
            "properties": {
                "sku": {
                    "type": "string",
                    "description": "The product SKU to optimize."
                }
            },
            "required": ["sku"],
            "additionalProperties": False
        }
    },
    {
        "type": "function",
        "name": "run_batch_pricing",
        "description": "Return the top pricing opportunities across SKUs.",
        "parameters": {
            "type": "object",
            "properties": {
                "top_n": {
                    "type": "integer",
                    "description": "How many top opportunities to return."
                }
            },
            "required": ["top_n"],
            "additionalProperties": False
        }
    }
]

def call_tool(name, args):
    if name == "run_price_optimization_for_sku":
        return run_price_optimization_for_sku(df_feat, args["sku"])
    if name == "run_batch_pricing":
        return run_batch_pricing(df_feat, top_n=args["top_n"])
    raise ValueError(f"Unknown tool: {name}")

user_query = "What is the best price for SKU 10135?"

response = client.responses.create(
    model="gpt-5.4",
    input=user_query,
    tools=tools
)

for item in response.output:
    if item.type == "function_call":
        tool_name = item.name
        tool_args = json.loads(item.arguments)
        tool_result = call_tool(tool_name, tool_args)

        followup = client.responses.create(
            model="gpt-5.4",
            previous_response_id=response.id,
            input=[{
                "type": "function_call_output",
                "call_id": item.call_id,
                "output": json.dumps(tool_result)
            }]
        )

        print(followup.output_text)