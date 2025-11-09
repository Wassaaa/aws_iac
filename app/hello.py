from flask import Flask, jsonify, request, send_file
import subprocess
import os

# 1. Create the Flask app instance
app = Flask(__name__)

# Path to the compiled probit binary
PROBIT_BINARY = "/app/probit_api"


# 2. Serve the frontend
@app.route("/")
def index():
    """Serve the frontend HTML page."""
    return send_file("index.html")


# 3. API endpoint for inverse normal calculation
@app.route("/api/probit", methods=["POST"])
def calculate_probit():
    """
    Calculate the inverse cumulative normal (z-score) for a given probability.

    Input (JSON): {"probability": 95.0}  (percentage from 0-100)
    Output (JSON): {"probability": 95.0, "z_score": 1.6448536269514722}
    """
    try:
        data = request.get_json()

        if not data or "probability" not in data:
            return jsonify({"error": "Missing probability field"}), 400

        probability = float(data["probability"])

        # Validate range
        if probability <= 0.0 or probability >= 100.0:
            return (
                jsonify({"error": "Probability must be between 0 and 100 (exclusive)"}),
                400,
            )

        # Call the C++ binary
        result = subprocess.run(
            [PROBIT_BINARY, str(probability)],
            capture_output=True,
            text=True,
            timeout=1.0,
        )

        if result.returncode != 0:
            return (
                jsonify({"error": "Calculation failed", "details": result.stderr}),
                500,
            )

        z_score = float(result.stdout.strip())

        return jsonify({"probability": probability, "z_score": z_score})

    except ValueError as e:
        return jsonify({"error": "Invalid probability value"}), 400
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Calculation timeout"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 4. Health check endpoint
@app.route("/health")
def health_check():
    """A simple health check endpoint for the load balancer."""
    # Check if probit binary exists
    binary_exists = os.path.exists(PROBIT_BINARY)

    if binary_exists:
        return jsonify(status="ok", probit_binary="available"), 200
    else:
        return jsonify(status="degraded", probit_binary="missing"), 503


if __name__ == "__main__":
    # listening on all IPs (0.0.0.0) on port 8080
    app.run(host="0.0.0.0", port=8080)
