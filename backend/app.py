from flask import Flask, jsonify, request, send_from_directory
from db import init_db, get_user, update_balance, add_referral, get_referrals, give_bonus
import os

# Flask ilovasini yaratamiz
app = Flask(__name__, static_folder="../web", static_url_path="/")

# 🔹 Asosiy sahifa
@app.route('/')
def index():
    return send_from_directory('../web', 'index.html')

# 🔹 Statik fayllarni (HTML, CSS, JS) xizmat qilish
@app.route('/<path:path>')
def serve_file(path):
    return send_from_directory('../web', path)

# 🔹 API — foydalanuvchi ma'lumotlari
@app.route('/api/user/<int:user_id>', methods=['GET'])
def user_info(user_id):
    user = get_user(user_id)
    if user:
        return jsonify(user)
    else:
        return jsonify({"error": "Foydalanuvchi topilmadi"}), 404

# 🔹 API — yig‘ish funksiyasi
@app.route('/api/collect', methods=['POST'])
def collect():
    data = request.json
    user_id = data.get("user_id")
    add = 0.001  # har safar yig‘ilganda qo‘shiladigan miqdor
    new_balance = update_balance(user_id, add)
    return jsonify({"status": "ok", "added": add, "new_balance": new_balance})

# 🔹 API — bonus olish
@app.route('/api/bonus', methods=['POST'])
def bonus():
    data = request.json
    user_id = data.get("user_id")
    result = give_bonus(user_id)
    return jsonify(result)

# 🔹 API — referallarni olish
@app.route('/api/referrals/<int:user_id>', methods=['GET'])
def referrals(user_id):
    refs = get_referrals(user_id)
    return jsonify(refs)

# 🔹 Serverni ishga tushirish
if __name__ == '__main__':
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
