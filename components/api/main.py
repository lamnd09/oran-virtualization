from fastapi import FastAPI
from typing import Optional
from pymongo import MongoClient
import os
from datetime import datetime

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://mongo:27017")
DB_NAME = os.environ.get("DB_NAME", "oran_db")
COLLECTION_NAME = os.environ.get("COLLECTION_NAME", "metrics")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

app = FastAPI()

@app.get("/metrics")
def get_metrics(start: Optional[str] = None, end: Optional[str] = None):
    query = {}
    if start:
        start_dt = datetime.fromisoformat(start)
        query["timestamp"] = {"$gte": start_dt}
    if end:
        end_dt = datetime.fromisoformat(end)
        if "timestamp" in query:
            query["timestamp"]["$lte"] = end_dt
        else:
            query["timestamp"] = {"$lte": end_dt}

    data = list(collection.find(query, {"_id": 0}).sort("timestamp", 1))
    return data

@app.get("/latest_bandwidth")
def latest_bandwidth():
    doc = collection.find_one(sort=[("timestamp", -1)], projection={"_id": 0, "ue_bandwidth": 1, "timestamp": 1})
    return doc if doc else {}
