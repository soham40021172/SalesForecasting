import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import joblib

from olist_ecommerce.modeling.predict import predict_segment
from olist_ecommerce.config import MODELS_DIR

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="📊 Sales Forecasting DSS",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------
st.title("📊 Olist Sales Forecasting System")
st.markdown("### Predict Future Sales with Probability Insights")

# ---------------------------------------------------
# LOAD MODEL ARTIFACTS
# ---------------------------------------------------
@st.cache_resource
def load_model_data():
    model_path = MODELS_DIR / "xgb_model.pkl"

    artifacts = joblib.load(model_path)

    return artifacts["data"]


df = load_model_data()

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
st.sidebar.header("🔍 Select Parameters")

categories = sorted(df["category"].unique())
states = sorted(df["state"].unique())

selected_category = st.sidebar.selectbox(
    "Category",
    categories
)

selected_state = st.sidebar.selectbox(
    "State",
    states
)

weeks = st.sidebar.slider(
    "Forecast Weeks",
    min_value=1,
    max_value=12,
    value=6
)

# ---------------------------------------------------
# RUN FORECAST
# ---------------------------------------------------
if st.sidebar.button("🚀 Run Forecast"):

    with st.spinner("Calculating forecast..."):

        result = predict_segment(
            category=selected_category,
            state=selected_state,
            weeks=weeks
        )

    # ---------------------------------------------------
    # RESULT VALIDATION
    # ---------------------------------------------------
    if result is not None and not result.empty:

        # ---------------------------------------------------
        # METRICS
        # ---------------------------------------------------
        st.subheader("📌 Forecast Summary")

        col1, col2, col3 = st.columns(3)

        avg_sales = round(result["predicted_sales"].mean(), 2)
        max_sales = round(result["predicted_sales"].max(), 2)
        min_sales = round(result["predicted_sales"].min(), 2)

        col1.metric("Avg Sales", f"{avg_sales:,}")
        col2.metric("Max Sales", f"{max_sales:,}")
        col3.metric("Min Sales", f"{min_sales:,}")

        # ---------------------------------------------------
        # TABLE
        # ---------------------------------------------------
        st.subheader("📋 Forecast Table")

        st.dataframe(
            result,
            use_container_width=True
        )

        # ---------------------------------------------------
        # SALES TREND CHART
        # ---------------------------------------------------
        st.subheader("📈 Sales Forecast Trend")

        fig, ax = plt.subplots(figsize=(10, 4))

        ax.plot(
            result["date"],
            result["predicted_sales"],
            marker="o"
        )

        ax.set_title("Future Sales Prediction")
        ax.set_xlabel("Date")
        ax.set_ylabel("Sales")

        plt.xticks(rotation=45)

        st.pyplot(fig)

        plt.close(fig)

        # ---------------------------------------------------
        # PROBABILITY CHART
        # ---------------------------------------------------
        st.subheader("⚠️ Demand Risk (Poisson Insight)")

        fig2, ax2 = plt.subplots(figsize=(10, 4))

        ax2.plot(
            result["date"],
            result["increase_prob (%)"],
            label="Increase Probability"
        )

        ax2.plot(
            result["date"],
            result["decrease_prob (%)"],
            label="Decrease Probability"
        )

        ax2.legend()

        ax2.set_title("Sales Increase / Decrease Probability")

        plt.xticks(rotation=45)

        st.pyplot(fig2)

        plt.close(fig2)

    else:
        st.error(
            "No data available for this selection. "
            "Try adjusting your filters."
        )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("---")
st.markdown(
    "Built with ❤️ using Machine Learning + Time Series Forecasting"
)