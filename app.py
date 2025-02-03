from flask import Flask, jsonify, request
from dto.models import Hello

app = Flask(__name__)


@app.route("/hello")
def hello_world():
    return jsonify({"status": "success", "data": Hello(id="123", content="world").dict()}), 200


if __name__ == "__main__":
    app.run()
