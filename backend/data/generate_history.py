import pandas as pd
import numpy as np
import random
import uuid
from datetime import datetime, timedelta

# Configuration
NUM_RECORDS = 5000
START_DATE = datetime(2025, 1, 1)
CITIES = ["Delhi", "Mumbai", "Bengaluru", "Chennai", "Kolkata", "Lucknow", "Indore"]
FRAUD_TYPES = ["UPI_SCAM", "CLONED_CARD", "SIM_SWAP", "PHISHING", "IMPOSSIBLE_TRAVEL", "WAITING_GAME"]

# Helper to generate random date
def random_date(start, end):
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = random.randrange(int_delta)
    return start + timedelta(seconds=random_second)

print("Generating Crystal Clear Historical Data...")

data = []
for _ in range(NUM_RECORDS):
    is_fraud = random.random() < 0.15 # 15% fraud rate
    
    city = random.choice(CITIES)
    amount = random.randint(100, 50000)
    
    # Logic: Fraud is usually higher amount
    if is_fraud:
        amount = random.randint(5000, 100000)
        fraud_type = random.choice(FRAUD_TYPES)
        
        # Scenario: User vs Fraudster Location
        user_loc = city
        fraudster_loc = random.choice([c for c in CITIES if c != city]) # Different city often
    else:
        fraud_type = "NONE"
        user_loc = city
        fraudster_loc = city
    
    # Enhanced Data Parameters for REALISM
    # 1. Merchant Category Code (MCC)
    if is_fraud:
        # High Risk MCCs: 7995 (Gambling), 6051 (Crypto), 4829 (Wire Transfer)
        mcc = random.choice([7995, 6051, 4829, 5967])
        # Fraudsters often use Emulators or Rooted Androids
        device_id = f"Emulator_{random.randint(1000, 9999)}"
        # IP Address often proxies (Non-Indian IPs or Datacenter IPs)
        ip_addr = f"{random.choice([45, 103, 185])}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    else:
        # Normal MCCs: 5411 (Grocery), 5812 (Dining), 5311 (Department Store)
        mcc = random.choice([5411, 5812, 5311, 4121])
        # Normal Devices
        device_id = random.choice(["iPhone13", "SamsungS21", "OnePlus9", "Pixel6"]) + f"_{random.randint(100,999)}"
        # Normal Home/Mobile IP
        ip_addr = f"192.168.{random.randint(0,255)}.{random.randint(0,255)}"
    # Map city to coords (Approx)
    coords = {
        "Delhi": (28.7041, 77.1025),
        "Mumbai": (19.0760, 72.8777),
        "Bangalore": (12.9716, 77.5946),
        "Chennai": (13.0827, 80.2707),
        "Kolkata": (22.5726, 88.3639),
        "Hyderabad": (17.3850, 78.4867),
        "Pune": (18.5204, 73.8567),
        "Ahmedabad": (23.0225, 72.5714),
        "Jaipur": (26.9124, 75.7873),
        "Lucknow": (26.8467, 80.9462)
    }
    lat, lng = coords.get(city, (20.5937, 78.9629))
    
    sender_id = f"User_{random.randint(1000, 5000)}" 
        
    row = {
        "txn_id": str(uuid.uuid4()),
        "sender_id": sender_id,
        "timestamp": random_date(START_DATE, datetime.now()).isoformat(),
        "amount": amount,
        "city": city,
        "lat": lat,
        "lng": lng,
        "user_home_location": user_loc,
        "active_location": fraudster_loc, # Where txn happened
        "fraud_type": fraud_type,
        "is_fraud": 1 if is_fraud else 0,
        "is_fraud": 1 if is_fraud else 0,
        "bank_response_time_ms": random.randint(50, 400),
        # New Tech Fields for Judges
        "mcc": mcc,
        "device_id": device_id,
        "ip_address": ip_addr
    }
    data.append(row)

df = pd.DataFrame(data)
# Save to CSV
OUTPUT_PATH = "backend/data/historical_data_enriched.csv"
df.to_csv(OUTPUT_PATH, index=False)
print(f"Successfully generated {NUM_RECORDS} records at {OUTPUT_PATH}")
