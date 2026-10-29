
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "orders",
        "message": "Hello from Orders Backend",
        "version": "v1"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/orders", methods=["GET"])
def get_orders():
    return jsonify({
        "orders": [
            {"id": 101, "item": "Laptop", "status": "processing"},
            {"id": 102, "item": "Keyboard", "status": "shipped"}
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
