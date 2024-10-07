import subprocess
import sys
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# دالة لتحميل المكتبة إذا لم تكن مثبتة
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# محاولة استيراد المكتبات وتحميلها إذا لم تكن مثبتة
try:
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, CallbackContext
except ImportError:
    print("تثبيت المكتبات المطلوبة...")
    install("python-telegram-bot==13.7")
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, CallbackContext

# إعداد التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توكن البوت
TOKEN = "7482908901:AAHLJbvx6NBCsaukcRLIYcFTQlQFclQEqYc"

# دالة لإرسال الساعة كل دقيقة
def send_time(context: CallbackContext) -> None:
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    context.bot.send_message(chat_id=context.job.context, text=f"الساعة الآن: {current_time}")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('تم بدء البوت!')

    # بدء جدولة إرسال الوقت كل دقيقة
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(send_time, interval=60, first=0, context=chat_id)

def main() -> None:
    # إعداد المراقب
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # إضافة معالج الأمر /start
    dispatcher.add_handler(CommandHandler("start", start))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
