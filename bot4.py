import subprocess
import sys
import logging
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# دالة لتحميل المكتبة إذا لم تكن مثبتة
def install(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

# محاولة استيراد المكتبات وتحميلها إذا لم تكن مثبتة
try:
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
    from apscheduler.schedulers.background import BackgroundScheduler
except ImportError:
    print("تثبيت المكتبات المطلوبة...")
    install("python-telegram-bot==13.7")
    install("apscheduler")
    from telegram import Update
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
    from apscheduler.schedulers.background import BackgroundScheduler

# إعداد التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توكن البوت
TOKEN = "7713971167:AAEIrDPo4SvXrqf60LTd7Rgjzslx2fEJUgw"

# دالة لإرسال الرسائل في الأوقات المحددة
def send_messages(context: CallbackContext) -> None:
    current_time = datetime.now().strftime("%H:%M")
    chat_id = context.job.context  # الحصول على معرف الدردشة

    if current_time == "05:00":
        context.bot.send_message(chat_id=chat_id, text="تقبل الله صلاتكم")
    elif current_time == "07:00":
        context.bot.send_message(chat_id=chat_id, text="صباح الخير للجميع")
    elif current_time == "08:00":
        context.bot.send_message(chat_id=chat_id, text="روح تقرا 🙂")
    elif current_time == "13:00":
        context.bot.send_message(chat_id=chat_id, text="مساء الخير للجميع")
    elif current_time == "20:00":
        context.bot.send_message(chat_id=chat_id, text="تصبحون على خير")

# دالة الترحيب بالعضو الجديد
def welcome(update: Update, context: CallbackContext) -> None:
    for member in update.message.new_chat_members:
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"مرحبًا بك في المجموعة، {member.full_name}!")

# دالة الرد على "السلام عليكم"
def reply_salam(update: Update, context: CallbackContext) -> None:
    if "السلام عليكم" in update.message.text:
        context.bot.send_message(chat_id=update.effective_chat.id, text="وعليكم السلام ورحمة الله تعالى وبركاته")

# دالة الرد على كلمة "بوت"
def respond_to_bot(update: Update, context: CallbackContext) -> None:
    responses = [
        "أنا هنا لمساعدتك!",
        "كيف يمكنني مساعدتك اليوم؟",
        "هل تحتاج إلى شيء خاص؟",
        "لا تتردد في سؤالي!",
        "كيف تسير الأمور؟"
    ]
    context.bot.send_message(chat_id=update.effective_chat.id, text=random.choice(responses))

# دالة الرد على النقطة
def reply_dot(update: Update, context: CallbackContext) -> None:
    if update.message.text == ".":
        context.bot.send_message(chat_id=update.effective_chat.id, text="@a_4pa")

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحبًا! سأبدأ بإرسال الرسائل في الأوقات المحددة.')
    
    # بدء جدولة الرسائل
    chat_id = update.message.chat_id
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_messages, 'interval', minutes=1, args=[context], id=str(chat_id))
    scheduler.start()

def main() -> None:
    # إعداد المراقب
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # الأوامر والمراقبة
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, welcome))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, reply_salam))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'\bبوت\b'), respond_to_bot))
    dispatcher.add_handler(MessageHandler(Filters.text & Filters.regex(r'^\.$'), reply_dot))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
