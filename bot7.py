from telegram import Update, ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from collections import defaultdict
import time

# توكن البوت
TOKEN = "7770873994:AAEDuCatwYvEwP2YpqFjbgITayAcFcVTi-o"

# عدد الرسائل المسموح بها قبل الحظر
MAX_MESSAGES = 5

# لتتبع عدد الرسائل لكل مستخدم
user_message_count = defaultdict(int)

# لتتبع الأوقات التي تم فيها حظر المستخدمين
banned_users = {}

def start(update: Update, context: CallbackContext):
    """إرسال /start لتنشيط البوتات الأخرى."""
    update.message.reply_text("/start")

def send_start_command(context: CallbackContext):
    """إرسال /start بشكل تلقائي كل دقيقة."""
    chat_id = context.job.context['chat_id']
    
    # تأكد من أن chat_id ليس هو معرف البوت نفسه
    if chat_id != context.bot.id:
        context.bot.send_message(chat_id=chat_id, text="/start")

def restore_group_name(update: Update, context: CallbackContext):
    """إعادة اسم المجموعة إلى الاسم الأصلي إذا تم تغييره."""
    original_group_name = "بوتات حسن 🤖🦅⭐"  # أدخل اسم المجموعة الأصلي هنا
    if update.effective_chat.title != original_group_name:
        try:
            context.bot.set_chat_title(update.effective_chat.id, original_group_name)
        except Exception as e:
            print(f"Error changing group title: {e}")  # طباعة الخطأ إذا حدث

def message_handler(update: Update, context: CallbackContext):
    """معالجة الرسائل، وحساب عدد الرسائل المرسلة من المستخدمين."""
    user_id = update.message.from_user.id

    if user_id in banned_users and time.time() < banned_users[user_id]:
        return  # إذا كان المستخدم محظورًا، لا نقوم بأي شيء

    # زيادة عدد الرسائل المرسلة من المستخدم
    user_message_count[user_id] += 1

    # إذا تجاوز عدد الرسائل الحد المسموح به
    if user_message_count[user_id] > MAX_MESSAGES:
        banned_users[user_id] = time.time() + 60  # حظر المستخدم لمدة دقيقة
        user_message_count[user_id] = 0  # إعادة تعيين العد
        
        # تحديد الحقوق التي سنمنعها
        permissions = ChatPermissions(can_send_messages=False)

        context.bot.restrict_chat_member(
            update.effective_chat.id,
            user_id,
            permissions=permissions,
            until_date=int(time.time()) + 60  # حظر لمدة دقيقة
        )
        update.message.reply_text("لقد تم حظرك لمدة دقيقة بسبب تجاوز عدد الرسائل المسموح بها.")

def main():
    """بدء تشغيل البوت."""
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # إضافة معالجات الأوامر
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))
    
    # إضافة معالج لتغيير اسم المجموعة
    dp.add_handler(MessageHandler(Filters.chat_type.groups, restore_group_name))

    # إضافة الوظيفة لإرسال /start كل دقيقة
    job_queue = updater.job_queue
    job_queue.run_repeating(send_start_command, interval=60, first=0, context={'chat_id': updater.bot.id})

    # بدء التشغيل
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
