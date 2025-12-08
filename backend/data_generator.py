import random
import uuid
from datetime import datetime, timedelta
from backend.database import SessionLocal, init_db, ATM, Transaction, Suspect
from backend.data.atm_locations import ATM_LOCATIONS
from sqlalchemy.orm import Session
import math

# --- LOGIC CONSTANTS ---
IMPOSSIBLE_TRAVEL_SPEED_KMH = 800 # If > 800 km/h, it's impossible (unless flying, but still suspicious for ATM)
MAX_DAILY_WITHDRAWAL = 50000

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

class DataGenerator:
    def __init__(self):
        init_db()
        self.db = SessionLocal()
        self.seed_atms()
        # Cache for velocity checks
        self.user_last_loc = {} # {user_id: (lat, lng, timestamp)}

    def seed_atms(self):
        if self.db.query(ATM).count() == 0:
            print("Seeding ATMs...")
            for atm_data in ATM_LOCATIONS:
                atm = ATM(**atm_data)
                self.db.add(atm)
            self.db.commit()

    def generate_smart_transaction(self):
        """
        Generates a transaction with "Crystal Clear" fraud logic injected dynamically.
        """
        # 1. Pick a random ATM
        atm = random.choice(ATM_LOCATIONS)
        
        # 2. Pick a User
        user_id = f"User_{random.randint(1000, 1020)}" # Small pool to force collisions/relocation
        
        # 3. Determine if we want to FORCE a fraud scenario for demo
        # 40% chance of fraud for visibility
        is_fraud_scenario = random.random() < 0.4
        
        amount = random.choice([500, 1000, 2000, 5000, 10000, 20000])
        txn_time = datetime.utcnow()
        fraud_type = None
        fraud_prob = 0.1
        
        # Track previous location for visualization
        prev_loc = self.user_last_loc.get(user_id)
        
        # --- LOGIC: VELOCITY CHECK (Impossible Travel) ---
        if prev_loc:
            last_lat, last_lng, last_time = prev_loc
            distance = haversine(last_lat, last_lng, atm['lat'], atm['lng'])
            time_diff_hours = (txn_time - last_time).total_seconds() / 3600 + 0.001
            speed = distance / time_diff_hours
            
            if speed > IMPOSSIBLE_TRAVEL_SPEED_KMH:
                is_fraud_scenario = True
                fraud_type = "VELOCITY_IMPOSSIBLE_TRAVEL"
                fraud_prob = 0.99
                print(f"FRAUD: Impossible Travel. {speed:.0f} km/h")
        
        # --- LOGIC: ANOMALY (Sudden High Value in New City) ---
        # Simulating "Home City" logic
        # Assume User_1000 lives in Delhi. If he transacts in Chennai -> Flag
        if user_id == "User_1000" and atm['city'] != "Delhi":
             is_fraud_scenario = True
             fraud_type = "GEOSPATIAL_ANOMALY"
             fraud_prob = 0.85
             amount = 45000 # Max out
        
        if is_fraud_scenario and not fraud_type:
             # Genuine Random Fraud (e.g. Card Cloning pattern)
             fraud_type = "PATTERN_CLONED_CARD"
             fraud_prob = 0.92

        # Update Last Location
        self.user_last_loc[user_id] = (atm['lat'], atm['lng'], txn_time)
        
        # Create Transaction Object
        txn = Transaction(
            txn_id=str(uuid.uuid4()),
            atm_id=atm['id'],
            sender_id=user_id,
            amount=amount,
            timestamp=txn_time,
            lat=atm['lat'],
            lng=atm['lng'],
            city=atm['city'],
            is_fraud=is_fraud_scenario,
            fraud_probability=fraud_prob,
            fraud_type=fraud_type,
            status="DECLINED_FRAUD" if fraud_prob > 0.9 else "SUCCESS"
        )
        
        # Commit to DB
        self.db.add(txn)
        self.db.commit()
        
        # Convert to dict for SocketIO
        return {
            "txn_id": txn.txn_id,
            "amount": txn.amount,
            "lat": txn.lat,
            "lng": txn.lng,
            "prev_lat": prev_loc[0] if prev_loc else None, # For Jump Vector
            "prev_lng": prev_loc[1] if prev_loc else None,
            "location": atm['location'],
            "city": txn.city,
            "sender_id": txn.sender_id,
            "is_fraud": txn.is_fraud,
            "fraud_probability": txn.fraud_probability,
            "fraud_type": txn.fraud_type,
            "timestamp": txn.timestamp.isoformat(),
            "status": txn.status
        }

generator = DataGenerator()