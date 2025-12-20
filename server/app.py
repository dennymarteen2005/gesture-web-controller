from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

latest_gesture = "NONE"

@app.route("/gesture", methods=["POST"])
def receive_gesture():
    global latest_gesture
    data = request.json
    latest_gesture = data.get("gesture", "NONE")
    return jsonify({"status": "ok"})

@app.route("/gesture", methods=["GET"])
def send_gesture():
    global latest_gesture
    gesture_to_send = latest_gesture
    latest_gesture = "NONE"   # 🔥 RESET after sending
    return jsonify({"gesture": gesture_to_send})

if __name__ == "__main__":
    app.run(port=5000)
