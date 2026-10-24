import os
import threading
import telebot
from flask import Flask

# 1. التوكن الجديد الصحيح من BotFather
TOKEN = "ضَع_التوكن_الجديد_هنا"
bot = telebot.TeleBot(TOKEN)

# 2. قاعدة بيانات الكتب البسيطة
books_db = {
    "بايثون": "https://example.com/python",
    "برمجة": "https://example.com/programming",
    "ذكاء اصطناعي": "https://example.com/ai",
    "سي شارب": "https://example.com/csharp"
}

def find_book(query_text):
    query = query_text.strip().lower()
    for book_name, book_link in books_db.items():
        if book_name in query:
            return book_link
    return None

# 3. إعدادات فلاسك لإرضاء UptimeRobot ومنصة Render
app = Flask(__name__)

@app.route('/')
def home():
    return "Aether Library Bot is running!"

# 4. الهاندلرات (أوامر ورسائل البوت)
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "📚 أهلاً بك في مكتبة Aether Nova\n\n"
        "اكتب اسم الكتاب للبحث عنه (مثل: بايثون، برمجة، ذكاء اصطناعي، سي شارب)، وسأرسل لك رابطه فوراً."
    )
    bot.reply_to(message, welcome_text)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_text = message.text
    book_link = find_book(user_text)

    if book_link:
        reply_text = f"📚 رابط تحميل الكتاب:\n{book_link}"
    else:
        reply_text = (
            "عذراً، لم أجد كتاباً بهذا الاسم.\n"
            "جرب البحث عن: بايثون، برمجة، ذكاء اصطناعي، أو سي شارب."
        )
    bot.reply_to(message, reply_text)

# 5. تشغيل البوت في الخلفية مع حذف أي Webhook قديم عائق
def run_telegram_bot():
    try:
        bot.remove_webhook()
        bot.infinity_polling()
    except Exception as e:
        print(f"Bot error: {e}")

if __name__ == "__main__":
    # تشغيل تليجرام في الخلفية عبر Thread
    t = threading.Thread(target=run_telegram_bot)
    t.daemon = True
    t.start()

    # تشغيل سيرفر الفلاسك على المنفذ المطلوب لـ Render
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
