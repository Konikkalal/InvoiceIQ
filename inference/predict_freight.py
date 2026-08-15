import joblib
import pandas as pd
from pathlib import Path


# =========================================================
# Model Path
# =========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "freight_cost_prediction"
    / "models"
    / "predict_freight_model.pkl"
)


# =========================================================
# Load Model
# =========================================================

model = joblib.load(MODEL_PATH)


# =========================================================
# Prediction Function
# =========================================================

def predict_freight_cost(input_data):

    input_df = pd.DataFrame(input_data)

    # Keep exactly the features used during training
    input_df = input_df[
        ["Quantity", "Dollars"]
    ]

    prediction = model.predict(
        input_df
    ).round()

    input_df["Predicted_Freight"] = prediction

    return input_df