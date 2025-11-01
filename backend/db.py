import sqlite3, time

DB_NAME = "database.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0,
            bonus_time INTEGER DEFAULT 0,
            referrals INTEGER DEFAULT 0
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS referral_links (
            inviter_id INTEGER,
            invited_id INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cur.fetchone()
    if not user:
        cur.execute("INSERT INTO users (id, balance, bonus_time, referrals) VALUES (?,0,0,0)", (user_id,))
        conn.commit()
        user = (user_id, 0, 0, 0)
    conn.close()
    return {"id": user[0], "balance": user[1], "bonus_time": user[2], "referrals": user[3]}

def update_balance(user_id, amount):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE users SET balance = balance + ? WHERE id=?", (amount, user_id))
    conn.commit()
    cur.execute("SELECT balance FROM users WHERE id=?", (user_id,))
    balance = cur.fetchone()[0]
    conn.close()
    return balance

def add_referral(inviter_id, invited_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("INSERT INTO referral_links VALUES (?,?)", (inviter_id, invited_id))
    cur.execute("UPDATE users SET referrals = referrals + 1 WHERE id=?", (inviter_id,))
    conn.commit()
    conn.close()

def get_referrals(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT invited_id FROM referral_links WHERE inviter_id=?", (user_id,))
    rows = cur.fetchall()
    conn.close()
    return {"referrals": len(rows), "list": [r[0] for r in rows]}

def give_bonus(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT bonus_time FROM users WHERE id=?", (user_id,))
    last_bonus = cur.fetchone()[0]
    now = int(time.time())
    if now - last_bonus < 86400:
        return {"status": "wait", "message": "Bonus hali olinmagan, keyinroq urinib ko‘ring."}
    cur.execute("UPDATE users SET balance = balance + 0.01, bonus_time=? WHERE id=?", (now, user_id))
    conn.commit()
    conn.close()
    return {"status": "ok", "message": "🎁 Bonus muvaffaqiyatli qo‘shildi! +0.01 ₽"}
