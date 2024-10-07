import subprocess
import sys

# دالة لتحميل المكتبة إذا لم تكن مثبتة
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# محاولة استيراد المكتبات وتحميلها إذا لم تكن مثبتة
try:
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
except ImportError:
    print("تثبيت المكتبات المطلوبة...")
    install("python-telegram-bot==13.7")
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import logging

# إعداد التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توكن البوت
TOKEN = "8165660765:AAGF2-ZltZZy-V_nSWwx_frCxXOtBAYeq24"

# الاسم والصورة الأصلية
ORIGINAL_TITLE = "اسم المجموعة الأصلي"  # قم بتغيير هذا إلى الاسم الأصلي
ORIGINAL_PHOTO_ID = None  # هنا يمكنك وضع معرف الصورة الأصلية إذا كان لديك

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحبًا! أنا هنا لحماية المجموعة.')

def check_group_title(update: Update, context: CallbackContext) -> None:
    if update.message.chat.title != ORIGINAL_TITLE:
        # إعادة تعيين الاسم
        context.bot.set_chat_title(chat_id=update.message.chat.id, title=ORIGINAL_TITLE)
        logging.info(f'تم إعادة تعيين الاسم إلى {ORIGINAL_TITLE}')

def check_group_photo(update: Update, context: CallbackContext) -> None:
    # تحقق من الصورة إذا كانت غير متاحة، سيتم وضعها
    if ORIGINAL_PHOTO_ID is not None and update.message.chat.photo is not None:
        if update.message.chat.photo[-1].file_id != ORIGINAL_PHOTO_ID:
            context.bot.set_chat_photo(chat_id=update.message.chat.id, photo=ORIGINAL_PHOTO_ID)
            logging.info('تم إعادة تعيين الصورة.')

def main() -> None:
    # إعداد المراقب
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # الأوامر والمراقبة
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.status_update, check_group_title))
    dispatcher.add_handler(MessageHandler(Filters.status_update, check_group_photo))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
