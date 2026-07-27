import os
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Amazon Sales Analytics Dashboard", page_icon="🛒", layout="wide"
)


# --- DATA LOADING & CLEANING ---
@st.cache_data
def load_and_clean_data(file_path="data/raw/amazon.csv"):
  if not os.path.exists(file_path):
    st.error(f"Dataset not found at `{file_path}`. Please upload or add it.")
    return pd.DataFrame()

  df = pd.read_csv(file_path)

  # 1. Clean Price Columns (remove currency symbol ₹ and commas)
  for col in ["discounted_price", "actual_price"]:
    if col in df.columns:
      df[col] = (
          df[col]
          .astype(str)
          .str.replace("₹", "", regex=False)
          .str.replace(",", "", regex=False)
      )
      df[col] = pd.to_numeric(df[col], errors="coerce")

  # 2. Clean Discount Percentage (remove % symbol)
  if "discount_percentage" in df.columns:
    df["discount_percentage"] = (
        df["discount_percentage"].astype(str).str.replace("%", "", regex=False)
    )
    df["discount_percentage"] = pd.to_numeric(
        df["discount_percentage"], errors="coerce"
    )

  # 3. Clean Rating
  if "rating" in df.columns:
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")

  # 4. Clean Rating Count (remove commas)
  if "rating_count" in df.columns:
    df["rating_count"] = (
        df["rating_count"].astype(str).str.replace(",", "", regex=False)
    )
    df["rating_count"] = pd.to_numeric(df["rating_count"], errors="coerce")

  # 5. Extract Main Category
  if "category" in df.columns:
    df["main_category"] = (
        df["category"]
        .astype(str)
        .apply(lambda x: x.split("|")[0] if "|" in x else x)
    )

  return df.dropna(subset=["discounted_price", "actual_price", "rating"]).copy()


# Load data
df = load_and_clean_data()

# --- HEADER SECTION ---
st.title("🛒 Amazon Sales & Product Analytics Dashboard")
st.markdown(
    "An interactive dashboard exploring prices, discounts, ratings, and"
    " category performance across top-listed Amazon products."
)

if df.empty:
  st.warning(
      "Please ensure `data/raw/amazon.csv` is present to view dashboard"
      " analytics."
  )
  st.stop()

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Data")
categories = ["All"] + sorted(list(df["main_category"].dropna().unique()))
selected_category = st.sidebar.selectbox("Select Main Category", categories)

min_rating = st.sidebar.slider("Minimum Rating Stars", 1.0, 5.0, 3.0, step=0.1)

filtered_df = df.copy()
if selected_category != "All":
  filtered_df = filtered_df[filtered_df["main_category"] == selected_category]
filtered_df = filtered_df[filtered_df["rating"] >= min_rating]

# --- PREVIEW ---
with st.expander("🔍 Preview Cleaned Dataset", expanded=False):
  st.write(
      f"Showing **{len(filtered_df)}** filtered products out of **{len(df)}**"
      " total entries."
  )
  st.dataframe(filtered_df.head(10), use_container_width=True)

st.divider()

# --- SUMMARY METRICS ---
st.subheader("📌 Key Summary Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
  st.metric(label="Total Products Filtered", value=f"{len(filtered_df):,}")
with col2:
  avg_disc_price = (
      filtered_df["discounted_price"].mean() if len(filtered_df) > 0 else 0
  )
  st.metric(label="Avg Discounted Price", value=f"{avg_disc_price:,.2f}")
with col3:
  avg_discount = (
      filtered_df["discount_percentage"].mean() if len(filtered_df) > 0 else 0
  )
  st.metric(label="Avg Discount Rate", value=f"{avg_discount:.1f}%")
with col4:
  avg_rating = filtered_df["rating"].mean() if len(filtered_df) > 0 else 0
  st.metric(label="Avg Customer Rating", value=f"⭐ {avg_rating:.2f} / 5.0")

st.divider()

# --- CHARTS ---
st.subheader("1. Category Distribution")
cat_counts = (
    filtered_df["main_category"]
    .value_counts()
    .reset_index(name="product_count")
)
fig1 = px.bar(
    cat_counts,
    x="main_category",
    y="product_count",
    labels={
        "main_category": "Main Category",
        "product_count": "Number of Products",
    },
    title="Number of Products per Main Category",
    color="product_count",
    color_continuous_scale="Viridis",
)
st.plotly_chart(fig1, use_container_width=True)

st.info(
    "**Written Takeaway:** Electronics and Computers & Accessories dominate"
    " the dataset, accounting for the vast majority of top-listed product"
    " entries. Categories like Office Products and Home & Kitchen represent"
    " smaller product counts, indicating that tech-related items drive"
    " marketplace volume."
)

st.divider()

st.subheader("2. Pricing Structure Comparison")
fig2 = px.scatter(
    filtered_df,
    x="actual_price",
    y="discounted_price",
    color="main_category",
    hover_data=["discount_percentage", "rating"],
    labels={
        "actual_price": "Actual Retail Price (₹)",
        "discounted_price": "Discounted Price (₹)",
    },
    title="Actual Price vs. Discounted Price Relationship",
)
st.plotly_chart(fig2, use_container_width=True)

st.info(
    "**Written Takeaway:** There is a strong positive linear correlation"
    " between retail prices and discounted prices, though high-priced products"
    " display wider variance. Most product offerings cluster under ₹10,000,"
    " demonstrating that steep promotional discounts are consistently applied"
    " across lower-to-mid tier items."
)

st.divider()

st.subheader("3. Discount Rate vs. Customer Rating")
fig3 = px.box(
    filtered_df,
    x="rating",
    y="discount_percentage",
    labels={
        "rating": "Customer Rating (Stars)",
        "discount_percentage": "Discount Percentage (%)",
    },
    title="Discount Percentage Distribution Across Star Ratings",
    color_discrete_sequence=["#FF9900"],
)
st.plotly_chart(fig3, use_container_width=True)

st.info(
    "**Written Takeaway:** Discount percentages remain evenly distributed across"
    " product rating tiers, typically averaging between 40% and 60%. This"
    " reveals that heavy discounting does not harm customer satisfaction"
    " ratings, nor are high ratings restricted strictly to full-price premium"
    " goods."
)