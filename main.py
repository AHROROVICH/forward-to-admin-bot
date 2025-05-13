import telebot
import os
from flask import Flask, request

# Muhit o'zgaruvchilari orqali token va admin ID olinadi
BOT_TOKEN = os.environ.get("BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID"))
RENDER_EXTERNAL_URL = os.environ.get("RENDER_EXTERNAL_URL")  # render.com URL

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# /start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Xush kelibsiz! Har bir xabaringiz admin foydalanuvchiga yuboriladi.")

# Barcha xabarlarni adminga forward qilish
@bot.message_handler(func=lambda message: True)
def forward_to_admin(message):
    try:
        bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    except Exception as e:
        print(f"Xatolik: {e}")

# Telegram webhook'dan kelgan xabarni qabul qilish
@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.stream.read().decode("utf-8")
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "OK", 200

# Render birinchi kirganda webhookni sozlaydi
@app.route("/")
def webhook_setup():
    webhook_url = f"https://{RENDER_EXTERNAL_URL}/{BOT_TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)
    return f"Webhook o‘rnatildi: {webhook_url}", 200

# Flask ilovasini ishga tushirish
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

