import json
import requests

def aggregate_and_forward_logs(log_file='oran_logs.json'):
    with open(log_file, 'r') as f:
        logs = json.load(f)

    sensitive_ratio = logs['sensitive_requests'] / logs['total_requests']
    metrics_data = {
        "timestamp": logs['timestamp'],
        "total_requests": logs['total_requests'],
        "sensitive_requests": logs['sensitive_requests'],
        "sensitive_ratio": sensitive_ratio
    }

    print(f"Aggregated Metrics: {metrics_data}")

    response = requests.post(
        'http://localhost:5000/evaluate_risk',
        json={"metrics_data": metrics_data}
    )

    drl_response = response.json()
    print(f"DRL Agent Response: {drl_response}")

    # Save DRL response for simulated agent
    with open('drl_decision.json', 'w') as f:
        json.dump(drl_response, f)

if __name__ == "__main__":
    aggregate_and_forward_logs()
