from fastapi import FastAPI, BackgroundTasks, Depends, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import socketio
import asyncio
import uuid
import random
import sys
import json
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel

# Local Imports
from backend.database import get_db, Transaction, ATM, User, Fraudster, Complaint, FraudAlert
from backend.data_generator import generator
from backend.prediction_engine import engine as prediction_engine

# --- App Setup ---
app = FastAPI(title="Kavach Titanium Enterprise", version="2.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Socket.IO
sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='*')
socket_app = socketio.ASGIApp(sio, app)

# Global State
SIMULATION_ACTIVE = True

# --- Terminal Simulation Loop ---
async def terminal_simulation_loop():
    """
    Runs a visible loop in the terminal simulating real-time transactions.
    """
    print("\n" + "="*60)
    print(" KAVACH TITANIUM - REAL-TIME TRANSACTION MONITORING")
    print("="*60 + "\n")
    print(f"{'TXN ID':<10} | {'AMOUNT':<10} | {'MERCHANT':<20} | {'STATUS':<10} | {'PREDICTION'}")
    print("-" * 80)
    
    while True:
        if SIMULATION_ACTIVE:
            try:
                # 1. Generate Real-time Data
                txn_data = generator.generate_smart_transaction()
                
                # 2. Predict (Redundant with Generator internals but authentic simulation flows)
                # In a real system, generator -> queue -> model. Here generator does it.
                # We'll use the prediction engine to get "Next Withdrawal Location" if fraud
                
                pred_text = "Safe"
                if txn_data['is_fraud']:
                    # Predict Next Location
                    predictions = prediction_engine.predict_withdrawal_locations(txn_data)
                    top_loc = predictions[0]['location'] if predictions else "Unknown"
                    pred_text = f"FRAUD DETECTED! Intercept @ {top_loc[:15]}..."
                    
                    # Emit Alert
                    await sio.emit('new_alert', {
                        'id': str(uuid.uuid4()),
                        'transaction': txn_data,
                        'predicted_atms': predictions,
                        'timestamp': txn_data['timestamp'],
                        'severity': 'CRITICAL'
                    })
                
                # 3. Terminal Output
                status_color =  "BLOCKED" if txn_data.get('status') == 'BLOCKED' else "SUCCESS"
                print(f"{txn_data['txn_id'][:8]}.. | ₹{txn_data['amount']:<8} | {txn_data['merchant'][:18]:<18} | {status_color:<10} | {pred_text}")
                
                # 4. Emit to Dashboard
                await sio.emit('new_transaction', txn_data)
                
            except Exception as e:
                print(f"[!] Simulation Error: {e}")
                
        await asyncio.sleep(random.uniform(0.5, 1.5))

@app.on_event("startup")
async def startup_event():
    # Start the background loop
    asyncio.create_task(terminal_simulation_loop())

# --- REST Endpoints ---

@app.get("/")
def read_root():
    return {"status": "TITANIUM SHIELD ONLINE", "version": "2.0-Enterprise"}

@app.get("/api/atms")
def get_atms(db: Session = Depends(get_db)):
    return db.query(ATM).all()

@app.get("/api/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_txns = db.query(Transaction).count()
    fraud_txns = db.query(Transaction).filter(Transaction.is_fraud == True).count()
    users_count = db.query(User).count()
    
    return {
        "active_monitoring": True,
        "users_protected": users_count,
        "total_transactions": total_txns,
        "threats_intercepted": fraud_txns,
        "fraud_rate": round((fraud_txns/total_txns * 100) if total_txns > 0 else 0, 2)
    }

@app.get("/api/lea/stats") # Police Dashboard
def get_lea_stats(db: Session = Depends(get_db)):
    recent_frauds = db.query(Transaction).filter(Transaction.is_fraud == True).order_by(Transaction.timestamp.desc()).limit(15).all()
    
    # Serialize for frontend
    alerts_data = []
    for t in recent_frauds:
        alerts_data.append({
             "transaction": { # Nested to match socket structure if needed, or flat. Frontend expects 'recent_alerts' array of objects.
                 # Wait, Frontend: recent_alerts.map(alert => ... alert.sender_id) 
                 # Socket pushes { transaction: ... }. 
                 # Initial fetch should probably return list of transactions directly or list of alert objects.
                 # Frontend: setStats(prev => ... recent_alerts: [alert.transaction, ...prev] ) 
                 # So socket 'alert' has '.transaction'. 
                 # Initial fetch 'data' is setStats(data). 
                 # So data.recent_alerts should be List[TransactionDict].
                 "sender_id": t.user_id or "Unknown",
                 "city": t.city,
                 "ip_address": t.ip_address,
                 "device_id": t.device_fingerprint,
                 "fraud_type": t.fraud_type,
                 "amount": t.amount,
                 "timestamp": t.timestamp.isoformat()
             }
        })
        
    # Actually frontend maps `stats.recent_alerts.map(alert...)` 
    # But socket logic adds `alert.transaction` to the list. 
    # So the list is mixed? 
    # Socket: `setStats(prev => ... recent_alerts: [alert.transaction, ...]`
    # So the list contains `transaction` objects. 
    # My initial fetch should return `{ recent_alerts: [txn1, txn2] }`.
    
    clean_alerts = []
    for t in recent_frauds:
         clean_alerts.append({
             "sender_id": t.user_id or "Unknown",
             "city": t.city,
             "ip_address": t.ip_address,
             "device_id": t.device_fingerprint,
             "fraud_type": t.fraud_type,
             "amount": t.amount,
             "timestamp": t.timestamp.isoformat()
         })

    return {
        "active_operations": len(recent_frauds),
        "suspects_tracked": db.query(User).count(), # All users are potential suspects in this sim
        "recent_alerts": clean_alerts
    }

@app.get("/api/bank/stats") # Bank Dashboard
def get_bank_stats(db: Session = Depends(get_db)):
    frauds = db.query(Transaction).filter(Transaction.is_fraud == True).all()
    saved = sum([f.amount for f in frauds if f.status == "BLOCKED"])
    return {
        "total_saved_inr": saved,
        "blocked_cards": len(frauds),
        "false_positive_rate": "0.4%"
    }

class ComplaintRequest(BaseModel):
    mobile_no: str
    account_no: str
    email: str
    bank_name: str
    transaction_id: str
    fraud_type: str
    description: str

@app.post("/api/portal/submit")
async def submit_complaint(
    complaint: ComplaintRequest,
    db: Session = Depends(get_db)
):
    # Find user or create dummy reference
    user = db.query(User).filter(User.phone == complaint.mobile_no).first()
    
    new_complaint = Complaint(
        ticket_id=f"TKT-{random.randint(10000,99999)}",
        user_id=user.user_id if user else None,
        mobile_no=complaint.mobile_no,
        account_no=complaint.account_no,
        contact_email=complaint.email,
        description=f"[Bank: {complaint.bank_name}] [TxnID: {complaint.transaction_id}] {complaint.description}",
        fraud_type=complaint.fraud_type,
        status="OPEN"
    )
    db.add(new_complaint)
    db.commit()
    return {"status": "submitted", "ticket_id": new_complaint.ticket_id}

# --- Socket IO Control ---
@sio.event
async def connect(sid, environ):
    await sio.emit('system_status', {'status': 'connected', 'simulation': SIMULATION_ACTIVE})

@sio.event
async def start_simulation(sid):
    global SIMULATION_ACTIVE
    SIMULATION_ACTIVE = True
    print("\n>>> SIMULATION STARTED BY DASHBOARD <<<\n")
    await sio.emit('sim_status', {'running': True})

@sio.event
async def stop_simulation(sid):
    global SIMULATION_ACTIVE
    SIMULATION_ACTIVE = False
    print("\n>>> SIMULATION PAUSED <<<\n")
    await sio.emit('sim_status', {'running': False})

if __name__ == "__main__":
    import uvicorn
    # Disable Uvicorn functionality logs to keep terminal clean for our loop
    uvicorn.run(socket_app, host="0.0.0.0", port=8000, log_level="warning")
