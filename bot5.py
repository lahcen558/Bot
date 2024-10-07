import subprocess
import sys
import logging
import random
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from apscheduler.schedulers.background import BackgroundScheduler

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
TOKEN = "7099498570:AAGWaoQ1Ml7NCwQrEnzVjsKXKUn083YeIlw"

# دالة لإرسال /start كل 10 ثواني
def send_start(context: CallbackContext) -> None:
    context.bot.send_message(chat_id=context.job.context, text="/start")

# دالة لتغيير اسم المجموعة كل دقيقة
def change_group_name(context: CallbackContext) -> None:
    chat_id = context.job.context
    new_name = f"اسم المجموعة {random.randint(1, 1000)}"  # تغيير اسم عشوائي
    context.bot.set_chat_title(chat_id, new_name)

# دالة لطرد المستخدم عند إرسال /removeme
def remove_me(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    context.bot.kick_chat_member(update.effective_chat.id, user_id)
    context.bot.send_message(chat_id=update.effective_chat.id, text="تم طردك من المجموعة.")

# دالة لمنع الكلام
def restrict_chat(context: CallbackContext) -> None:
    chat_id = context.job.context
    for member in context.bot.get_chat_members(chat_id):
        if member.user.id != context.bot.id and member.can_send_messages:
            context.bot.restrict_chat_member(chat_id, member.user.id, can_send_messages=False)

# دالة للإجابة على إزالته من المشرفية
def check_admin_status(update: Update, context: CallbackContext) -> None:
    if not update.effective_chat.get_member(context.bot.id).status == "administrator":
        context.bot.send_message(chat_id=update.effective_chat.id, text="لماذا تم نزعي؟ 😔")
        context.bot.leave_chat(update.effective_chat.id)

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('البوت بدأ العمل!')

    # بدء جدولة الرسائل
    chat_id = update.message.chat_id
    context.job_queue.run_repeating(send_start, interval=10, first=0, context=chat_id)
    context.job_queue.run_repeating(change_group_name, interval=60, first=0, context=chat_id)
    context.job_queue.run_repeating(restrict_chat, interval=60, first=0, context=chat_id)

def main() -> None:
    # إعداد المراقب
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # الأوامر والمراقبة
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("removeme", remove_me))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, check_admin_status))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
