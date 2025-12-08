import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.cluster import DBSCAN
import joblib
import os

# Constants
from pathlib import Path

# Constants
BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / 'data' / 'historical_data_enriched.csv'
MODEL_DIR = BASE_DIR / 'models'
MODEL_PATH = os.path.join(MODEL_DIR, 'fraud_model.pkl')
COLUMNS_PATH = os.path.join(MODEL_DIR, 'model_columns.pkl')

def load_data(path):
    print(f"Loading data from {path}...")
    df = pd.read_csv(path)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

def feature_engineering(df):
    print("Starting feature engineering...")
    
    # 1. Hour of Day
    df['hour_of_day'] = df['timestamp'].dt.hour
    
    # 2. Log Amount
    df['amount_log'] = np.log1p(df['amount'])
    
    # 3. Velocity (Transactions in last 1 hour per sender)
    print("Calculating velocity...")
    df = df.sort_values('timestamp')
    # Group by sender_id and use rolling window on timestamp
    # We need to set timestamp as index for rolling
    df_indexed = df.set_index('timestamp')
    # 1h window, count transactions. 
    # We use 'txn_id' to count. 
    # closed='both' includes endpoints, but rolling count usually includes current row.
    velocity = df_indexed.groupby('sender_id')['txn_id'].rolling('1h').count().reset_index()
    # Rename column
    velocity = velocity.rename(columns={'txn_id': 'velocity_1h'})
    
    # Merge back to original df. 
    # Note: rolling returns timestamp as well, so we merge on sender_id and timestamp.
    # However, duplicates in timestamp for same sender might cause issues if not handled carefully.
    # Let's ensure we merge correctly.
    df = pd.merge(df, velocity, on=['sender_id', 'timestamp'], how='left')
    
    # 4. Geo Clustering (DBSCAN)
    print("Clustering locations...")
    # DBSCAN expects radians for haversine metric
    coords = np.radians(df[['lat', 'lng']])
    
    # Epsilon: 0.5 km radius (approx). Earth radius ~6371 km.
    # 0.5 / 6371 ~= 0.000078 radians
    kms_per_radian = 6371.0088
    epsilon = 0.5 / kms_per_radian
    
    db = DBSCAN(eps=epsilon, min_samples=3, metric='haversine', algorithm='ball_tree')
    df['geo_cluster_id'] = db.fit_predict(coords)
    
    # Treat noise (-1) as 0, and shift others to avoid negative inputs if model dislikes them (though RF handles it)
    # Let's just map -1 to 0 and others to cluster_id + 1 to keep it clean positive integers
    df['geo_cluster_id'] = df['geo_cluster_id'].apply(lambda x: 0 if x == -1 else x + 1)
    
    print("Feature engineering complete.")
    return df

def train_model(df):
    print("Preparing data for training...")
    
    # Select features
    features = ['amount', 'amount_log', 'hour_of_day', 'velocity_1h', 'geo_cluster_id', 'lat', 'lng']
    target = 'is_fraud'
    
    X = df[features]
    y = df[target]
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    
    print(f"Training RandomForestClassifier with {len(X_train)} samples...")
    clf = RandomForestClassifier(n_estimators=200, max_depth=15, random_state=42, n_jobs=-1)
    clf.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = clf.predict(X_test)
    
    print("\nConfusion Matrix:")
    print(confusion_matrix(y_test, y_pred))
    
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred))
    
    return clf, features

def save_model(clf, features):
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(clf, MODEL_PATH)
    
    print(f"Saving column names to {COLUMNS_PATH}...")
    joblib.dump(features, COLUMNS_PATH)
    
    print("Serialization complete.")

if __name__ == "__main__":
    if not os.path.exists(DATA_PATH):
        print(f"Error: Data file not found at {DATA_PATH}. Please run Task 1 first.")
        exit(1)
        
    df = load_data(DATA_PATH)
    df = feature_engineering(df)
    model, features = train_model(df)
    save_model(model, features)
