import json
import os
import joblib
import pandas as pd

model = None
features = None

def init():
    global model, features
    model_dir = os.environ.get("AZUREML_MODEL_DIR", ".")
    model_path = os.path.join(model_dir, "model.pkl")
    features_path = os.path.join(model_dir, "features.json")

    model = joblib.load(model_path)

    with open(features_path, "r", encoding="utf-8") as f:
        features = json.load(f)

def run(raw_data):
    data = raw_data
    if isinstance(raw_data, (str, bytes)):
        data = json.loads(raw_data)

    # očekujemo: {"data": {"CO(GT)": 2.6, "NOx(GT)": 166, ...}}
    row = data["data"]
    X = pd.DataFrame([[row.get(c) for c in features]], columns=features)
    pred = model.predict(X)[0]
    return {"prediction": str(pred)}
