import asyncio
import json
import random
import uuid
import csv
import os
from datetime import datetime
from fastapi import FastAPI, BackgroundTasks, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import socketio
import pandas as pd
from pathlib import Path

# New Imports
from backend.prediction_engine import engine as prediction_engine
from backend.database import get_db, Transaction, ATM, Suspect, FraudReport
from backend.data_generator import generator

# File Paths
BASE_DIR = Path(__file__).resolve().parent.parent
COMPLAINTS_FILE = BASE_DIR / 'backend' / 'data' / 'complaints.csv'

# Ensure data dir exists
COMPLAINTS_FILE.parent.mkdir(parents=True, exist_ok=True)
if not COMPLAINTS_FILE.exists():
    with open(COMPLAINTS_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['ticket_id', 'reporter_name', 'category', 'description', 'timestamp'])

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

# --- API Endpoints ---

@app.get("/")
def read_root():
    return {"status": "Kavach Titanium Brain Running | DB Connected"}

@app.get("/api/atms")
def get_atms(db: Session = Depends(get_db)):
    # Return from DB now
    return db.query(ATM).all()

@app.get("/api/stats") # General Dashboard (God Mode)
def get_stats(db: Session = Depends(get_db)):
    total_txns = db.query(Transaction).count()
    fraud_txns = db.query(Transaction).filter(Transaction.is_fraud == True).count()
    return {
        "active_monitoring": True,
        "atms_protected": db.query(ATM).count(),
        "total_transactions": total_txns,
        "threats_stopped": fraud_txns,
        "system_status": "TITANIUM_SHIELD_ACTIVE"
    }

# --- PORTAL APIs (New) ---

@app.get("/api/lea/stats") # Police Dashboard
def get_lea_stats(db: Session = Depends(get_db)):
    # Calculate interception metrics
    recent_frauds = db.query(Transaction).filter(Transaction.is_fraud == True).order_by(Transaction.timestamp.desc()).limit(10).all()
    return {
        "active_operations": 3,
        "suspects_tracked": db.query(Suspect).count(),
        "recent_alerts": recent_frauds
    }

@app.get("/api/bank/stats") # Bank Dashboard
def get_bank_stats(db: Session = Depends(get_db)):
    # Financial metrics
    frauds = db.query(Transaction).filter(Transaction.is_fraud == True).all()
    saved = sum([f.amount for f in frauds if f.status == "DECLINED_FRAUD"])
    return {
        "total_saved_inr": saved,
        "blocked_cards": len(frauds),
        "false_positive_rate": "0.4%"
    }

@app.post("/api/portal/submit") # User Grievance
def submit_report(report: dict, db: Session = Depends(get_db)):
    # Save user query to DB
    new_report = FraudReport(
        reporter_name=report.get('name', 'Anonymous'),
        description=report.get('desc'),
        fraud_category=report.get('category'),
        status="OPEN"
    )
    db.add(new_report)
    db.commit()
    
    # Save to Live CSV
    try:
        with open(COMPLAINTS_FILE, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                new_report.report_id,
                new_report.reporter_name,
                new_report.fraud_category,
                new_report.description,
                new_report.timestamp.isoformat()
            ])
    except Exception as e:
        print(f"CSV Logging Error: {e}")

    return {"status": "received", "ticket_id": new_report.report_id}

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
        print("Starting SMART simulation...")
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
    print("Simulation loop started (DB Mode).")
    
    while SIMULATION_RUNNING:
        # Use simple try-except to prevent crash loops
        try:
            # Generate SMART transaction via Generator
            txn_dict = generator.generate_smart_transaction()
            
            # Emit Transaction
            await sio.emit('new_transaction', txn_dict)
            
            # If Fraud => Predict Withdrawal & Emit Alert
            if txn_dict['is_fraud']:
                # Use engine to predict NEXT location
                predictions = prediction_engine.predict_withdrawal_locations(txn_dict)
                
                alert_data = {
                    'id': str(uuid.uuid4()),
                    'transaction': txn_dict,
                    'predicted_atms': predictions,
                    'timestamp': txn_dict['timestamp'],
                    'severity': 'HIGH' if txn_dict['fraud_probability'] > 0.9 else 'MEDIUM'
                }
                
                print(f"!!! FRAUD DETECTED !!! Type: {txn_dict['fraud_type']}")
                await sio.emit('new_alert', alert_data)
                
        except Exception as e:
            print(f"Simulation Error: {e}")
            
        # Sleep to control rate
        await asyncio.sleep(random.uniform(0.5, 1.5))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(socket_app, host="0.0.0.0", port=8000)
