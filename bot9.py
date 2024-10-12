from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters
import logging

# ضع توكن البوت هنا
TOKEN = 'YOUR_TOKEN_HERE'

# إعداد تسجيل الأخطاء
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# بدء تشغيل البوت
def start(update, context):
    chat_id = update.message.chat_id
    context.bot.send_message(chat_id=chat_id, text="تم تفعيل البوت بنجاح!")

def handle_member_status(update, context):
    user = update.message.from_user
    bot = context.bot
    chat = update.message.chat

    # إذا كان البوت قد تم إضافته كمشرف
    if bot.get_chat_member(chat.id, bot.id).status == 'administrator':
        # رسالة عند تفعيل البوت
        text = f"تم تفعيل المجموعة تلقائيًا من طرف @{user.username}\nالبوت قيد التطوير 🤖\nاضغط هنا لتفعيل البوت 👇🏻"
        keyboard = [[InlineKeyboardButton("تفعيل البوت", callback_data='start_bot')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=chat.id, text=text, reply_markup=reply_markup)
    
    # إذا كان البوت قد تم إضافته كعضو عادي
    else:
        # إرسال رسالة ثم خروج البوت
        bot.send_message(chat_id=chat.id, text="لا أستطيع القيام بأي شيء دون أن أكون مشرفًا. وداعًا! 👋")
        bot.leave_chat(chat_id=chat.id)

def button(update, context):
    query = update.callback_query
    if query.data == 'start_bot':
        context.bot.send_message(chat_id=query.message.chat_id, text="/start")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # التعامل مع الأوامر
    dp.add_handler(CommandHandler('start', start))

    # التعامل مع إضافة البوت كمشرف أو عضو
    dp.add_handler(MessageHandler(Filters.status_update, handle_member_status))

    # التعامل مع الضغط على الأزرار
    dp.add_handler(CallbackQueryHandler(button))

    # تشغيل البوت
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
