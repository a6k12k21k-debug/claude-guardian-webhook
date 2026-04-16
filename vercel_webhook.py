import os, requests, json
from flask import Flask, request

app = Flask(__name__)
DB_URL = os.getenv("FIREBASE_URL")
DB_SECRET = os.getenv("FIREBASE_SECRET")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    for event in data.get("events", []):
        if event["type"] == "message" and event["message"]["type"] == "text":
            url = f"{DB_URL}/last_reply.json?auth={DB_SECRET}"
            requests.put(url, json=event["message"]["text"])
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

