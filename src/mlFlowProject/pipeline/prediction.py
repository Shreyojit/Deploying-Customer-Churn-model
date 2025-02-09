import joblib
import numpy as np
import pandas as pd
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

class PredictionPipeline:
    def __init__(self, preprocessor_path='prediction_utils/preprocessor.joblib', 
                 model_path='prediction_utils/model.joblib'):
        self.preprocessor_path = preprocessor_path
        self.model_path = model_path
        
        try:
            logging.info(f"Loading preprocessor from {self.preprocessor_path}")
            self.preprocessor = joblib.load(self.preprocessor_path)
            
            logging.info(f"Loading model from {self.model_path}")
            self.model = joblib.load(self.model_path)
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
            raise FileNotFoundError(f"File not found: {e}")
        except Exception as e:
            logging.error(f"Error loading model or preprocessor: {e}")
            raise RuntimeError(f"Error loading model or preprocessor: {e}")

    def predict(self, data):

        
        try:
            logging.info("Transforming input data using preprocessor")
            data = self.preprocessor.transform(data)
            
            logging.info("Making predictions using the model")
            prediction = self.model.predict(data)
            return prediction
        except Exception as e:
            logging.error(f"Error during prediction: {e}")
            raise RuntimeError(f"Error during prediction: {e}")