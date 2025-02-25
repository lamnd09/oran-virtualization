import requests
import random
import time

DRL_AGENT_URL = "http://drl-agent:5001/process"

def generate_network_data():
    """Generate random network data simulating UE traffic."""
    return {
        "timestamp": time.time(),
        "ratio": round(random.uniform(0.1, 0.5), 2),  # Simulated ratio between 10% and 50%
        "latency": random.randint(10, 100),  # Simulated latency in ms
        "packet_loss": round(random.uniform(0, 5), 2)  # Simulated packet loss in %
    }

def send_data_to_drl():
    """Send UE-generated data to the DRL agent."""
    data = [generate_network_data() for _ in range(5)]  # Send batch of 5 readings
    response = requests.post(DRL_AGENT_URL, json=data)
    return response.json()

if __name__ == "__main__":
    while True:
        drl_response = send_data_to_drl()
        print("UE-Agent: DRL Adjusted Response:", drl_response)
        time.sleep(10)  # Send data every 10 seconds
