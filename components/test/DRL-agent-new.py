import numpy as np
from flask import Flask, request, jsonify
import torch
import torch.nn as nn
import torch.optim as optim

app = Flask(__name__)

# Define a simple DRL model using PyTorch
class DRLModel(nn.Module):
    def __init__(self):
        super(DRLModel, self).__init__()
        self.fc1 = nn.Linear(10, 32)  # Input size 10, hidden layer 32
        self.fc2 = nn.Linear(32, 16)
        self.fc3 = nn.Linear(16, 1)   # Output single adjusted ratio

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))  # Normalized output between 0 and 1
        return x

# Initialize model
model = DRLModel()
optimizer = optim.Adam(model.parameters(), lr=0.001)
criterion = nn.MSELoss()

# Function to process input data
def process_data(data):
    values = np.array([d["ratio"] for d in data])
    avg_ratio = np.mean(values)

    threshold = 0.3  # 30% threshold
    if avg_ratio < threshold:
        adjustment_factor = 1.2  # Increase ratio by 20%
    else:
        adjustment_factor = 0.8  # Decrease ratio by 20%

    adjusted_values = avg_ratio * adjustment_factor
    return adjusted_values

@app.route("/process", methods=["POST"])
def process():
    data = request.json
    adjusted_value = process_data(data)
    return jsonify({"adjusted_ratio": adjusted_value})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
