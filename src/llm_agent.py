from openai import OpenAI
import os

# Initialize client using environment variable
from openai import OpenAI
import os

# Initialize client using environment variable
client = OpenAI()

def explain_row(row):
    """
    Generate a short business explanation for a pricing recommendation.
    Expects a pandas row with:
    SKU, Recommended Price, Expected Profit, Confidence, Risk, Decision
    """

    prompt = f"""
    You are a pricing strategy expert.

    Given the following recommendation:

    SKU: {row['SKU']}
    Recommended Price: {row['Recommended Price']}
    Expected Profit: {row['Expected Profit']}
    Confidence: {row['Confidence']}
    Risk: {row['Risk']}
    Decision: {row['Decision']}

    Explain in simple business language:
    - Why this price is recommended
    - What the risk level means
    - What action should be taken

    Keep it concise (2–3 sentences).
    """

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return getattr(response, "output_text", "No explanation generated")

    except Exception as e:
        return f"Error generating explanation: {str(e)}"


def explain_row(row):
    """
    Generate a short business explanation for a pricing recommendation.
    Expects a pandas row with:
    SKU, Recommended Price, Expected Profit, Confidence, Risk, Decision
    """

    prompt = f"""
    You are a pricing strategy expert.

    Given the following recommendation:

    SKU: {row['SKU']}
    Recommended Price: {row['Recommended Price']}
    Expected Profit: {row['Expected Profit']}
    Confidence: {row['Confidence']}
    Risk: {row['Risk']}
    Decision: {row['Decision']}

    Explain in simple business language:
    - Why this price is recommended
    - What the risk level means
    - What action should be taken

    Keep it concise (2–3 sentences).
    """

    try:
        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"Error generating explanation: {str(e)}"