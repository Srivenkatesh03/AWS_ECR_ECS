
from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "service": "users",
        "message": "Hello from Users Backend",
        "version": "v1"
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


@app.route("/api/users", methods=["GET"])
def get_users():
    return jsonify({
        "users": [
            {"id": 1, "name": "User One"},
            {"id": 2, "name": "User Two"}
        ]
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
