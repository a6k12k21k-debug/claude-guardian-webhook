import os, requests, json
from flask import Flask, request

app = Flask(__name__)
DB_URL = os.getenv("FIREBASE_URL")
DB_SECRET = os.getenv("FIREBASE_SECRET")

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    app.logger.info(f"Received: {json.dumps(data)[:200]}")
    app.logger.info(f"DB_URL={DB_URL}, SECRET_LEN={len(DB_SECRET) if DB_SECRET else 0}")
    for event in data.get("events", []):
        if event["type"] == "message" and event["message"]["type"] == "text":
            text = event["message"]["text"]
            url = f"{DB_URL}/last_reply.json?auth={DB_SECRET}"
            try:
                r = requests.put(url, json=text)
                app.logger.info(f"Firebase PUT {r.status_code}: {r.text[:100]}")
            except Exception as e:
                app.logger.error(f"Firebase PUT failed: {e}")
    return "OK", 200

@app.route("/", methods=["GET"])
def health():
    return f"OK DB_URL={'SET' if DB_URL else 'MISSING'} SECRET={'SET' if DB_SECRET else 'MISSING'}", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

