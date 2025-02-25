# server.py
from flask import Flask, request, jsonify
from drl_agent import DRLAgent

app = Flask(__name__)
drl_agent = DRLAgent()

@app.route('/api/sensitive-data', methods=['POST'])
def sensitive_data():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON payload received"}), 400

    # Process the data (e.g., logging, storage)
    print("Received data:", data)
    
    # Example: Adjust the sensitive ratio using the DRL agent
    original_ratio = data.get("sensitive_ratio")
    adjusted_ratio = drl_agent.deep_rl_function(original_ratio)
    print(f"Original Ratio: {original_ratio}, Adjusted Ratio: {adjusted_ratio}")

    return jsonify({
        "status": "success",
        "message": "Data received successfully.",
        "adjusted_ratio": adjusted_ratio
    }), 200

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
