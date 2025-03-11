import random
import time

def preprocess_vitals():
    raw_heart_rate = random.randint(50, 140)
    raw_oxygen = random.uniform(85, 100)
    alert = "High" if raw_heart_rate > 100 else "Normal"
    return {
        "patient_id": "P001",
        "heart_rate": raw_heart_rate,
        "oxygen": raw_oxygen,
        "status": "High" if raw_heart_rate > 100 else "Normal",  # Match status for consistency
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }