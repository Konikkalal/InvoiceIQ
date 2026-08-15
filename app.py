import streamlit as st
import pandas as pd
import numpy as np

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag


# =========================================================
# Page Configuration
# =========================================================

st.set_page_config(
    page_title="InvoiceIQ",
    page_icon="📊",
    layout="wide"
)


# =========================================================
# Header
# =========================================================

st.markdown("""
# 📊 InvoiceIQ

### AI-Driven Freight Cost Prediction & Invoice Risk Flagging

This intelligent analytics platform leverages machine learning to:

- **Predict expected freight costs**
- **Detect risky or abnormal vendor invoices**
- **Support faster financial decision-making**
- **Reduce manual invoice review workload**
""")

st.divider()


# =========================================================
# Sidebar
# =========================================================

st.sidebar.title("🔍 Model Selection")

selected_model = st.sidebar.radio(
    "Choose Prediction Module",
    [
        "Freight Cost Prediction",
        "Invoice Manual Approval Flag"
    ]
)

st.sidebar.markdown("""
---

### 💼 Business Impact

- Improved cost forecasting
- Reduced invoice anomalies
- Faster finance operations
- Better financial control
""")


# =========================================================
# Freight Cost Prediction
# =========================================================

if selected_model == "Freight Cost Prediction":

    st.subheader("🚚 Freight Cost Prediction")

    st.markdown("""
    **Objective:**

    Predict freight cost for a vendor invoice using
    **Invoice Dollars** to support budgeting,
    forecasting, and vendor negotiations.
    """)

    with st.form("freight_form"):

        dollars = st.number_input(
            "Invoice Dollars",
            min_value=1.0,
            value=18500.0,
            step=100.0
        )

        submit_freight = st.form_submit_button(
            "🔮 Predict Freight Cost"
        )

    if submit_freight:

        input_data = {
            "Dollars": [dollars]
        }

        try:

            prediction_result = predict_freight_cost(
                input_data
            )

            prediction = prediction_result[
                "Predicted_Freight"
            ]

            st.success(

                "✅ Prediction completed successfully."
            )

            st.metric(
                label="Estimated Freight Cost",
                value=f"${prediction[0]:,.2f}"
            )

        except Exception as e:

            st.error(
                f"Unable to generate prediction: {e}"
            )


# =========================================================
# Invoice Flag Prediction
# =========================================================

else:

    st.subheader(
        "⚠️ Invoice Manual Approval Prediction"
    )

    st.markdown("""
    **Objective:**

    Predict whether a vendor invoice should be
    **flagged for manual approval** based on abnormal
    invoice and item cost patterns.
    """)

    with st.form("invoice_flag_form"):

        col1, col2 = st.columns(2)

        # -------------------------------------------------
        # Column 1
        # -------------------------------------------------

        with col1:

            invoice_quantity = st.number_input(
                "Invoice Quantity",
                min_value=1,
                value=50,
                step=1
            )

            invoice_dollars = st.number_input(
                "Invoice Dollars",
                min_value=1.0,
                value=352.95,
                step=10.0
            )

            freight = st.number_input(
                "Freight Cost",
                min_value=0.0,
                value=1.73,
                step=0.10
            )

        # -------------------------------------------------
        # Column 2
        # -------------------------------------------------

        with col2:

            total_item_quantity = st.number_input(
                "Total Item Quantity",
                min_value=1,
                value=162,
                step=1
            )

            total_item_dollars = st.number_input(
                "Total Item Dollars",
                min_value=1.0,
                value=2476.0,
                step=10.0
            )

        submit_flag = st.form_submit_button(
            "🔍 Evaluate Invoice Risk"
        )

    # -----------------------------------------------------
    # Prediction
    # -----------------------------------------------------

    if submit_flag:

        input_data = {
            "invoice_quantity": [
                invoice_quantity
            ],

            "invoice_dollars": [
                invoice_dollars
            ],

            "Freight": [
                freight
            ],

            "total_item_quantity": [
                total_item_quantity
            ],

            "total_item_dollars": [
                total_item_dollars
            ]
        }

        try:

            flag_result = predict_invoice_flag(
                input_data
            )

            flag_prediction = flag_result[
                "Predicted_Flag"
            ]

            is_flagged = bool(
                flag_prediction[0]
            )

            if is_flagged:

                st.error(
                    "🚨 Invoice requires **MANUAL APPROVAL**"
                )

                st.warning(
                    "The machine learning model has identified "
                    "this invoice as potentially risky."
                )

            else:

                st.success(
                    "✅ Invoice is **SAFE for Auto-Approval**"
                )

                st.info(
                    "No significant risk was detected by the model."
                )

        except Exception as e:

            st.error(
                f"Unable to evaluate invoice: {e}"
            )