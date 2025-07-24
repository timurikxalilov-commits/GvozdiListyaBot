from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)
import asyncio
import random

# 🔧 Настройки
TOKEN = "7436013012:AAGDYHV2P8mDuruQIBQCRCqmxC-864bZr3Q"
MASTER_CHAT_ID = 5225197085

# 📜 Цитаты
QUOTES = [
    "🍵 Чай — это вода, которая помнит.",
    "🌿 Каждая заварка — как новая жизнь.",
    "☁️ Завари чай, успокой ветер в голове.",
    "🪷 Слушай, как молчит чай.",
    "🔥 Кипяток лечит спешку.",
    "🫖 Время с чаем идёт иначе.",
    "🍃 Даже один глоток может быть церемонией.",
    "🐉 Пуэр хранит истории пещер.",
    "🧘 Кто пьёт чай — не спешит.",
    "💭 Мудрость уходит в осадок, как чайные листья.",
    # добавь ещё 90 — если хочешь, могу скинуть весь список
]

# Состояния
NAME, DATE, PLACE, COMMENTS, PHONE = range(5)

# --- Команды
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🧘 О практике", "📅 Записаться"],
        ["🍵 Цитата дня от чайного пьяницы"],
        ["🤝 Поддержать проект", "✉️ Оставить записку"]
    ]
    await update.message.reply_text(
        "🍃 Добро пожаловать в пространство *Гвозди и Листья*.\n\n"
        "🔩 Гвозди\n🍵 Чай\n💆 Банки\n🏕 Выезды\n\n"
        "👇 Выбери действие:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True),
        parse_mode="Markdown"
    )

async def practice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🌿 Здесь мы:\n"
        "🔩 стоим на гвоздях\n"
        "🍵 пьем чай (пуэры, улуны, Да Хун Пао)\n"
        "💆 ставим банки\n"
        "🏕 выезжаем в леса\n"
        "💬 просто говорим по душам"
    )

# --- Заявка
async def sign_up(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Как тебя зовут?")
    return NAME

async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["name"] = update.message.text
    await update.message.reply_text("Когда тебе удобно?")
    return DATE

async def get_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["date"] = update.message.text
    await update.message.reply_text("Где хочешь провести практику?")
    return PLACE

async def get_place(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["place"] = update.message.text
    await update.message.reply_text("Есть пожелания?")
    return COMMENTS

async def get_comments(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["comments"] = update.message.text
    await update.message.reply_text("Оставь номер телефона 📱")
    return PHONE

async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["phone"] = update.message.text
    user = update.message.from_user

    text = (
        f"📥 *Новая заявка:*\n"
        f"👤 Имя: {context.user_data['name']}\n"
        f"📅 Время: {context.user_data['date']}\n"
        f"📍 Место: {context.user_data['place']}\n"
        f"💬 Комментарии: {context.user_data['comments']}\n"
        f"📱 Телефон: {context.user_data['phone']}\n"
        f"Telegram: @{user.username or 'нет'}"
    )

    await context.bot.send_message(chat_id=MASTER_CHAT_ID, text=text, parse_mode="Markdown")
    await update.message.reply_text("Заявка отправлена 🙌")
    return ConversationHandler.END

# --- Цитата
async def send_quote(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(random.choice(QUOTES))

# --- Поддержка
async def support(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💚 Хочешь поддержать проект?\n\n"
        "📲 Перевод на номер: *+7 912 852-81-81*\n"
        "_Сбербанк / Т-Банк_\n\n"
        "Или приходи на чай 🐉",
        parse_mode="Markdown"
    )

# --- Связь
async def note_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Оставь записку, и я получу её лично 🙏")
    return PHONE

async def receive_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    await context.bot.send_message(
        MASTER_CHAT_ID,
        f"📩 Записка от @{user.username or 'аноним'}:\n\n{update.message.text}"
    )
    await update.message.reply_text("Спасибо, передано 🙏")
    return ConversationHandler.END

# --- Неизвестная команда
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Не понял тебя 🙃 Нажми кнопку ниже!")

# ▶️ MAIN
async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    # Заявка
    sign_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("📅 Записаться"), sign_up)],
        states={
            NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
            DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_date)],
            PLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_place)],
            COMMENTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_comments)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone)],
        },
        fallbacks=[]
    )

    # Записка
    note_conv = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("✉️ Оставить записку"), note_entry)],
        states={PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_note)]},
        fallbacks=[]
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(sign_conv)
    app.add_handler(note_conv)
    app.add_handler(MessageHandler(filters.Regex("🧘 О практике"), practice))
    app.add_handler(MessageHandler(filters.Regex("🤝 Поддержать проект"), support))
    app.add_handler(MessageHandler(filters.Regex("🍵 Цитата дня от чайного пьяницы"), send_quote))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    app.add_handler(MessageHandler(filters.TEXT, unknown))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
