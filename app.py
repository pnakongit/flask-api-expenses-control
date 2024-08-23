from flask import Flask, jsonify, Response

app = Flask(__name__)


@app.route("/", methods=["GET", ])
def index() -> (Response, int):
    return jsonify({"message": "Hello World!"}), 200


if __name__ == "__main__":
    app.run(debug=True)
