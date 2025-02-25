import random
import time
from datetime import datetime, timedelta
import os
from pymongo import MongoClient

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.environ.get("DB_NAME", "oran_db")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "metrics")

CPU_THRESHOLD = int(os.environ.get("CPU_THRESHOLD", "100"))
MEM_THRESHOLD = int(os.environ.get("MEM_THRESHOLD", "400"))
REDUCE_TO = int(os.environ.get("REDUCE_TO", "5"))

class UEAgent:
    def __init__(self, initial_bandwidth=1):
        self.bandwidth = initial_bandwidth
    
    def update_bandwidth(self):
        self.bandwidth = random.randint(1, 10)
    
    def set_bandwidth(self, new_bw):
        self.bandwidth = new_bw
    
    def get_bandwidth(self):
        return self.bandwidth

class DRLAgent:
    def __init__(self, cpu_threshold=100, mem_threshold=400, reduce_to=5):
        self.cpu_threshold = cpu_threshold
        self.mem_threshold = mem_threshold
        self.reduce_to = reduce_to
    
    def decide_action(self, component_metrics):
        for metric in component_metrics:
            if metric["cpu"] > self.cpu_threshold or metric["memory"] > self.mem_threshold:
                return ('reduce_bandwidth', self.reduce_to)
        return ('no_action', None)

if __name__ == "__main__":
    ue_agent = UEAgent(initial_bandwidth=1)
    drl_agent = DRLAgent(cpu_threshold=CPU_THRESHOLD, mem_threshold=MEM_THRESHOLD, reduce_to=REDUCE_TO)
    
    components = [
        "o-ran-ru",
        "o-ran-du",
        "o-ran-cu",
        "5gc-amf",
        "5gc-smf",
        "5gc-upf"
    ]

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    current_time = datetime(2024, 11, 6, 14, 14, 46)

    while True:
        ue_agent.update_bandwidth()
        current_bw = ue_agent.get_bandwidth()

        component_metrics = []
        for component in components:
            cpu_m = 30 + current_bw * random.randint(7, 12)
            memory_mi = 200 + current_bw * random.randint(25, 40)
            component_metrics.append({
                "timestamp": current_time,
                "component": component,
                "cpu": cpu_m,
                "memory": memory_mi
            })

        # Decide DRL action
        action, value = drl_agent.decide_action(component_metrics)
        if action == 'reduce_bandwidth':
            ue_agent.set_bandwidth(value)
        
        # Insert a record for UE bandwidth
        record = {
            "timestamp": current_time,
            "ue_bandwidth": ue_agent.get_bandwidth(),
            "components": component_metrics
        }
        collection.insert_one(record)

        print(f"> Generated Bandwidth from UE={ue_agent.get_bandwidth()} Mbps, Action={action}")

        current_time += timedelta(seconds=10)
        time.sleep(10)
