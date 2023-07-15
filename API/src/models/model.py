from pathlib import Path
import tensorflow as tf
import pickle
import numpy as np


BASE_DIR = Path(__file__).resolve(strict=True).parent 
MODEL_PATH = f"{BASE_DIR}/model.h5"
SCALER_PATH = f"{BASE_DIR}/scaler.pkl"

with open(SCALER_PATH, 'rb') as file:
    scaler = pickle.load(file)

class WeatherPredictor:

    def __init__(self):
        self.model = tf.keras.models.load_model(MODEL_PATH)

    def predict_next_15(self, input_array):
        tr_array = scaler.transform(input_array)
        tr_array = np.expand_dims(tr_array,axis=1)
        pred = self.model.predict(tr_array)
        return pred