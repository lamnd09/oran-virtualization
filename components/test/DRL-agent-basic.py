from flask import Flask, request, jsonify

app = Flask(__name__)

# Define threshold
THRESHOLD = 0.3  # 30% threshold
INCREASE_FACTOR = 1.2  # Increase by 20% if below threshold
DECREASE_FACTOR = 0.8  # Decrease by 20% if above threshold

def adjust_ratio(data):
    """Applies a linear function to adjust the ratio based on the threshold."""
    adjusted_results = []
    for entry in data:
        ratio = entry.get("ratio", 0.0)  # Default to 0 if missing
        if ratio < THRESHOLD:
            new_ratio = ratio * INCREASE_FACTOR  # Increase if below threshold
            policy_action = "Increase UE ratio"
        else:
            new_ratio = ratio * DECREASE_FACTOR  # Decrease if above threshold
            policy_action = "Decrease UE ratio"

        adjusted_results.append({
            "original_ratio": ratio,
            "adjusted_ratio": round(new_ratio, 2),
            "policy_action": policy_action
        })
    
    return adjusted_results

@app.route("/process", methods=["POST"])
def process():
    """Endpoint to receive data and return adjusted ratios."""
    data = request.json
    adjusted_data = adjust_ratio(data)
    return jsonify(adjusted_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
