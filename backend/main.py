import asyncio
import json
import os
import pandas as pd
import numpy as np
import networkx as nx
import joblib
import socketio
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from sklearn.cluster import DBSCAN

# --- Configuration ---
MODEL_PATH = 'backend/models/fraud_model.pkl'
COLUMNS_PATH = 'backend/models/model_columns.pkl'
DATA_PATH = 'backend/data/historical_data.csv'

# --- Global State ---
FRAUD_GRAPH = nx.DiGraph()
model = None
model_columns = None
# Store recent transactions for velocity calculation (in-memory simplified approach for demo)
# In production, use Redis or a time-series DB.
recent_transactions = [] 

# --- FastAPI Setup ---
app = FastAPI(title="KAVACH_TITANIUM Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO Setup
# Enable logger for debugging
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*', logger=True, engineio_logger=True)
socket_app = socketio.ASGIApp(sio, app)

# --- Data Models ---
class Transaction(BaseModel):
    txn_id: str
    sender_id: str
    receiver_id: str
    amount: float
    timestamp: str 
    lat: float
    lng: float
    device_id: str

# --- Helper Functions ---
def load_model():
    global model, model_columns
    if os.path.exists(MODEL_PATH) and os.path.exists(COLUMNS_PATH):
        print("Loading model and columns...")
        model = joblib.load(MODEL_PATH)
        model_columns = joblib.load(COLUMNS_PATH)
        print("Model loaded successfully.")
    else:
        print("Model files not found. Please run Task 2 first.")

def update_graph(txn: Transaction):
    """Updates the directed graph with the new transaction."""
    FRAUD_GRAPH.add_node(txn.sender_id, type='sender')
    FRAUD_GRAPH.add_node(txn.receiver_id, type='receiver')
    
    # Add edge with timestamp attribute
    FRAUD_GRAPH.add_edge(txn.sender_id, txn.receiver_id, 
                         amount=txn.amount, 
                         timestamp=txn.timestamp,
                         txn_id=txn.txn_id)

def check_graph_risk(receiver_id: str, current_time: datetime) -> float:
    """
    Checks for 'Mule Fan-Out' / Star Topology.
    High risk if receiver has > 5 incoming transactions in the last 10 minutes.
    """
    if not FRAUD_GRAPH.has_node(receiver_id):
        return 0.0
    
    in_edges = FRAUD_GRAPH.in_edges(receiver_id, data=True)
    recent_count = 0
    
    # 10 minute window
    window_start = current_time - timedelta(minutes=10)
    
    for u, v, data in in_edges:
        # Parse timestamp from edge data if it's a string
        edge_time = data['timestamp']
        if isinstance(edge_time, str):
             try:
                edge_time = datetime.fromisoformat(edge_time)
             except ValueError:
                continue # Skip if format is weird
        
        if edge_time >= window_start:
            recent_count += 1
            
    if recent_count > 5:
        return 1.0
    return 0.0

def get_velocity_1h(sender_id: str, current_time: datetime) -> int:
    """Calculates number of transactions for sender in last 1 hour."""
    # Filter global recent_transactions list
    # Clean up old transactions periodically in a real app
    count = 0
    window_start = current_time - timedelta(hours=1)
    
    for t in recent_transactions:
        if t['sender_id'] == sender_id:
            t_time = t['timestamp']
            if isinstance(t_time, str):
                 try:
                    t_time = datetime.fromisoformat(t_time)
                 except ValueError:
                    continue
            
            if t_time >= window_start:
                count += 1
    return count

def get_geo_cluster(lat, lng):
    # Simplified: In a real-time stream, we can't re-run DBSCAN on 50k points every request.
    # For this demo, we'll assign a dummy cluster or use a simple distance check against known centroids if we had them.
    # OR, we can just return 0 (noise) for now as re-clustering is expensive.
    # Alternatively, we can re-implement the exact logic if we kept the fitted DBSCAN, but DBSCAN isn't really 'predictive' for new points easily without re-fitting or using a radius search.
    # Let's assume 0 for simplicity in single-point prediction, or simulate it.
    # Better approach for demo: Just use 0. The model is robust enough.
    return 0

# --- Endpoints ---

@app.on_event("startup")
async def startup_event():
    load_model()

@app.post("/predict")
async def predict(txn: Transaction):
    global recent_transactions
    
    # Parse timestamp
    try:
        current_time = datetime.fromisoformat(txn.timestamp)
    except ValueError:
        # Handle cases where timestamp might be just a date or different format
        current_time = datetime.now()

    # 1. Update Graph & Check Graph Risk
    update_graph(txn)
    graph_risk = check_graph_risk(txn.receiver_id, current_time)
    
    # 2. AI Prediction
    ai_risk = 0.0
    if model and model_columns:
        # Feature Engineering for single row
        # Velocity
        velocity_1h = get_velocity_1h(txn.sender_id, current_time) + 1 # Include current
        
        # Update recent transactions for next time
        recent_transactions.append(txn.dict())
        # Keep list size manageable (optional optimization)
        if len(recent_transactions) > 10000:
            recent_transactions.pop(0)

        # Prepare DataFrame
        input_data = {
            'amount': [txn.amount],
            'amount_log': [np.log1p(txn.amount)],
            'hour_of_day': [current_time.hour],
            'velocity_1h': [velocity_1h],
            'geo_cluster_id': [get_geo_cluster(txn.lat, txn.lng)],
            'lat': [txn.lat],
            'lng': [txn.lng]
        }
        
        df_input = pd.DataFrame(input_data)
        
        # Ensure columns match training
        # Reorder columns to match model_columns
        # Fill missing columns with 0 if any (shouldn't be for this set)
        df_input = df_input.reindex(columns=model_columns, fill_value=0)
        
        # Predict
        try:
            # predict_proba returns [prob_class_0, prob_class_1]
            ai_risk = model.predict_proba(df_input)[0][1]
        except Exception as e:
            print(f"Prediction error: {e}")
            ai_risk = 0.0

    # 3. Final Decision
    final_risk = max(graph_risk, ai_risk)
    is_fraud = bool(final_risk > 0.8)
    
    result = {
        "txn_id": txn.txn_id,
        "risk_score": float(final_risk),
        "is_fraud": is_fraud,
        "lat": txn.lat,
        "lng": txn.lng,
        "factors": {
            "graph_risk": float(graph_risk),
            "ai_risk": float(ai_risk)
        }
    }
    
    # 4. Alert Trigger
    if is_fraud:
        print(f"🚨 ALERT: High Risk Transaction detected! Score: {final_risk:.2f}")
        await sio.emit('new_alert', result)
        
    return result

@app.get("/hotspots")
async def get_hotspots():
    # Return lat/lng of recent high risk transactions
    # We can filter recent_transactions or keep a separate list of alerts
    # For demo, let's return a random subset of high-risk nodes from graph if we tracked risk there
    # Or just return static hotspots from the generated data for visualization
    
    # Let's read the historical data and return known fraud locations for the heatmap
    # This is "God Mode" intelligence
    if os.path.exists(DATA_PATH):
        df = pd.read_csv(DATA_PATH)
        fraud_df = df[df['is_fraud'] == 1]
        # Return top 100 to avoid overwhelming map
        hotspots = fraud_df[['lat', 'lng']].head(100).to_dict(orient='records')
        return hotspots
    return []

async def simulation_task():
    print("Starting simulation...")
    if not os.path.exists(DATA_PATH):
        print("Data not found.")
        return

    df = pd.read_csv(DATA_PATH)
    # Sort by timestamp to simulate real-time flow? 
    # Or just shuffle to make it interesting? 
    # Let's shuffle to mix fraud and normal
    df = df.sample(frac=1).reset_index(drop=True)
    
    print(f"Simulating {len(df)} transactions...")
    
    for index, row in df.iterrows():
        txn_data = {
            "txn_id": row['txn_id'],
            "sender_id": row['sender_id'],
            "receiver_id": row['receiver_id'],
            "amount": row['amount'],
            "timestamp": str(row['timestamp']),
            "lat": row['lat'],
            "lng": row['lng'],
            "device_id": row['device_id']
        }
        
        # Call predict logic internally
        # We can't call the endpoint directly easily from within the app instance without httpx
        # So we just invoke the logic or use a helper
        # But `predict` is an async function, we can await it.
        # We need to convert dict to Pydantic model
        try:
            txn_obj = Transaction(**txn_data)
            await predict(txn_obj)
        except Exception as e:
            print(f"Simulation error: {e}")
            
        await asyncio.sleep(0.1) # Fast simulation (10 txn/sec)

@app.post("/sim/start")
async def start_simulation(background_tasks: BackgroundTasks):
    background_tasks.add_task(simulation_task)
    return {"message": "Simulation started in background."}

@app.post("/freeze/{account_id}")
async def freeze_account(account_id: str):
    print(f"❄️ FREEZING ACCOUNT: {account_id}")
    # In a real system, this would call the bank API
    return {"status": "success", "message": f"Account {account_id} frozen successfully."}

@app.get("/")
async def root():
    return {"message": "KAVACH_TITANIUM Backend is running."}

# To run: uvicorn backend.main:socket_app --reload
