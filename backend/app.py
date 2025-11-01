from flask import Flask, jsonify, request, send_from_directory
from db import init_db, get_user, update_balance, add_referral, get_referrals, give_bonus
import os

# Flask app yaratamiz
app = Flask(__name__, static_folder="../web", static_url_path="/")

# 🔹 Statik sahifalar
@app.route('/')
def index():
    return send_from_directory('../web', 'index.html')

@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('../web', path)

# 🔹 API — foydalanuvchi ma'lumotlari
@app.route('/api/user/<int:user_id>', methods=['GET'])
def user_info(user_id):
    user = get_user(user_id)
    return jsonify(user)

# 🔹 API — yig‘ish
@app.route('/api/collect', methods=['POST'])
def collect():
    data = request.json
    user_id = data.get("user_id")
    add = 0.001
    new_balance = update_balance(user_id, add)
    return jsonify({"status": "ok", "added": add, "new_balance": new_balance})

# 🔹 API — bonus
@app.route('/api/bonus', methods=['POST'])
def bonus():
    data = request.json
    user_id = data.get("user_id")
    result = give_bonus(user_id)
    return jsonify(result)

# 🔹 API — referallar
@app.route('/api/referrals/<int:user_id>', methods=['GET'])
def referrals(user_id):
    refs = get_referrals(user_id)
    return jsonify(refs)

# 🔹 Dastur ishga tushirish
if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
