import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Initialize Faker
fake = Faker('en_IN')

# Constants
TOTAL_ROWS = 50000
NORMAL_ROWS = 45000
MULE_ROWS = 4000
CIRCULAR_ROWS = 1000

NEW_DELHI_LAT = 28.6139
NEW_DELHI_LNG = 77.2090
RADIUS_KM = 50

# Helper function to generate random lat/lng within radius using Gaussian distribution
def generate_location(center_lat, center_lng, radius_km):
    # 1 degree lat ~= 111 km
    # 1 degree lng ~= 111 km * cos(lat)
    
    # Use Gaussian distribution for clustering around the center
    # sigma = radius / 3 ensures ~99% of points are within radius
    sigma_km = radius_km / 3
    
    lat_offset_km = np.random.normal(0, sigma_km)
    lng_offset_km = np.random.normal(0, sigma_km)
    
    new_lat = center_lat + (lat_offset_km / 111)
    new_lng = center_lng + (lng_offset_km / (111 * np.cos(np.radians(center_lat))))
    
    return new_lat, new_lng

def generate_data():
    print("Starting data generation...")
    data = []
    
    # --- Scenario A: Normal Behavior (45,000 rows) ---
    print(f"Generating {NORMAL_ROWS} normal transactions...")
    for _ in range(NORMAL_ROWS):
        lat, lng = generate_location(NEW_DELHI_LAT, NEW_DELHI_LNG, RADIUS_KM)
        data.append({
            'txn_id': fake.uuid4(),
            'sender_id': fake.uuid4(),
            'receiver_id': fake.uuid4(),
            'amount': round(random.uniform(50, 5000), 2),
            'timestamp': fake.date_time_between(start_date='-30d', end_date='now'),
            'lat': lat,
            'lng': lng,
            'device_id': fake.uuid4(),
            'is_fraud': 0
        })

    # --- Scenario B: Mule Fan-Out Attack (4,000 rows) ---
    # Logic: One sender -> 10 receivers, same time window, same device/location for receivers
    print(f"Generating {MULE_ROWS} Mule Fan-Out transactions...")
    mule_batches = MULE_ROWS // 10
    
    for _ in range(mule_batches):
        sender_id = fake.uuid4()
        base_time = fake.date_time_between(start_date='-30d', end_date='now')
        
        # The "Tell": Same device and location for all receivers (or very close)
        fraud_device_id = fake.uuid4()
        fraud_lat, fraud_lng = generate_location(NEW_DELHI_LAT, NEW_DELHI_LNG, RADIUS_KM)
        
        for _ in range(10):
            data.append({
                'txn_id': fake.uuid4(),
                'sender_id': sender_id,
                'receiver_id': fake.uuid4(),
                'amount': 49999.00, # Exact amount
                'timestamp': base_time + timedelta(seconds=random.randint(0, 120)), # Within 2 mins
                'lat': fraud_lat,
                'lng': fraud_lng,
                'device_id': fraud_device_id,
                'is_fraud': 1
            })

    # --- Scenario C: Circular Trading (1,000 rows) ---
    # Logic: A -> B -> C -> A
    print(f"Generating {CIRCULAR_ROWS} Circular Trading transactions...")
    # Each cycle is 3 transactions. 1000 rows / 3 per cycle ~= 333 cycles. 
    # We'll do 333 cycles -> 999 rows. Add one random fraud to make it even 1000 or just do 334 cycles and trim.
    # Let's do 333 cycles of 3 transactions = 999 rows. 
    # To hit exactly 1000, we can just add one more standalone fraud or just do 334 and slice.
    # Let's do 333 cycles and add one extra fraud row manually to match count exactly if needed, 
    # or just accept 999/1002. The prompt says "1,000 rows". 
    # Let's do 333 cycles of 3 = 999. Then 1 extra.
    
    cycles = CIRCULAR_ROWS // 3
    remainder = CIRCULAR_ROWS % 3
    
    for _ in range(cycles):
        user_a = fake.uuid4()
        user_b = fake.uuid4()
        user_c = fake.uuid4()
        
        cycle_amount = round(random.uniform(100000, 500000), 2)
        cycle_time = fake.date_time_between(start_date='-30d', end_date='now')
        
        # A -> B
        data.append({
            'txn_id': fake.uuid4(),
            'sender_id': user_a,
            'receiver_id': user_b,
            'amount': cycle_amount,
            'timestamp': cycle_time,
            'lat': NEW_DELHI_LAT + np.random.normal(0, 0.01),
            'lng': NEW_DELHI_LNG + np.random.normal(0, 0.01),
            'device_id': fake.uuid4(),
            'is_fraud': 1
        })
        
        # B -> C
        data.append({
            'txn_id': fake.uuid4(),
            'sender_id': user_b,
            'receiver_id': user_c,
            'amount': cycle_amount,
            'timestamp': cycle_time + timedelta(minutes=random.randint(10, 60)),
            'lat': NEW_DELHI_LAT + np.random.normal(0, 0.01),
            'lng': NEW_DELHI_LNG + np.random.normal(0, 0.01),
            'device_id': fake.uuid4(),
            'is_fraud': 1
        })
        
        # C -> A
        data.append({
            'txn_id': fake.uuid4(),
            'sender_id': user_c,
            'receiver_id': user_a,
            'amount': cycle_amount,
            'timestamp': cycle_time + timedelta(minutes=random.randint(70, 120)),
            'lat': NEW_DELHI_LAT + np.random.normal(0, 0.01),
            'lng': NEW_DELHI_LNG + np.random.normal(0, 0.01),
            'device_id': fake.uuid4(),
            'is_fraud': 1
        })

    # Fill remainder if any (should be 1 row if 1000 total)
    for _ in range(remainder):
         data.append({
            'txn_id': fake.uuid4(),
            'sender_id': fake.uuid4(),
            'receiver_id': fake.uuid4(),
            'amount': 150000.00,
            'timestamp': fake.date_time_between(start_date='-30d', end_date='now'),
            'lat': NEW_DELHI_LAT,
            'lng': NEW_DELHI_LNG,
            'device_id': fake.uuid4(),
            'is_fraud': 1
        })

    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Ensure directory exists
    os.makedirs('backend/data', exist_ok=True)
    
    # Save to CSV
    output_path = 'backend/data/historical_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Data Generation Complete: {len(df)} rows.")

if __name__ == "__main__":
    generate_data()
