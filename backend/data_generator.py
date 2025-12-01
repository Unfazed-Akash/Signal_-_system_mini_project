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

# City Configuration
CITIES = {
    'Delhi': {'lat': 28.6139, 'lng': 77.2090, 'radius': 40},
    'Mumbai': {'lat': 19.0760, 'lng': 72.8777, 'radius': 35},
    'Bengaluru': {'lat': 12.9716, 'lng': 77.5946, 'radius': 30},
    'Chennai': {'lat': 13.0827, 'lng': 80.2707, 'radius': 30},
    'Kolkata': {'lat': 22.5726, 'lng': 88.3639, 'radius': 30},
    'Lucknow': {'lat': 26.8467, 'lng': 80.9462, 'radius': 20},
    'Indore': {'lat': 22.7196, 'lng': 75.8577, 'radius': 15}
}

# Helper function to generate random lat/lng within radius using Gaussian distribution
def generate_location(city_name):
    city = CITIES.get(city_name)
    if not city:
        # Default to Delhi if not found
        city = CITIES['Delhi']
        
    center_lat = city['lat']
    center_lng = city['lng']
    radius_km = city['radius']
    
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
    city_names = list(CITIES.keys())
    
    for _ in range(NORMAL_ROWS):
        # Pick a random city for this transaction
        city = random.choice(city_names)
        lat, lng = generate_location(city)
        
        data.append({
            'txn_id': fake.uuid4(),
            'sender_id': fake.uuid4(),
            'receiver_id': fake.uuid4(),
            'amount': round(random.uniform(50, 5000), 2),
            'timestamp': fake.date_time_between(start_date='-30d', end_date='now'),
            'lat': lat,
            'lng': lng,
            'device_id': fake.uuid4(),
            'is_fraud': 0,
            'city': city
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
        
        # Pick a random city for this fraud batch
        fraud_city = random.choice(city_names)
        fraud_lat, fraud_lng = generate_location(fraud_city)
        
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
                'is_fraud': 1,
                'city': fraud_city
            })

    # --- Scenario C: Circular Trading (1,000 rows) ---
    # Logic: A -> B -> C -> A
    print(f"Generating {CIRCULAR_ROWS} Circular Trading transactions...")
    
    cycles = CIRCULAR_ROWS // 3
    remainder = CIRCULAR_ROWS % 3
    
    for _ in range(cycles):
        user_a = fake.uuid4()
        user_b = fake.uuid4()
        user_c = fake.uuid4()
        
        cycle_amount = round(random.uniform(100000, 500000), 2)
        cycle_time = fake.date_time_between(start_date='-30d', end_date='now')
        
        # Pick a random city for this ring
        ring_city = random.choice(city_names)
        base_lat, base_lng = generate_location(ring_city)
        
        # A -> B
        data.append({
            'txn_id': fake.uuid4(),
            'sender_id': user_a,
            'receiver_id': user_b,
            'amount': cycle_amount,
            'timestamp': cycle_time,
            'lat': base_lat + np.random.normal(0, 0.01),
            'lng': base_lng + np.random.normal(0, 0.01),
            'device_id': fake.uuid4(),
            'is_fraud': 1,
            'city': ring_city
        })
        
        # B -> C
        data.append({
            'txn_id': fake.uuid4(),
            'sender_id': user_b,
            'receiver_id': user_c,
            'amount': cycle_amount,
            'timestamp': cycle_time + timedelta(minutes=random.randint(10, 60)),
            'lat': base_lat + np.random.normal(0, 0.01),
            'lng': base_lng + np.random.normal(0, 0.01),
            'device_id': fake.uuid4(),
            'is_fraud': 1,
            'city': ring_city
        })
        
        # C -> A
        data.append({
            'txn_id': fake.uuid4(),
            'sender_id': user_c,
            'receiver_id': user_a,
            'amount': cycle_amount,
            'timestamp': cycle_time + timedelta(minutes=random.randint(70, 120)),
            'lat': base_lat + np.random.normal(0, 0.01),
            'lng': base_lng + np.random.normal(0, 0.01),
            'device_id': fake.uuid4(),
            'is_fraud': 1,
            'city': ring_city
        })

    # Fill remainder if any (should be 1 row if 1000 total)
    for _ in range(remainder):
         rem_city = random.choice(city_names)
         rem_lat, rem_lng = generate_location(rem_city)
         data.append({
            'txn_id': fake.uuid4(),
            'sender_id': fake.uuid4(),
            'receiver_id': fake.uuid4(),
            'amount': 150000.00,
            'timestamp': fake.date_time_between(start_date='-30d', end_date='now'),
            'lat': rem_lat,
            'lng': rem_lng,
            'device_id': fake.uuid4(),
            'is_fraud': 1,
            'city': rem_city
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
