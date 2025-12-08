import pandas as pd
import numpy as np
import joblib
import os
from math import radians, sin, cos, sqrt, atan2
from backend.data.atm_locations import ATM_LOCATIONS

from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / 'backend' / 'models' / 'fraud_model.pkl'
COLUMNS_PATH = BASE_DIR / 'backend' / 'models' / 'model_columns.pkl'

class PredictionEngine:
    def __init__(self):
        self.model = None
        self.model_columns = None
        self.load_model()
        
    def load_model(self):
        try:
            if os.path.exists(MODEL_PATH):
                self.model = joblib.load(MODEL_PATH)
                print(f"Model loaded from {MODEL_PATH}")
            else:
                print("Warning: Model not found. Predictions will be simulated.")
                
            if os.path.exists(COLUMNS_PATH):
                self.model_columns = joblib.load(COLUMNS_PATH)
            else:
                self.model_columns = ['amount', 'amount_log', 'hour_of_day', 'velocity_1h', 'geo_cluster_id', 'lat', 'lng']
        except Exception as e:
            print(f"Error loading model: {e}")

    def haversine_distance(self, lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        return R * c

    def predict_fraud(self, transaction):
        """
        Predict probability of fraud for a single transaction.
        transaction: dict
        """
        # If model exists, prepare features
        if self.model:
            try:
                # Create DataFrame for single row
                df = pd.DataFrame([transaction])
                
                # Feature Engineering (Lite version for real-time)
                df['amount_log'] = np.log1p(df['amount'])
                df['timestamp'] = pd.to_datetime(df['timestamp'])
                df['hour_of_day'] = df['timestamp'].dt.hour
                
                # These require history, so we might estimate or accept them as input
                if 'velocity_1h' not in df.columns:
                    df['velocity_1h'] = transaction.get('velocity_1h', 1) # Default to 1
                if 'geo_cluster_id' not in df.columns:
                    df['geo_cluster_id'] = transaction.get('geo_cluster_id', 0)
                    
                # Ensure columns match training
                X = df[self.model_columns]
                
                # Predict probability
                prob = self.model.predict_proba(X)[0][1] # Probability of class 1 (Fraud)
                return float(prob)
            except Exception as e:
                print(f"Prediction error: {e}. Fallback to rule-based.")
        
        # Fallback Rule-Based (if model fails or missing)
        score = 0
        if transaction['amount'] > 20000: score += 0.4
        if transaction.get('velocity_1h', 0) > 5: score += 0.4
        return min(score, 0.99)

    def predict_withdrawal_locations(self, transaction, top_k=3):
        """
        Predict where the money will be withdrawn.
        Returns list of ATM dicts with 'probability'.
        """
        tx_lat = transaction['lat']
        tx_lng = transaction['lng']
        city = transaction.get('city')
        
        # Filter ATMs by city if available, else use all
        candidates = [atm for atm in ATM_LOCATIONS if city is None or atm['city'] == city]
        if not candidates:
            candidates = ATM_LOCATIONS
            
        # Calculate distances
        scored_atms = []
        for atm in candidates:
            dist = self.haversine_distance(tx_lat, tx_lng, atm['lat'], atm['lng'])
            # Probability is inversely proportional to distance
            # Simple heuristic: prob = 1 / (dist + 1)
            prob_score = 100 / (dist + 0.5)
            scored_atms.append({
                **atm,
                'distance': round(dist, 2),
                'score': prob_score
            })
            
        # Sort by score descending
        scored_atms.sort(key=lambda x: x['score'], reverse=True)
        top_atms = scored_atms[:top_k]
        
        # Normalize probabilities to sum to ~0.9 (uncertainty factor)
        total_score = sum(a['score'] for a in top_atms)
        results = []
        for atm in top_atms:
            p = (atm['score'] / total_score) * 0.90 # 90% confidence distributed among top 3
            results.append({
                'id': atm['id'],
                'location': atm['location'],
                'lat': atm['lat'],
                'lng': atm['lng'],
                'probability': round(p, 2),
                'estimated_time': f"{np.random.randint(15, 60)} mins" # Simulated ETA
            })
            
        return results

# Singleton instance
engine = PredictionEngine()