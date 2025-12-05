import asyncio
import json
import random
import uuid
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import socketio
import pandas as pd
from prediction_engine import engine
from data.atm_locations import ATM_LOCATIONS

# App Setup
app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global State
SIMULATION_RUNNING = False
DATA_PATH = 'backend/data/historical_data.csv'

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "Kavach 2.0 Backend Running"}

@app.get("/api/atms")
def get_atms():
    return ATM_LOCATIONS

@app.get("/api/stats")
def get_stats():
    return {
        "active_monitoring": True,
        "cities_covered": 7,
        "atms_protected": len(ATM_LOCATIONS),
        "system_status": "OPERATIONAL"
    }

# --- Socket.IO Events ---

@sio.event
async def connect(sid, environ):
    print(f"Client connected: {sid}")
    await sio.emit('system_status', {'status': 'connected'}, room=sid)

@sio.event
async def start_simulation(sid):
    global SIMULATION_RUNNING
    if not SIMULATION_RUNNING:
        SIMULATION_RUNNING = True
        print("Starting simulation...")
        asyncio.create_task(run_simulation())
        await sio.emit('sim_status', {'running': True})

@sio.event
async def stop_simulation(sid):
    global SIMULATION_RUNNING
    SIMULATION_RUNNING = False
    print("Stopping simulation...")
    await sio.emit('sim_status', {'running': False})

# --- Simulation Logic ---

async def run_simulation():
    """
    Continuous loop that generates transactions and processes them.
    In a real system, this would ingest from a message queue (Kafka).
    """
    print("Simulation loop started.")
    
    # Load some historical data to replay or sample from
    try:
        df_history = pd.read_csv(DATA_PATH)
        sample_pool = df_history.to_dict('records')
    except:
        print("No historical data found, generating synthetic on the fly.")
        sample_pool = []

    while SIMULATION_RUNNING:
        # Create a transaction (Hybrid: Replay or Random)
        if sample_pool and random.random() < 0.7:
            base_txn = random.choice(sample_pool)
            # Jitter
            txn = base_txn.copy()
            txn['txn_id'] = str(uuid.uuid4())
            txn['timestamp'] = datetime.now().isoformat()
            txn['amount'] = float(txn['amount']) * random.uniform(0.9, 1.1)
        else:
            # Generate fresh
            city_idx = random.randint(0, len(ATM_LOCATIONS)-1)
            city_center = ATM_LOCATIONS[city_idx] # Just use ATM loc as anchor
            txn = {
                'txn_id': str(uuid.uuid4()),
                'amount': random.uniform(100, 50000),
                'lat': city_center['lat'] + random.uniform(-0.05, 0.05),
                'lng': city_center['lng'] + random.uniform(-0.05, 0.05),
                'city': city_center['city'],
                'timestamp': datetime.now().isoformat(),
                'sender_id': f"User_{random.randint(1000,9999)}"
            }

        # Predict Fraud
        fraud_prob = engine.predict_fraud(txn)
        is_fraud = fraud_prob > 0.7
        
        # Enrich txn for frontend
        txn['fraud_probability'] = round(fraud_prob, 2)
        txn['is_fraud'] = is_fraud
        
        # Emit Transaction
        await sio.emit('new_transaction', txn)
        
        # If Fraud => Predict Withdrawal & Emit Alert
        if is_fraud:
            predictions = engine.predict_withdrawal_locations(txn)
            
            alert_data = {
                'id': str(uuid.uuid4()),
                'transaction': txn,
                'predicted_atms': predictions,
                'timestamp': datetime.now().isoformat(),
                'severity': 'HIGH' if fraud_prob > 0.9 else 'MEDIUM'
            }
            
            print(f"!!! FRAUD DETECTED !!! Predicting withdrawal at: {[p['location'] for p in predictions]}")
            await sio.emit('new_alert', alert_data)
            
        # Sleep to control rate
        await asyncio.sleep(random.uniform(0.5, 2.0))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)