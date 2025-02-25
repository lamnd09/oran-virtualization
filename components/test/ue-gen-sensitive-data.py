import requests
import random
import time
import json
import uuid

# Define API endpoint where UE-Agent will send data
CENTRAL_LOGGING_URL = "http://centralized-logging-mongodb:5002/logs"

# Generate unique UE identifiers
UE_IMSI = str(random.randint(222000000000000, 222999999999999))  # Simulated IMSI
UE_IMEI = str(random.randint(860000000000000, 869999999999999))  # Simulated IMEI

def generate_sensitive_data():
    """Generate sensitive UE data for ORAN network simulation."""
    return {
        "timestamp": time.time(),
        "ue_id": str(uuid.uuid4()),  # Unique UE Session ID
        "imsi": UE_IMSI,
        "imei": UE_IMEI,
        "cell_id": f"gNB-{random.randint(100, 999)}",  # Simulated Cell Tower ID
        "rsrp": round(random.uniform(-110, -80), 2),  # Reference Signal Received Power (dBm)
        "rsrq": round(random.uniform(-20, -5), 2),  # Reference Signal Received Quality (dB)
        "sinr": round(random.uniform(5, 30), 2),  # Signal-to-Interference-Noise Ratio (dB)
        "bandwidth_mhz": random.choice([5, 10, 20, 40, 80, 100]),  # Bandwidth in MHz
        "latency_ms": random.randint(5, 100),  # Network latency in milliseconds
        "packet_loss_percent": round(random.uniform(0, 5), 2),  # Packet loss percentage
        "encryption_status": random.choice(["AES-256", "ChaCha20", "Disabled"]),  # Encryption method used
        "handover_status": random.choice(["Successful", "Failed", "In Progress"]),  # Handover state
        "anomaly_detected": random.choice([True, False]),  # Indicate if anomaly is detected
    }

def send_data_to_logging():
    """Send UE-generated data to the centralized logging system."""
    data = generate_sensitive_data()
    headers = {"Content-Type": "application/json"}
    
    try:
        response = requests.post(CENTRAL_LOGGING_URL, data=json.dumps(data), headers=headers)
        if response.status_code == 200:
            print(f"UE-Agent: Data successfully sent to logging system: {data}")
        else:
            print(f"UE-Agent: Failed to send data, Status Code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"UE-Agent: Error sending data - {e}")

if __name__ == "__main__":
    while True:
        send_data_to_logging()
        time.sleep(5)  # Send data every 5 seconds
