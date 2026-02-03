from flask import Flask, request, jsonify, render_template
import joblib
import pandas as pd

app = Flask(__name__)

MODEL_PATH = "model.pkl"
model = joblib.load(MODEL_PATH)


FEATURES = [
    "CO(GT)",
    "PT08.S1(CO)",
    "NMHC(GT)",
    "C6H6(GT)",
    "PT08.S2(NMHC)",
    "NOx(GT)",
    "PT08.S3(NOx)",
    "PT08.S4(NO2)",
    "PT08.S5(O3)",
    "T",
    "RH",
    "AH"
]

def to_float(value, name):
    try:
        return float(value)
    except Exception:
        raise ValueError(f"Feature '{name}' must be a number, got: {value}")

def predict_one(features_dict):
   
    row = {f: to_float(features_dict.get(f), f) for f in FEATURES}
    df = pd.DataFrame([row])

    y = model.predict(df)[0]

    return y

@app.get("/")
def index():
    return render_template("index.html", features=FEATURES)

@app.post("/predict")
def predict_form():

    try:
        y = predict_one(request.form)
        return render_template("index.html", features=FEATURES, prediction=y)
    except Exception as e:
        return render_template("index.html", features=FEATURES, error=str(e)), 400

@app.post("/api/predict")
def predict_api():
    payload = request.get_json(force=True, silent=False)
    x = payload.get("data", payload)

    try:
        y = predict_one(x)
        return jsonify({"prediction": str(y)})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    if not FEATURES:
        print("WARNING: FEATURES list is empty. Fill FEATURES in app.py with your columns.")
    app.run(host="127.0.0.1", port=5000, debug=True)
