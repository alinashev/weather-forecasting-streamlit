import json
import joblib

def load_model(path='model/aussie_rain.joblib'):
    return joblib.load(path)

def load_stats(path='model/train_stats.json'):
    with open(path, "r") as f:
        return json.load(f)
