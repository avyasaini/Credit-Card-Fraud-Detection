from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import pandas as pd
import bz2
import joblib
import os

app = Flask(__name__)

# 1. Load the trained pipeline

with bz2.open("models/best_fraud_detection_pipeline1.1.pkl.bz2", "rb") as f:
    pipeline = joblib.load(f)
# 2. Category options (for dropdown in index.html)
categories = [
    "entertainment", "food_dining", "gas_transport", "grocery_net", "grocery_pos",
    "health_fitness", "home", "kids_pets", "misc_net", "misc_pos",
    "personal_care", "shopping_net", "shopping_pos", "travel"
]

def generate_risk_advice(fraud_prob):
    """
    AI-driven advice generator based on the computed fraud probability.
    Can be expanded to incorporate additional business logic.
    """
    if fraud_prob > 0.8:
        return "Critical Risk: High probability of fraud. Action required immediately."
    elif fraud_prob > 0.5:
        return "Moderate Risk: Unusual activity detected. Verify user identity."
    else:
        return "Low Risk: Standard transaction behavior. No action needed."

@app.route('/')
def index():
    # Render the HTML template, passing the category list for the dropdown
    return render_template("index.html", categories=categories)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # 3. Collect data from form (if submitted via HTML) or JSON (if submitted via API)
        data = request.form if request.form else request.get_json()

        # Extract features from the data
        amt = float(data['amt'])
        city_pop = float(data['city_pop'])
        lat = float(data['lat'])
        long = float(data['long'])
        merch_lat = float(data['merch_lat'])
        merch_long = float(data['merch_long'])
        unix_time = float(data['unix_time'])
        category = data['category']

        # 4. Construct a pandas DataFrame for the model input
        tx_dataframe = pd.DataFrame([[amt, city_pop, lat, long, merch_lat, merch_long, unix_time, category]],
                                  columns=['amt', 'city_pop', 'lat', 'long', 'merch_lat', 'merch_long', 'unix_time', 'category'])

        # 5. Execute model prediction
        model_pred = pipeline.predict(tx_dataframe)[0]
        fraud_prob = pipeline.predict_proba(tx_dataframe)[0][1]

        # 6. Generate risk advice
        risk_advice = generate_risk_advice(fraud_prob)

        # 7. Send JSON response
        return jsonify({
            "prediction": "Fraud Detected" if model_pred >= 0.8 else "Legitimate",
            "probability": round(fraud_prob, 2),
            "recommendation": risk_advice
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=True)
