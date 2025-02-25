## API to DRL to Shao

The Centralized Logging Agent exposes an API endpoint to accept sensitive ratio data. An example JSON payload and API call are provided below:

```plaintext
oran-project/
├── server.py              # Your Flask API server
├── drl_agent.py           # Module containing the DRL core logic
├── requirements.txt
└── README.md

```

### JSON Data Template

```json
`{
  "timestamp": "2025-02-16T15:00:00Z",
  "total_requests": 1000,
  "sensitive_requests": 300,
  "sensitive_ratio": 0.3
}`
```

### Example API Call Using `curl`:

```bash
curl -X POST http://<centralized-logging-agent-ip>/api/sensitive-data \
     -H "Content-Type: application/json" \
     -d '{
           "timestamp": "2025-02-26T15:00:00Z",
           "total_requests": 1000,
           "sensitive_requests": 300,
           "sensitive_ratio": 0.3
         }'

```

expected response: 

```json
{
  "status": "success",
  "message": "Data received successfully.",
  "adjusted_ratio": 0.3
}

```

### How to run it?

Start the flask server:

```bash
python server.py
```

By default, the server will run in debug mode on 0.0.0.0 at port 5000.

* The API server listens for POST requests at the /api/sensitive-data endpoint.
* The DRL agent is integrated into the server code and processes the incoming sensitive_ratio value.
* On receiving a valid JSON payload, the API prints the original data, computes the adjusted ratio, and returns the response.

### Your main function: 

```python
# drl_agent.py
import numpy as np

class DRLAgent:
    def __init__(self, threshold=0.3, k=0.5):
        self.threshold = threshold
        self.k = k
        # Initialize additional DRL parameters or model here
  
    def deep_rl_function(self, ratio): # Shao - Update your code here
        """
        Adjusts the sensitive ratio using DRL logic.
        For now, it applies a simple linear reduction if the ratio exceeds the threshold.
        """
        if ratio > self.threshold:
            adjusted = ratio - self.k * (ratio - self.threshold)
        else:
            adjusted = ratio
        return adjusted

# Example usage
if __name__ == "__main__":
    agent = DRLAgent()
    sample_ratio = 0.4
    print("Adjusted Ratio:", agent.deep_rl_function(sample_ratio))

```
