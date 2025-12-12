from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def index():
    return {
        "message": "Hello from ECS Fargate!",
        "version": os.environ.get("APP_VERSION", "v1")
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
