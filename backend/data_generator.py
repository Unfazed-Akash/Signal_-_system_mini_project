import random
import uuid
import json
import math
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func

from backend.database import SessionLocal, init_db, ATM, Transaction, User, Fraudster, Complaint
from backend.data.atm_locations import ATM_LOCATIONS

# --- CONSTANTS ---
MERCHANT_CATEGORIES = ["Retail", "Dining", "Travel", "Electronics", "Groceries", "Utilities", "Entertainment"]
FRAUD_TYPES = ["VELOCITY_IMPOSSIBLE_TRAVEL", "GEOSPATIAL_ANOMALY", "PATTERN_CLONED_CARD", "DEVICE_MISMATCH", "HIGH_VALUE_ANOMALY"]
BENFORD_PROBS = [math.log10(1 + 1/d) for d in range(1, 10)]

class DataGenerator:
    def __init__(self):
        init_db()
        self.db = SessionLocal()
        self.seed_priors()
        
    def seed_priors(self):
        """Seed initial Users, ATMs if empty."""
        try:
            if self.db.query(ATM).count() == 0:
                print("Seeding ATMs...")
                for atm_data in ATM_LOCATIONS:
                    atm = ATM(**atm_data)
                    self.db.add(atm)
                    
            if self.db.query(User).count() == 0:
                print("Seeding Users...")
                for i in range(50):
                    user = User(
                        user_id=f"IS_USER_{1000+i}",
                        name=f"Citizen {i}",
                        email=f"citizen{i}@kavach.in",
                        phone=f"987654{1000+i}",
                        account_numbers=["ACCT" + str(random.randint(10000000, 99999999))],
                        risk_score=random.uniform(0, 0.2)
                    )
                    self.db.add(user)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            print(f"Seeding Error: {e}")

    def get_benford_amount(self):
        """Generate amount following Benford's Law."""
        leading_digit = random.choices(range(1, 10), weights=BENFORD_PROBS)[0]
        # Scale: 100 to 50,000
        magnitude = random.choice([100, 1000, 10000])
        base = leading_digit * magnitude
        # Add random noise
        return base + random.randint(0, magnitude // 2)

    def generate_smart_transaction(self):
        """
        Generates comprehensive transaction data matching new schema.
        """
        # Context
        users = self.db.query(User).all()
        if not users: self.seed_priors(); users = self.db.query(User).all()
        user = random.choice(users)
        
        atm = random.choice(ATM_LOCATIONS)
        is_fraud = random.random() < 0.20 # 20% baseline fraud rate for DEMO VISIBILITY
        
        if is_fraud:
            # Inject Specific Patterns
            fraud_scenario = random.choice(FRAUD_TYPES)
            if fraud_scenario == "HIGH_VALUE_ANOMALY":
                amount = random.randint(50000, 200000)
            else:
                amount = self.get_benford_amount()
            
            # Geo jumps logic could go here
        else:
            fraud_scenario = None
            amount = self.get_benford_amount()

        txn_id = str(uuid.uuid4())
        timestamp = datetime.utcnow()
        
        # Risk Logic (Simplified Rule Engine embedded for Generation)
        fraud_prob = 0.95 if is_fraud else 0.02
        status = "PROCESSING"
        if fraud_prob > 0.9:
            status = "BLOCKED"
        
        txn = Transaction(
            txn_id=txn_id,
            user_id=user.user_id,
            amount=float(amount),
            currency="INR",
            merchant="ATM Withdrawal" if "ATM" in atm['location'] else f"{random.choice(MERCHANT_CATEGORIES)} Store",
            merchant_category=random.choice(MERCHANT_CATEGORIES),
            timestamp=timestamp,
            geo_lat=atm['lat'],
            geo_lon=atm['lng'],
            city=atm['city'],
            device_fingerprint=f"DEV_{user.user_id}_{random.randint(1,2)}", # mostly consistent
            ip_address="192.168.1.1",
            features={
                "velocity_24h": random.randint(0, 5),
                "avg_amt_deviation": random.uniform(0.1, 3.0)
            },
            is_fraud=is_fraud,
            fraud_probability=fraud_prob,
            fraud_type=fraud_scenario,
            status=status
        )
        
        self.db.add(txn)
        self.db.commit()
        
        return {
            "txn_id": txn.txn_id,
            "sender_id": txn.user_id,
            "amount": txn.amount,
            "location": atm['location'],
            "lat": txn.geo_lat,
            "lng": txn.geo_lon,
            "city": txn.city,
            "ip_address": txn.ip_address,
            "device_id": txn.device_fingerprint,
            "fraud_type": txn.fraud_type,
            "is_fraud": txn.is_fraud,
            "fraud_prob": txn.fraud_probability,
            "merchant": txn.merchant,
            "timestamp": txn.timestamp.isoformat(),
            "status": txn.status
        }

generator = DataGenerator()