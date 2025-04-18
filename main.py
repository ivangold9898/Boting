
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

admin_id = 7854869964
TELEGRAM_BOT_TOKEN = "8152113854:AAH3-eOegBASZDrSo3Mz1sj2jpBgI15uTis"

# Збереження користувача
def save_user(user_id):
    with open("users.txt", "a") as f:
        if str(user_id) not in open("users.txt").read():
            f.write(f"{user_id}\n")

# Команда старт
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)
    keyboard = [["Баланс", "Мій гаманець"], ["Налаштування", "Почати снайпінг"], ["Вивести", "Промокод"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Вітаю в Solana Sniper Bot!", reply_markup=markup)

# Розсилка
async def broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != admin_id:
        return await update.message.reply_text("У тебе немає доступу.")
    await update.message.reply_text("Введи текст для розсилки:")
    context.user_data["broadcast"] = True

# Обробка текстових повідомлень
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    save_user(user_id)

    if context.user_data.get("broadcast"):
        context.user_data["broadcast"] = False
        text = update.message.text

        with open("users.txt") as f:
            user_ids = [line.strip() for line in f.readlines()]

        success = 0
        for uid in user_ids:
            try:
                await context.bot.send_message(chat_id=int(uid), text=text)
                success += 1
            except:
                pass
        await update.message.reply_text(f"Розіслано {success} користувачам.")
        return

    await update.message.reply_text("Функціонал у розробці.")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
