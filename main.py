import os, random
from flask import Flask, request
from telegram import Update, Bot, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

TOKEN = "7436013012:AAGDYHV2P8mDuruQIBQCRCqmxC-864bZr3Q"
MASTER_CHAT_ID = 5225197085
APP_URL = os.getenv("APP_URL")
if not APP_URL:
    raise RuntimeError("Укажи переменную APP_URL")

bot = Bot(TOKEN)
app = ApplicationBuilder().token(TOKEN).build()
flask_app = Flask(__name__)

tea_quotes = [
    # вставь сюда свои 100 фраз, добавил первые 10
    "🍵 Иногда чашка чая говорит больше, чем тысяча слов.",
    "🍃 Тишина между глотками — тоже часть церемонии.",
    "🌫️ Первый глоток — для тела. Второй — для духа.",
    "🍂 Чай не спешит. И ты — тоже.",
    "🐉 Пуэр не терпит суеты.",
    "🪷 Тишина — лучший собеседник за чай.",
    "🌕 Чай пьётся не для бодрости, а для ясности.",
    "🍂 Время для чая — это время для себя.",
    "🌬️ Вдох. Глоток. Выдох. Жизнь.",
    "🍃 Тепло в ладонях — уже медитация.",
    # ... добавь остальные до 100
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await bot.send_message(MASTER_CHAT_ID, f"👤 Новый пользователь: @{user.username or 'без ника'}")
    k = [
      ["🍵 Цитата дня от чайного пьяницы"],
      ["🤝 Поддержать проект"]
    ]
    await update.message.reply_text(
      "👋 Привет! Выбирай:",
      reply_markup=ReplyKeyboardMarkup(k, resize_keyboard=True)
    )
async def tea_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(tea_quotes))
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💚 Поддержка: +7 912 852‑81‑81")
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Нажми кнопку, пожалуйста 🙂")

@flask_app.route("/")
def home():
    return "Bot is working"
@flask_app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    app.process_update(update)
    return "OK"

if __name__ == "__main__":
    bot.delete_webhook()
    bot.set_webhook(f"{APP_URL}/webhook/{TOKEN}")
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("🍵 Цитата дня"), tea_quote))
    app.add_handler(MessageHandler(filters.Regex("🤝 Поддержать проект"), support))
    app.add_handler(MessageHandler(filters.TEXT, unknown))
    flask_app.run(host="0.0.0.0", port=8080)
