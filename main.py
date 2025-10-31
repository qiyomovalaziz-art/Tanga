import telebot
import json

BOT_TOKEN = "8493429830:AAE21OTeGn7uFmY0uwU-7olzRUAOANIVsQs"
bot = telebot.TeleBot(BOT_TOKEN)

# Oddiy bazani yuklash/saqlash
def load_data():
    try:
        with open("database.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_data(data):
    with open("database.json", "w") as f:
        json.dump(data, f, indent=2)

@bot.message_handler(commands=['start'])
def start(message):
    data = load_data()
    user_id = str(message.from_user.id)

    if user_id not in data:
        data[user_id] = {"balance": 0, "referrals": 0}
        save_data(data)

    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(
        telebot.types.InlineKeyboardButton(
            "🪙 Ilovaga kirish",
            web_app=telebot.types.WebAppInfo(url="https://web-production-57765.up.railway.app/")
        )
    )

    bot.send_message(message.chat.id,
        "👋 Salom! 'Tanga' mini ilovasiga xush kelibsiz!\n"
        "👇 Quyidagi tugma orqali kirish mumkin:",
        reply_markup=markup
    )

bot.polling(non_stop=True)
