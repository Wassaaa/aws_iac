from flask import Flask, jsonify
import datetime

# 1. Create the Flask app instance
app = Flask(__name__)

# 2. Define the main route
@app.route('/')
def hello():
    """Provides a simple JSON response."""
    return jsonify(
        message="Hello from my Fargate container!",
        timestamp=datetime.datetime.now().isoformat()
    )

# 3. Define the health check route
@app.route('/health')
def health_check():
    """A simple health check endpoint for the load balancer."""
    return jsonify(status="ok"), 200

if __name__ == '__main__':
    # listening on all IPs (0.0.0.0) on port 8080
    app.run(host='0.0.0.0', port=8080)
