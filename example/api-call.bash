curl -X POST http://<centralized-logging-agent-ip>/api/sensitive-data \
     -H "Content-Type: application/json" \
     -d '{
           "timestamp": "2025-02-21T15:00:00Z",
           "total_requests": 1000,
           "sensitive_requests": 300,
           "sensitive_ratio": 0.3
         }'
