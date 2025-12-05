# backend/data/atm_locations.py
import random
import numpy as np

# Indian ATM/Branch database with realistic distributions
ATM_DATABASE = {
    'Delhi': [
        {'id': 'ATM_DEL_001', 'bank': 'SBI', 'lat': 28.6139, 'lng': 77.2090, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_DEL_002', 'bank': 'HDFC', 'lat': 28.7041, 'lng': 77.1025, 'district': 'North', 'type': 'Branch'},
        {'id': 'ATM_DEL_003', 'bank': 'ICICI', 'lat': 28.5355, 'lng': 77.3910, 'district': 'East', 'type': 'ATM'},
        {'id': 'ATM_DEL_004', 'bank': 'Axis', 'lat': 28.4595, 'lng': 77.0266, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_DEL_005', 'bank': 'PNB', 'lat': 28.6692, 'lng': 77.4538, 'district': 'East', 'type': 'Branch'},
        {'id': 'ATM_DEL_006', 'bank': 'SBI', 'lat': 28.6304, 'lng': 77.2177, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_DEL_007', 'bank': 'HDFC', 'lat': 28.5494, 'lng': 77.2501, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_DEL_008', 'bank': 'ICICI', 'lat': 28.7196, 'lng': 77.0369, 'district': 'West', 'type': 'ATM'},
        {'id': 'ATM_DEL_009', 'bank': 'Kotak', 'lat': 28.5921, 'lng': 77.0460, 'district': 'West', 'type': 'Branch'},
        {'id': 'ATM_DEL_010', 'bank': 'SBI', 'lat': 28.6517, 'lng': 77.2219, 'district': 'Central', 'type': 'ATM'},
    ],
    'Mumbai': [
        {'id': 'ATM_MUM_001', 'bank': 'SBI', 'lat': 19.0760, 'lng': 72.8777, 'district': 'South', 'type': 'Branch'},
        {'id': 'ATM_MUM_002', 'bank': 'HDFC', 'lat': 19.0596, 'lng': 72.8295, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_MUM_003', 'bank': 'ICICI', 'lat': 19.1136, 'lng': 72.8697, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_MUM_004', 'bank': 'Axis', 'lat': 19.2183, 'lng': 72.9781, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_MUM_005', 'bank': 'PNB', 'lat': 18.9388, 'lng': 72.8354, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_MUM_006', 'bank': 'SBI', 'lat': 19.0551, 'lng': 72.8324, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_MUM_007', 'bank': 'HDFC', 'lat': 19.1176, 'lng': 72.9060, 'district': 'Central', 'type': 'Branch'},
        {'id': 'ATM_MUM_008', 'bank': 'Kotak', 'lat': 19.0330, 'lng': 73.0297, 'district': 'East', 'type': 'ATM'},
        {'id': 'ATM_MUM_009', 'bank': 'ICICI', 'lat': 19.2812, 'lng': 72.8681, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_MUM_010', 'bank': 'Axis', 'lat': 19.0144, 'lng': 72.8479, 'district': 'South', 'type': 'ATM'},
    ],
    'Bengaluru': [
        {'id': 'ATM_BLR_001', 'bank': 'SBI', 'lat': 12.9716, 'lng': 77.5946, 'district': 'Central', 'type': 'Branch'},
        {'id': 'ATM_BLR_002', 'bank': 'HDFC', 'lat': 12.9698, 'lng': 77.7499, 'district': 'East', 'type': 'ATM'},
        {'id': 'ATM_BLR_003', 'bank': 'ICICI', 'lat': 13.0358, 'lng': 77.5970, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_BLR_004', 'bank': 'Axis', 'lat': 12.9352, 'lng': 77.6245, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_BLR_005', 'bank': 'Canara', 'lat': 12.8406, 'lng': 77.6602, 'district': 'South', 'type': 'Branch'},
        {'id': 'ATM_BLR_006', 'bank': 'SBI', 'lat': 13.0097, 'lng': 77.5505, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_BLR_007', 'bank': 'HDFC', 'lat': 12.9941, 'lng': 77.5904, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_BLR_008', 'bank': 'ICICI', 'lat': 12.9138, 'lng': 77.6387, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_BLR_009', 'bank': 'Kotak', 'lat': 13.0472, 'lng': 77.5933, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_BLR_010', 'bank': 'Axis', 'lat': 12.9599, 'lng': 77.6403, 'district': 'Central', 'type': 'Branch'},
    ],
    'Chennai': [
        {'id': 'ATM_CHE_001', 'bank': 'SBI', 'lat': 13.0827, 'lng': 80.2707, 'district': 'Central', 'type': 'Branch'},
        {'id': 'ATM_CHE_002', 'bank': 'HDFC', 'lat': 13.0569, 'lng': 80.2425, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_CHE_003', 'bank': 'ICICI', 'lat': 13.0475, 'lng': 80.2824, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_CHE_004', 'bank': 'Indian', 'lat': 13.0137, 'lng': 80.2206, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_CHE_005', 'bank': 'Axis', 'lat': 13.1156, 'lng': 80.2086, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_CHE_006', 'bank': 'SBI', 'lat': 13.0358, 'lng': 80.2573, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_CHE_007', 'bank': 'HDFC', 'lat': 13.0670, 'lng': 80.2378, 'district': 'North', 'type': 'Branch'},
        {'id': 'ATM_CHE_008', 'bank': 'Canara', 'lat': 12.9941, 'lng': 80.2467, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_CHE_009', 'bank': 'ICICI', 'lat': 13.0905, 'lng': 80.2093, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_CHE_010', 'bank': 'PNB', 'lat': 13.0260, 'lng': 80.2574, 'district': 'Central', 'type': 'ATM'},
    ],
    'Kolkata': [
        {'id': 'ATM_KOL_001', 'bank': 'SBI', 'lat': 22.5726, 'lng': 88.3639, 'district': 'Central', 'type': 'Branch'},
        {'id': 'ATM_KOL_002', 'bank': 'HDFC', 'lat': 22.5697, 'lng': 88.3959, 'district': 'East', 'type': 'ATM'},
        {'id': 'ATM_KOL_003', 'bank': 'ICICI', 'lat': 22.5958, 'lng': 88.4497, 'district': 'East', 'type': 'ATM'},
        {'id': 'ATM_KOL_004', 'bank': 'Axis', 'lat': 22.5431, 'lng': 88.3425, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_KOL_005', 'bank': 'PNB', 'lat': 22.6448, 'lng': 88.4315, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_KOL_006', 'bank': 'SBI', 'lat': 22.5511, 'lng': 88.3519, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_KOL_007', 'bank': 'HDFC', 'lat': 22.5937, 'lng': 88.3628, 'district': 'Central', 'type': 'Branch'},
        {'id': 'ATM_KOL_008', 'bank': 'Indian', 'lat': 22.5151, 'lng': 88.3395, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_KOL_009', 'bank': 'ICICI', 'lat': 22.6279, 'lng': 88.4317, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_KOL_010', 'bank': 'Kotak', 'lat': 22.5354, 'lng': 88.3643, 'district': 'Central', 'type': 'ATM'},
    ],
    'Lucknow': [
        {'id': 'ATM_LKO_001', 'bank': 'SBI', 'lat': 26.8467, 'lng': 80.9462, 'district': 'Central', 'type': 'Branch'},
        {'id': 'ATM_LKO_002', 'bank': 'PNB', 'lat': 26.8389, 'lng': 80.9234, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_LKO_003', 'bank': 'HDFC', 'lat': 26.8850, 'lng': 81.0066, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_LKO_004', 'bank': 'ICICI', 'lat': 26.8077, 'lng': 80.9411, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_LKO_005', 'bank': 'Axis', 'lat': 26.9124, 'lng': 80.9424, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_LKO_006', 'bank': 'SBI', 'lat': 26.8206, 'lng': 80.9293, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_LKO_007', 'bank': 'Canara', 'lat': 26.8672, 'lng': 80.9926, 'district': 'East', 'type': 'Branch'},
        {'id': 'ATM_LKO_008', 'bank': 'HDFC', 'lat': 26.7922, 'lng': 80.9131, 'district': 'South', 'type': 'ATM'},
    ],
    'Indore': [
        {'id': 'ATM_IND_001', 'bank': 'SBI', 'lat': 22.7196, 'lng': 75.8577, 'district': 'Central', 'type': 'Branch'},
        {'id': 'ATM_IND_002', 'bank': 'HDFC', 'lat': 22.7242, 'lng': 75.8649, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_IND_003', 'bank': 'ICICI', 'lat': 22.7532, 'lng': 75.8937, 'district': 'North', 'type': 'ATM'},
        {'id': 'ATM_IND_004', 'bank': 'Axis', 'lat': 22.6860, 'lng': 75.8333, 'district': 'South', 'type': 'ATM'},
        {'id': 'ATM_IND_005', 'bank': 'PNB', 'lat': 22.7470, 'lng': 75.9016, 'district': 'East', 'type': 'ATM'},
        {'id': 'ATM_IND_006', 'bank': 'SBI', 'lat': 22.7074, 'lng': 75.8737, 'district': 'Central', 'type': 'ATM'},
        {'id': 'ATM_IND_007', 'bank': 'HDFC', 'lat': 22.7658, 'lng': 75.8382, 'district': 'North', 'type': 'Branch'},
    ],
}

def get_all_atms():
    """Flatten ATM database into single list"""
    all_atms = []
    for city, atms in ATM_DATABASE.items():
        for atm in atms:
            atm['city'] = city
            all_atms.append(atm)
    return all_atms

def get_atms_by_city(city):
    """Get ATMs for specific city"""
    return ATM_DATABASE.get(city, [])

def find_nearest_atms(lat, lng, radius_km=10, limit=5):
    """Find nearest ATMs within radius"""
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371  # Earth radius in km
        dlat = np.radians(lat2 - lat1)
        dlon = np.radians(lon2 - lon1)
        a = np.sin(dlat/2)**2 + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.sin(dlon/2)**2
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
        return R * c
    
    all_atms = get_all_atms()
    atms_with_distance = []
    
    for atm in all_atms:
        distance = haversine(lat, lng, atm['lat'], atm['lng'])
        if distance <= radius_km:
            atm_copy = atm.copy()
            atm_copy['distance_km'] = distance
            atms_with_distance.append(atm_copy)
    
    # Sort by distance and return top N
    atms_with_distance.sort(key=lambda x: x['distance_km'])
    return atms_with_distance[:limit]
