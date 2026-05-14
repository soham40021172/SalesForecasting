import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from olist_ecommerce.modeling.predict import predict_segment
import joblib
from olist_ecommerce.config import MODELS_DIR

# -------------------------------
# Page Config
# -------------------------------
st.set_page_config(
    page_title="📊 Sales Forecasting DSS",
    layout="wide"
)

st.title("📊 Olist Sales Forecasting System")
st.markdown("### Predict Future Sales with Probability Insights")

# -------------------------------
# Load model artifacts
# -------------------------------
@st.cache_data
def load_data():
    artifacts = joblib.load(MODELS_DIR / "xgb_model.pkl")
    return artifacts["data"]

df = load_data()

# -------------------------------
# Sidebar Filters
# -------------------------------
st.sidebar.header("🔍 Select Parameters")

categories = sorted(df['category'].unique())
states = sorted(df['state'].unique())

selected_category = st.sidebar.selectbox("Category", categories)
selected_state = st.sidebar.selectbox("State", states)
weeks = st.sidebar.slider("Forecast Weeks", 1, 12, 6)

# -------------------------------
# Run Prediction
# -------------------------------
if st.sidebar.button("🚀 Run Forecast"):

    result = predict_segment(
        category=selected_category,
        state=selected_state,
        weeks=weeks
    )

    if result is not None:

        # -------------------------------
        # Display Metrics
        # -------------------------------
        st.subheader("📌 Forecast Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Avg Sales", round(result['predicted_sales'].mean(), 2))
        col2.metric("Max Sales", round(result['predicted_sales'].max(), 2))
        col3.metric("Min Sales", round(result['predicted_sales'].min(), 2))

        # -------------------------------
        # Table
        # -------------------------------
        st.subheader("📋 Forecast Table")
        st.dataframe(result)

        # -------------------------------
        # Chart
        # -------------------------------
        st.subheader("📈 Sales Forecast Trend")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(result['date'], result['predicted_sales'], marker='o')
        ax.set_title("Future Sales Prediction")
        ax.set_xlabel("Date")
        ax.set_ylabel("Sales")
        plt.xticks(rotation=45)

        st.pyplot(fig)

        # -------------------------------
        # Probability Visualization
        # -------------------------------
        st.subheader("⚠️ Demand Risk (Poisson Insight)")

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(result['date'], result['increase_prob (%)'], label='Increase %')
        ax2.plot(result['date'], result['decrease_prob (%)'], label='Decrease %')
        ax2.legend()
        ax2.set_title("Sales Increase / Decrease Probability")

        st.pyplot(fig2)

    else:
        st.error("No data available for this selection")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Machine Learning + Time Series + DSS")