import requests
from telegram import Update, Bot, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import time
import os
import sys
import threading

# توكن البوت
TOKEN = '7945039209:AAEsCFKI3dWgBpLM5TBehksud9mufzCjERs'
ADMIN_USER_ID = 7448496964

# متغيرات حالة الطقس
last_weather_info = None
sending_weather = True

# حذف الرسائل من المجموعة
def delete_message(update: Update, context: CallbackContext):
    if update.message and update.message.from_user.id != ADMIN_USER_ID:
        try:
            context.bot.delete_message(chat_id=update.message.chat_id, message_id=update.message.message_id)
        except:
            pass  # تجاهل الأخطاء إذا لم يستطع البوت حذف الرسالة

# الحصول على الطقس بناءً على الـ IP أو الموقع
def get_weather_by_ip():
    try:
        # طلب معلومات الطقس من wttr.in
        weather_url = f"http://wttr.in/?format=3"  # 'format=3' يعطي وصفًا قصيرًا للطقس
        weather_response = requests.get(weather_url)
        return weather_response.text
    except Exception as e:
        return None

# إرسال الطقس كل دقيقة
def send_weather_if_changed(update: Update, context: CallbackContext):
    global last_weather_info
    user_ip = None  # سيتم الاعتماد على الموقع الافتراضي

    while True:
        try:
            current_weather_info = get_weather_by_ip()
            if current_weather_info and current_weather_info != last_weather_info:
                last_weather_info = current_weather_info
                context.bot.send_message(chat_id=update.message.chat_id, text=current_weather_info)
                if ADMIN_USER_ID:
                    context.bot.send_message(chat_id=ADMIN_USER_ID, text=f"Weather updated: {current_weather_info}")
            time.sleep(60)  # التحديث كل دقيقة
        except Exception as e:
            # في حال حدوث خطأ، إعادة تشغيل البوت تلقائيًا
            context.bot.send_message(chat_id=ADMIN_USER_ID, text="Error occurred! Restarting the bot...")
            restart_bot()

# إعادة تشغيل البوت تلقائيًا
def restart_bot():
    try:
        # إعادة تشغيل العملية الحالية
        os.execv(sys.executable, ['python'] + sys.argv)
    except Exception as e:
        print(f"Error restarting the bot: {e}")

# تشغيل ميزة الطقس
def start_weather_updates(update: Update, context: CallbackContext):
    global sending_weather
    sending_weather = True
    update.message.reply_text('Weather updates have started!')
    threading.Thread(target=send_weather_if_changed, args=(update, context)).start()

# إيقاف ميزة الطقس
def stop_weather_updates(update: Update, context: CallbackContext):
    global sending_weather
    sending_weather = False
    update.message.reply_text('Weather updates have been stopped!')

# بدء البوت
def start(update: Update, context: CallbackContext):
    update.message.reply_text('Welcome! I will give you weather updates automatically.')

# إعداد البوت
def main():
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # أوامر البوت
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop_weather_updates))  # إيقاف تحديثات الطقس
    dispatcher.add_handler(CommandHandler("go", start_weather_updates))  # بدء تحديثات الطقس

    # حذف الرسائل من المجموعة
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, delete_message))

    # بدء التحديثات تلقائيًا عند تشغيل البوت
    updater.start_polling()
    updater.idle()
    threading.Thread(target=send_weather_if_changed, args=(None, None)).start()

if __name__ == '__main__':
    main()
