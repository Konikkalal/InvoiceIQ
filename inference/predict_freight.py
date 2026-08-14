import joblib
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "predict_freight_model.pkl"
)


def load_model(model_path: str = str(MODEL_PATH)):
    """
    Load trained freight cost prediction model.
    """

    with open(model_path, "rb") as f:
        model = joblib.load(f)

    return model


def predict_freight_cost(input_data):
    """
    Predict freight cost using Invoice Dollars.
    """

    model = load_model()

    input_df = pd.DataFrame(input_data)

    # Model was trained only using Dollars
    input_df = input_df[["Dollars"]]

    prediction = model.predict(input_df).round()

    input_df["Predicted_Freight"] = prediction

    return input_df


if __name__ == "__main__":

    sample_data = {
        "Dollars": [
            18500,
            9000,
            3000,
            200
        ]
    }

    prediction = predict_freight_cost(
        sample_data
    )

    print("\nFreight Cost Prediction:")
    print(prediction)