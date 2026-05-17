import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from olist_ecommerce.modeling.predict import predict_segment
import joblib
from olist_ecommerce.config import MODELS_DIR

# -------------------------------
# Page Config (Must be the very first Streamlit command)
# -------------------------------
st.set_page_config(
    page_title="📊 Sales Forecasting DSS",
    layout="wide"
)

st.title("📊 Olist Sales Forecasting System")
st.markdown("### Predict Future Sales with Probability Insights")

# -------------------------------
# Load model artifacts (Switched to cache_resource for model/pickled artifacts)
# -------------------------------
@st.cache_resource
def load_model_data():
    # Constructing path cleanly using pathlib
    model_path = MODELS_DIR / "xgb_model.pkl"
    artifacts = joblib.load(model_path)
    return artifacts["data"]

df = load_model_data()

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

    with st.spinner("Calculating forecast..."):
        result = predict_segment(
            category=selected_category,
            state=selected_state,
            weeks=weeks
        )

    if result is not None and not result.empty:

        # -------------------------------
        # Display Metrics
        # -------------------------------
        st.subheader("📌 Forecast Summary")

        col1, col2, col3 = st.columns(3)
        
        # Added commas for better currency/number formatting
        col1.metric("Avg Sales", f"{round(result['predicted_sales'].mean(), 2):,}")
        col2.metric("Max Sales", f"{round(result['predicted_sales'].max(), 2):,}")
        col3.metric("Min Sales", f"{round(result['predicted_sales'].min(), 2):,}")

        # -------------------------------
        # Table
        # -------------------------------
        st.subheader("📋 Forecast Table")
        st.dataframe(result, use_container_width=True)

        # -------------------------------
        # Chart
        # -------------------------------
        st.subheader("📈 Sales Forecast Trend")

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(result['date'], result['predicted_sales'], marker='o', color='#1f77b4')
        ax.set_title("Future Sales Prediction")
        ax.set_xlabel("Date")
        ax.set_ylabel("Sales")
        plt.xticks(rotation=45)
        st.pyplot(fig)
        plt.close(fig)  # Clear memory/prevent cross-user thread bleeding

        # -------------------------------
        # Probability Visualization
        # -------------------------------
        st.subheader("⚠️ Demand Risk (Poisson Insight)")

        fig2, ax2 = plt.subplots(figsize=(10, 4))
        ax2.plot(result['date'], result['increase_prob (%)'], label='Increase %', color='#2ca02c')
        ax2.plot(result['date'], result['decrease_prob (%)'], label='Decrease %', color='#d62728')
        ax2.legend()
        ax2.set_title("Sales Increase / Decrease Probability")
        plt.xticks(rotation=45)
        st.pyplot(fig2)
        plt.close(fig2)  # Clear memory

    else:
        st.error("No data available for this selection. Try adjusting your filters.")

# -------------------------------
# Footer
# -------------------------------
st.markdown("---")
st.markdown("Built with ❤️ using Machine Learning + Time Series + DSS")