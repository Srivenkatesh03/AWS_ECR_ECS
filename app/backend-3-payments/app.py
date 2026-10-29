
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "payments",
        "message": "Hello from Payments Backend",
        "version": "v1"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/payments", methods=["GET"])
def get_payments():
    return jsonify({
        "payments": [
            {"id": 201, "amount": 499.00, "status": "completed"},
            {"id": 202, "amount": 1299.00, "status": "pending"}
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
