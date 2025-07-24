from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask
import threading
import random
import asyncio

# 🔧 Настройки
TOKEN = "7436013012:AAGDYHV2P8mDuruQIBQCRCqmxC-864bZr3Q"
MASTER_CHAT_ID = 5225197085

# 🫖 Цитаты дня (100 штук)
tea_quotes = [
    "🍵 Чай не решит всех проблем, но даст время подумать.",
    "🍃 Там, где чай, там и покой.",
    "☁️ Один глоток чая — и ты ближе к себе.",
    "🍵 Мудрость приходит с паром над чашей.",
    "🌿 Пуэр знает, чего ты боишься — и всё равно тебя любит.",
    "🔥 Чай варится медленно, как и понимание себя.",
    "🍂 Отшельник пьёт чай не для вкуса, а для присутствия.",
    "🌙 В темноте чай светлее мыслей.",
    "🪵 Нет спешки в чае, нет спешки в пути.",
    "💭 Когда нет слов — налей чай.",
] + [f"🍵 Чайная истина #{i}" for i in range(11, 101)]

app = Flask(__name__)
@app.route('/')
def home():
    return "Bot is alive!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🧘 О практике", "📅 Записаться"],
        ["🫖 Цитата дня от чайного пьяницы", "🤝 Поддержать проект"],
        ["💌 Оставить записку"]
    ]
    await update.message.reply_text(
        "🛠️ Добро пожаловать в пространство *«Гвозди и Листья»* 🍃\n\n"
        "🔩 Стояние на гвоздях\n🍵 Чайные церемонии\n💆 Банки\n🏕 Выездные практики\n\n👇 Выбери действие:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

async def practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 Пространство для тех, кто хочет вернуться к себе:\n\n"
        "🔩 Гвозди — практика внимания\n"
        "🍵 Чай — ритуал вкуса и тишины\n"
        "💆 Банки — телесное освобождение\n"
        "🗣 Душевные разговоры\n"
        "🏕 Церемонии под открытым небом"
    )

async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💚 Хочешь поддержать проект?\n\n"
        "📲 Перевод: *+7 912 852-81-81*\n"
        "_Сбербанк / Т-Банк_\n\nИли приходи на чайную церемонию 🐉",
        parse_mode="Markdown"
    )

async def quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(tea_quotes))

async def note_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💌 Оставь записку, и я передам её лично 🙏")
    return 1

async def receive_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    msg = f"📩 Записка от @{user.username or 'аноним'}:\n\n{update.message.text}"
    await context.bot.send_message(MASTER_CHAT_ID, msg)
    await update.message.reply_text("📬 Записка доставлена!")
    return -1

def main():
    threading.Thread(target=run_flask).start()
    app_ = ApplicationBuilder().token(TOKEN).build()

    app_.add_handler(CommandHandler("start", start))
    app_.add_handler(MessageHandler(filters.Regex("🧘 О практике"), practice))
    app_.add_handler(MessageHandler(filters.Regex("🤝 Поддержать проект"), support))
    app_.add_handler(MessageHandler(filters.Regex("🫖 Цитата дня от чайного пьяницы"), quote))

    from telegram.ext import ConversationHandler
    app_.add_handler(ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("💌 Оставить записку"), note_entry)],
        states={1: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_note)]},
        fallbacks=[]
    ))

    app_.run_polling()

if __name__ == "__main__":
    main()
