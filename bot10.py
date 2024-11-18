import os
import subprocess
import sys

# تثبيت المكتبات تلقائيًا إذا لم تكن موجودة
def install_libraries():
    required_libraries = ["yt-dlp"]
    for lib in required_libraries:
        try:
            __import__(lib.replace("-", "_"))
        except ImportError:
            print(f"المكتبة {lib} غير مثبتة، يتم تثبيتها الآن...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

install_libraries()

from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# أدخل التوكن الخاص بك
BOT_TOKEN = "7177470820:AAFdhRgD4ctFCuAbzYslNqpK9Uc640MUxMk"

# وظيفة لتحميل محتوى الرابط باستخدام yt-dlp
def download_content(url, chat_id, bot):
    try:
        output_dir = "downloads"
        os.makedirs(output_dir, exist_ok=True)
        result = subprocess.run(
            ["yt-dlp", "-o", f"{output_dir}/%(title)s.%(ext)s", url],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            # البحث عن الملفات المحملة
            files = os.listdir(output_dir)
            for file in files:
                file_path = os.path.join(output_dir, file)
                bot.send_document(chat_id=chat_id, document=open(file_path, "rb"))
                os.remove(file_path)  # حذف الملف بعد الإرسال
        else:
            bot.send_message(chat_id=chat_id, text="⚠️ حدث خطأ أثناء تحميل الرابط.")
    except Exception as e:
        bot.send_message(chat_id=chat_id, text=f"⚠️ خطأ: {e}")

# وظيفة الرد على الرسائل
def handle_message(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    url = update.message.text

    if url.startswith("http://") or url.startswith("https://"):
        update.message.reply_text("⏳ يتم الآن تحميل المحتوى، الرجاء الانتظار...")
        download_content(url, chat_id, context.bot)
    else:
        update.message.reply_text("⚠️ الرجاء إرسال رابط صحيح يبدأ بـ http:// أو https://")

# وظيفة بدء البوت
def start(update: Update, context: CallbackContext):
    update.message.reply_text("👋 أهلاً بك! أرسل لي رابطاً لأي فيديو أو محتوى لتحميله.")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
