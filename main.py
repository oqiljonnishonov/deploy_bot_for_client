from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ConversationHandler, CallbackContext

# Bu yerda BotFather'dan olingan tokenni joylashtiring
TOKEN = '7362625475:AAESRFyIYdxGVfvk7gwdJjWg-k2Z9NgpQlA'
ADMIN_CHAT_ID = 6280619594  # Asosiy administratorning Telegram ID'si
SECOND_ADMIN_CHAT_ID = 6050258183  # Yangi administratorning Telegram ID'si

# Holatlar
FIO, PHONE, PHOTOS, LOCATION, VIDEO, BIO = range(6)

# /start buyrug'iga javob beradigan funksiya
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Assalomu alaykum!\n\nF.I.O ni to'liq yozib qoldiring:")
    return FIO

# F.I.O ni qabul qiladigan funksiya
async def fio(update: Update, context: CallbackContext) -> int:
    context.user_data['fio'] = update.message.text
    await update.message.reply_text("Telefon raqamingizni jonating:")
    return PHONE

# Telefon raqamini qabul qiladigan funksiya
async def phone(update: Update, context: CallbackContext) -> int:
    context.user_data['phone'] = update.message.text
    await update.message.reply_text("4 dona rasm yuboring:")
    return PHOTOS

# Rasm qabul qiladigan funksiya
async def photos(update: Update, context: CallbackContext) -> int:
    photos = context.user_data.get('photos', [])
    photos.append(update.message.photo[-1].file_id)
    context.user_data['photos'] = photos
    if len(photos) < 4:
        await update.message.reply_text(f"{4 - len(photos)} ta rasm yuboring:")
        return PHOTOS
    else:
        await update.message.reply_text("Yashash manzilingizni yuboring(lokatsiya):")
        return LOCATION

# Manzilni qabul qiladigan funksiya
async def location(update: Update, context: CallbackContext) -> int:
    context.user_data['location'] = update.message.location
    await update.message.reply_text("Ijodiy qobilyatingiz haqida qisqacha video (minimum 15 sekund) yuboring:")
    return VIDEO

# Videoni qabul qiladigan funksiya
async def video(update: Update, context: CallbackContext) -> int:
    context.user_data['video'] = update.message.video.file_id
    await update.message.reply_text("Tarjimai holingizni qisqacha yozib yuboring:")
    return BIO

# Tarjimai holni qabul qiladigan funksiya
async def bio(update: Update, context: CallbackContext) -> int:
    context.user_data['bio'] = update.message.text
    await update.message.reply_text("Siz bilan tez orada bog'lanamiz.")

    # Yig'ilgan ma'lumotlarni ko'rish uchun
    user_data = context.user_data
    message = (
        "Foydalanuvchidan olingan ma'lumotlar:\n"
        f"FIO: {user_data['fio']}\n"
        f"Telefon: {user_data['phone']}\n"
        f"Rasmlar: {user_data['photos']}\n"
        f"Manzil: {user_data['location']}\n"
        f"Video: {user_data['video']}\n"
        f"Tarjimai hol: {user_data['bio']}"
    )

    # Ma'lumotlarni administratorlarga yuborish
    for admin_id in [ADMIN_CHAT_ID, SECOND_ADMIN_CHAT_ID]:
        await context.bot.send_message(chat_id=admin_id, text=message)

        # Rasmlarni yuborish
        for photo in user_data['photos']:
            await context.bot.send_photo(chat_id=admin_id, photo=photo)

        # Videoni yuborish
        await context.bot.send_video(chat_id=admin_id, video=user_data['video'])

    return ConversationHandler.END

# Bekor qiluvchi funksiya
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("Amal bekor qilindi.")
    return ConversationHandler.END

# Asosiy bot funksiyasini yaratish
def main() -> None:
    # ApplicationBuilder obyekti orqali botni ishga tushirish
    application = Application.builder().token(TOKEN).build()

    # Conversation handler yaratish
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, fio)],
            PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, phone)],
            PHOTOS: [MessageHandler(filters.PHOTO & ~filters.COMMAND, photos)],
            LOCATION: [MessageHandler(filters.LOCATION & ~filters.COMMAND, location)],
            VIDEO: [MessageHandler(filters.VIDEO & ~filters.COMMAND, video)],
            BIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, bio)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    # Dispatcherga handlerni qo'shish
    application.add_handler(conv_handler)

    # Botni ishga tushirish
    application.run_polling()


if __name__ == '__main__':
    main()
