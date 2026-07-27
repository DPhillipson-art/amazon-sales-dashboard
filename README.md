Markdown
# 🛒 Amazon Sales Analytics Dashboard

An interactive Streamlit dashboard analyzing prices, discounts, ratings, and product categories across top Amazon listings.

---

## 🚀 Quickstart & Setup Instructions

### 1. Clone the repository
```bash
git clone [https://github.com/DPhillipson-art/amazon-sales-dashboard.git](https://github.com/DPhillipson-art/amazon-sales-dashboard.git)
cd amazon-sales-dashboard
2. Download Data
Unzip the downloaded dataset and place amazon.csv into:
data/raw/amazon.csv

3. Install Dependencies
Bash
uv sync
4. Run the Dashboard
Bash
uv run --native-tls streamlit run app.py
🧹 Data Cleaning & Preprocessing Justification
The raw Amazon Sales Dataset contained several formatting inconsistencies and non-numeric values that required explicit handling:

Prices (discounted_price & actual_price): Stripped the currency symbol (₹) and removed commas before converting values to floating-point numbers.

Discounts (discount_percentage): Removed the % sign and converted values to floats.

Ratings (rating): Removed non-numeric placeholder values (such as "|") and coerced valid entries to float values.

Review Counts (rating_count): Stripped commas and filled missing values appropriately before casting to numeric types.

🤖 AI-Use Log
Tool Used	Prompt / Task	Action Taken & Rationale
GitHub Copilot / opencode	"Write a Python function to clean currency columns with ₹ symbols and commas."	Kept & Modified: Accepted the regex stripping logic, but explicitly added error coercing (errors='coerce') to safely drop unexpected non-numeric placeholders.
AI Assistant	"Generate layout structure for a Streamlit app with top key metrics and Plotly charts."	Kept: Used the st.metric card structure and Plotly bar/scatter chart generation.
AI Assistant	"Fix Streamlit deprecation warning for use_container_width."	Kept: Replaced use_container_width=True with width="stretch" to clean terminal logs.

