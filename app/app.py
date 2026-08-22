"""
Sample containerized application for LAB EX19 (CD with GitHub Actions + Docker).

A tiny Flask API with:
- GET /            -> welcome message + version (proves the container is alive)
- GET /health      -> health check (used by the deploy job's smoke test)
- GET /add/<a>/<b> -> trivial business logic (something for unit tests to exercise)

Kept deliberately small so the *pipeline* is the point of the exercise, not the app.
"""

from flask import Flask, jsonify
import os

app = Flask(__name__)

# Baked in at build time via --build-arg APP_VERSION=<git sha> (see Dockerfile
# and the GitHub Actions workflow) so you can see, at runtime, exactly which
# commit is currently deployed.
APP_VERSION = os.environ.get("APP_VERSION", "dev")


@app.route("/")
def index():
    return jsonify(
        message="Hello from the GitHub Actions CD Lab app!",
        version=APP_VERSION,
    )


@app.route("/health")
def health():
    return jsonify(status="ok"), 200


@app.route("/add/<int:a>/<int:b>")
def add(a: int, b: int):
    return jsonify(a=a, b=b, sum=a + b)


if __name__ == "__main__":
    # 0.0.0.0 so it's reachable from outside the container
    app.run(host="0.0.0.0", port=5000)
