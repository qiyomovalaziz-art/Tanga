from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)

DATA_FILE = "database.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_user/<user_id>")
def get_user(user_id):
    data = load_data()
    user = data.get(user_id, {"balance": 0, "referrals": 0, "stars": 0})
    return jsonify(user)

@app.route("/update_balance", methods=["POST"])
def update_balance():
    data = load_data()
    info = request.get_json()
    user_id = info["user_id"]
    amount = info["amount"]

    if user_id not in data:
        data[user_id] = {"balance": 0, "referrals": 0, "stars": 0}

    data[user_id]["balance"] += amount
    save_data(data)
    return jsonify({"status": "success", "balance": data[user_id]["balance"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
