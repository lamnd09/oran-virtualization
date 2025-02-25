import random
from datetime import datetime, timedelta
import time

class UEAgent:
    def __init__(self, initial_bandwidth=1):
        self.bandwidth = initial_bandwidth
    
    def update_bandwidth(self):
        # Simulate bandwidth changes between 1 and 10 Mbps
        self.bandwidth = random.randint(1, 10)
    
    def set_bandwidth(self, new_bw):
        self.bandwidth = new_bw
    
    def get_bandwidth(self):
        return self.bandwidth

class DRLAgent:
    def __init__(self, cpu_threshold=100, mem_threshold=400, reduce_to=5):
        self.cpu_threshold = cpu_threshold     # CPU threshold in 'm'
        self.mem_threshold = mem_threshold     # Memory threshold in 'Mi'
        self.reduce_to = reduce_to
    
    def decide_action(self, component_metrics):
        for metric in component_metrics:
            if metric["cpu"] > self.cpu_threshold or metric["memory"] > self.mem_threshold:
                return ('reduce_bandwidth', self.reduce_to)
        return ('no_action', None)

if __name__ == "__main__":
    ue_agent = UEAgent(initial_bandwidth=1)
    drl_agent = DRLAgent(cpu_threshold=100, mem_threshold=400, reduce_to=5)
    
    current_time = datetime.now()
    
    components = [
        "o-ran-ru",
        "o-ran-du",
        "o-ran-cu",
        "5gc-amf",
        "5gc-smf",
        "5gc-upf"
    ]

    # Open the log file in append mode
    with open("ue_traffic.log", "a") as f:
        while True:
            # 1. Update UE bandwidth
            ue_agent.update_bandwidth()
            current_bw = ue_agent.get_bandwidth()

            # 2. Compute CPU and memory usage based on bandwidth
            component_metrics = []
            for component in components:
                cpu_m = 30 + current_bw * random.randint(7, 12)
                memory_mi = 200 + current_bw * random.randint(25, 40)
                
                log_line = f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}, {component}, CPU(cores): {cpu_m}m, MEMORY(bytes): {memory_mi}Mi"
                print(log_line, flush=True)
                
                component_metrics.append({"component": component, "cpu": cpu_m, "memory": memory_mi})

            # 3. DRL decision
            action, value = drl_agent.decide_action(component_metrics)
            if action == 'reduce_bandwidth':
                ue_agent.set_bandwidth(value)
            
            # Print bandwidth info
            bw_log = f"> Generated Bandwidth from UE ={ue_agent.get_bandwidth()} Mbps, Send Instruction={action}"
            print(bw_log, flush=True)

            # Log the bandwidth to the file with timestamp
            f.write(f"{current_time.strftime('%Y-%m-%d %H:%M:%S')}, {ue_agent.get_bandwidth()}\n")
            f.flush()  # Ensure data is written

            # 5. Move time forward by 10 seconds
            current_time += timedelta(seconds=10)
            
            # 6. Sleep 10 seconds for real-time progression
            time.sleep(1)
