import pandas as pd
import numpy as np
import random
import uuid
from datetime import datetime, timedelta
import os
from data.atm_locations import ATM_LOCATIONS

# Configuration
TOTAL_ROWS = 60000
NORMAL_TXNS = 40000
MULE_TXNS = 5000  # Fan-out
CIRCULAR_TXNS = 5000
# Remainder or adjustment to fit total

DATA_DIR = 'backend/data'
os.makedirs(DATA_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(DATA_DIR, 'historical_data.csv')

# Cities and Centers (approx lat/lng)
CITIES = {
    "Delhi": (28.6139, 77.2090),
    "Mumbai": (19.0760, 72.8777),
    "Bengaluru": (12.9716, 77.5946),
    "Chennai": (13.0827, 80.2707),
    "Kolkata": (22.5726, 88.3639),
    "Lucknow": (26.8467, 80.9462),
    "Indore": (22.7196, 75.8577)
}

def generate_random_location(city_center, radius_km=10):
    # Convert km to degrees (rough approx)
    # 1 deg lat ~ 111 km
    r = radius_km / 111.0
    u = random.random()
    v = random.random()
    w = r * np.sqrt(u)
    t = 2 * np.pi * v
    x = w * np.cos(t)
    y = w * np.sin(t)
    
    lat = city_center[0] + x
    lng = city_center[1] + y
    return lat, lng

def get_closest_atm(lat, lng, city=None):
    # Filter ATMs by city if provided, else all
    candidates = [atm for atm in ATM_LOCATIONS if city is None or atm['city'] == city]
    if not candidates:
        candidates = ATM_LOCATIONS
    
    # Simple Euclidean distance for speed (valid for small distances)
    best_atm = None
    min_dist = float('inf')
    
    for atm in candidates:
        dist = (atm['lat'] - lat)**2 + (atm['lng'] - lng)**2
        if dist < min_dist:
            min_dist = dist
            best_atm = atm
            
    return best_atm

def generate_data():
    print(f"Starting enhanced data generation with withdrawal predictions...")
    
    data = []
    
    # helper for dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    # 1. Normal Transactions
    print(f"Generating {NORMAL_TXNS} normal transactions...")
    for _ in range(NORMAL_TXNS):
        city_name = random.choice(list(CITIES.keys()))
        lat, lng = generate_random_location(CITIES[city_name])
        
        txn = {
            'txn_id': str(uuid.uuid4()),
            'sender_id': f"User_{random.randint(1, 5000)}",
            'receiver_id': f"User_{random.randint(5001, 10000)}",
            'amount': round(random.uniform(10, 5000), 2),
            'timestamp': start_date + (end_date - start_date) * random.random(),
            'lat': lat,
            'lng': lng,
            'city': city_name,
            'is_fraud': 0,
            'txn_type': 'payment',
            'withdrawal_atm_id': None # Normal payments often don't have immediate withdrawals
        }
        data.append(txn)

    # 2. Mule Fan-Out (Fraud)
    # One mule receives huge money then transfers small amounts to many accounts, 
    # OR One sender sends to many mules who then withdraw.
    # Pattern: 1 Sender -> N Receivers (Mules) -> Cash Withdrawal at ATM
    print(f"Generating {MULE_TXNS} Mule Fan-Out transactions with withdrawals...")
    
    mule_groups = 500
    txns_per_group = MULE_TXNS // mule_groups # ~10
    
    for i in range(mule_groups):
        master_fraudster = f"Fraudster_{random.randint(1, 100)}"
        city_name = random.choice(list(CITIES.keys()))
        
        # Burst time
        burst_time = start_date + (end_date - start_date) * random.random()
        
        for j in range(txns_per_group):
            # Locations often clustered or slightly scattered
            lat, lng = generate_random_location(CITIES[city_name], radius_km=5)
            
            # Prediction: Mules withdraw at closest ATM
            closest_atm = get_closest_atm(lat, lng, city_name)
            
            txn = {
                'txn_id': str(uuid.uuid4()),
                'sender_id': master_fraudster,
                'receiver_id': f"Mule_{random.randint(1, 1000)}",
                'amount': round(random.uniform(10000, 50000), 2),
                'timestamp': burst_time + timedelta(seconds=random.randint(0, 300)), # rapid succession
                'lat': lat,
                'lng': lng,
                'city': city_name,
                'is_fraud': 1,
                'txn_type': 'transfer_to_mule',
                'withdrawal_atm_id': closest_atm['id'] if closest_atm else None
            }
            data.append(txn)

    # 3. Circular Trading (Fraud)
    # A -> B -> C -> A
    print(f"Generating {CIRCULAR_TXNS} Circular Trading transactions...")
    circles = 1000 # 5000 txns / ~3-5 per circle
    
    for i in range(circles):
        circle_size = random.randint(3, 5)
        participants = [f"CircleUser_{random.randint(1, 1000)}" for _ in range(circle_size)]
        
        base_amount = round(random.uniform(50000, 100000), 2)
        city_name = random.choice(list(CITIES.keys()))
        lat, lng = generate_random_location(CITIES[city_name])
        
        txn_time = start_date + (end_date - start_date) * random.random()
        
        for k in range(circle_size):
            sender = participants[k]
            receiver = participants[(k + 1) % circle_size]
            
            txn = {
                'txn_id': str(uuid.uuid4()),
                'sender_id': sender,
                'receiver_id': receiver,
                'amount': base_amount * random.uniform(0.95, 1.05), # slightly varying
                'timestamp': txn_time + timedelta(minutes=random.randint(5, 60)),
                'lat': lat + random.uniform(-0.01, 0.01),
                'lng': lng + random.uniform(-0.01, 0.01),
                'city': city_name,
                'is_fraud': 1,
                'txn_type': 'circular',
                'withdrawal_atm_id': None
            }
            data.append(txn)
            txn_time += timedelta(minutes=random.randint(10, 30))

    # Convert to DF
    df = pd.DataFrame(data)
    
    # Ensure sorted by time
    df = df.sort_values('timestamp')
    
    print(f"\n=== DATA GENERATION COMPLETE ===")
    print(f"Total rows: {len(df)}")
    print(f"Transfers: {len(df)}")
    print(f"Withdrawals predicted: {df['withdrawal_atm_id'].notnull().sum()}")
    print(f"Fraud transactions: {df['is_fraud'].sum()}")
    
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_data()