import json
import random
import time

def generate_logs(total_requests=1000, sensitive_ratio=0.3):
    sensitive_requests = int(total_requests * sensitive_ratio)
    logs = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_requests": total_requests,
        "sensitive_requests": sensitive_requests,
    }

    with open('oran_logs.json', 'w') as f:
        json.dump(logs, f)

    print(f"Generated ORAN logs: {logs}")

if __name__ == "__main__":
    generate_logs()
