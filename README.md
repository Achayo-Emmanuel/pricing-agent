# AI Pricing Optimization Agent

An end-to-end pricing intelligence system that recommends optimal product prices using machine learning, simulation, and AI-generated business explanations.

---

## Problem

Pricing decisions are often:
- Manual and inconsistent
- Not data-driven
- Lacking clear justification

Businesses struggle to identify:
- Which products to adjust pricing for
- How pricing impacts profit
- Whether a pricing decision is risky

---

## Solution

This project builds a **pricing optimization agent** that:

- Predicts demand using machine learning
- Simulates pricing scenarios
- Identifies high-profit opportunities
- Assigns risk and confidence scores
- Uses AI (LLM) to explain recommendations in plain English

---

## How It Works

Input Data → Feature Engineering → Demand Model → Price Simulation → Optimization → Decision Layer → LLM Explanation



## Key Features

- **Batch Pricing Optimization**
  - Identifies top profit opportunities across SKUs

- **Decision Intelligence Layer**
  - Confidence scoring
  - Risk scoring
  - Clear action signals:
    - 🟢 Increase Price
    - 🟡 Test Carefully
    - 🔴 Risky

- **AI-Powered Explanations**
  - Converts model outputs into business insights
  - Explains *why* a price is recommended

- **Interactive Dashboard (Streamlit)**
  - Single SKU optimization
  - Top opportunities view
  - Real-time insights

---

## Dashboard Preview

### Top Opportunities View
-check sreenshot folder for images

### AI Explanation Example
-check sreenshot folder for images

---

## Tech Stack

- **Python**
- **Pandas / NumPy**
- **Scikit-learn (Random Forest)**
- **Streamlit (Dashboard UI)**
- **OpenAI API (LLM explanations)**

---

## Example Output

| SKU | Price | Profit | Confidence | Risk | Decision |
|-----|------|--------|------------|------|----------|
| 85123A | 12.5 | 2400 | 0.78 | 0.22 | 🟢 Increase Price |

💡 Explanation:
> "Increasing price improves profit while demand remains stable, indicating low elasticity and low risk."

---

## Live Demo

👉 [Streamlit App Link Here]

---

##Business Impact

This system transforms pricing from:
- Guesswork → Data-driven decisions  
- Raw numbers → Actionable insights  
- Static models → Explainable intelligence  

---

##Future Improvements

- Upload custom datasets
- Batch LLM explanations
- Exportable pricing reports
- Integration with e-commerce platforms

---

Author: Emmanuel Achayo

Data Analyst | Machine Learning | Decision Intelligence Systems