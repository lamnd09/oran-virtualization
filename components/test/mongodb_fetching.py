from pymongo import MongoClient
import requests
import json

# MongoDB connection settings
MONGO_URI = "mongodb://admin:password@centralized-logging-mongodb:27017/"
DATABASE_NAME = "logging_db"
COLLECTION_NAME = "logs"

# DRL agent API endpoint
DRL_AGENT_URL = "http://drl-agent:5001/process"

def fetch_data_from_mongodb():
    """Fetch data from MongoDB."""
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]

    # Fetch latest log data
    logs = list(collection.find().sort("_id", -1).limit(10))

    # Convert BSON to JSON
    json_logs = []
    for log in logs:
        log["_id"] = str(log["_id"])  # Convert ObjectId to string
        json_logs.append(log)

    client.close()
    return json_logs

def send_data_to_drl(json_data):
    """Send JSON data to DRL-agent for processing."""
    response = requests.post(DRL_AGENT_URL, json=json_data)
    return response.json()

if __name__ == "__main__":
    log_data = fetch_data_from_mongodb()
    drl_response = send_data_to_drl(log_data)
    print("DRL Agent Response:", drl_response)
