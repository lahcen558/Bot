import subprocess
import sys
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from time import sleep

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

# إعداد التسجيل
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# توكن البوت
TOKEN = "7772254227:AAGj5EfcztM87V0uxJAlQOAog4KBpWm__Ro"

# قائمة لحفظ المستخدمين الذين تم منعهم
blocked_users = set()

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('مرحبًا! أنا هنا لحماية المجموعة.')

def message_handler(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    # منع إرسال الرسائل كل دقيقة
    if user_id in blocked_users:
        # حذف الرسالة إذا كان المستخدم ممنوعًا
        context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
        return

    # التحقق من وجود رابط في الرسالة
    if update.message.text and ('http://' in update.message.text or 'https://' in update.message.text or 't.me' in update.message.text):
        context.bot.delete_message(chat_id=update.message.chat.id, message_id=update.message.message_id)
        logging.info(f'تم حذف رسالة تحتوي على رابط من {update.message.from_user.username}.')
        return

    # إضافة المستخدم إلى قائمة المحظورين
    blocked_users.add(user_id)
    try:
        update.message.reply_text('لقد قمت بإرسال رسالة. يجب أن تنتظر دقيقة قبل إرسال رسالة جديدة.')
    except Exception as e:
        logging.error(f'خطأ في إرسال رسالة: {e}')
        
    sleep(60)  # الانتظار لمدة دقيقة
    blocked_users.remove(user_id)  # إزالة المستخدم من قائمة المحظورين بعد دقيقة

def main() -> None:
    # إعداد المراقب
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # الأوامر والمراقبة
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    # بدء البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
