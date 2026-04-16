import os, requests
from flask import Flask, request

app = Flask(__name__)
DB_URL = os.getenv("FIREBASE_URL")  # 需在 Vercel 設定環境變數

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json
    for event in data.get("events", []):
        if event["type"] == "message" and event["message"]["type"] == "text":
            # 將使用者回覆內容寫入 Firebase (REST PUT)
            requests.put(f"{DB_URL}/last_reply.json", json=event["message"]["text"])
    return "OK", 200

