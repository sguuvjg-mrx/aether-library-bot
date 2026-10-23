import os
import threading
import telebot
from flask import Flask

# 1. ضع توكن بوتك الحقيقي هنا
TOKEN = 'ضع_توكن_البوت_هنا'
bot = telebot.TeleBot(TOKEN)

# 2. ضع هنا كل الأوامر والهاندلرات (Handlers) الخاصة بكود بوتك الحقيقي
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # ضع ردك أو كودك الحقيقي هنا
    bot.reply_to(message, "أهلاً بك في بوت مكتبة الأثير...")

# (يمكنك إضافة باقي أوداك وهاندلراتك هنا بكل حرية...)


# 3. إعدادات سيرفر الفلاسك (لإرضاء منصة Render وابقاء البوت شغالاً)
app = Flask(__name__)

@app.route('/')
def home():
    return "Aether Library Bot is running!"

# 4. دالة لتشغيل البوت في الخلفية عبر خيط (Thread)
def run_telegram_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل بوت التليجرام في الخلفية
    t = threading.Thread(target=run_telegram_bot)
    t.start()

    # تشغيل سيرفر الفلاسك على المنفذ المطلوب لـ Render
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)



import telebot

# توكن البوت الخاص بك
TOKEN = "8686110166:AAEJTbKCLlI1co38LiTb2vu0ZFpufFfq2tY"
bot = telebot.TeleBot(TOKEN)

# 1. قاعدة بيانات بسيطة لتخزين الكتب (اسم الكتاب والرابط الخاص به)
books_db = {
    "بايثون": "https://example.com/python-book.pdf",
    "برمجة": "https://example.com/programming-basics.pdf",
    "ذكاء اصطناعي": "https://example.com/ai-intro.pdf",
    "سي شارب": "https://example.com/csharp-guide.pdf",
}


# 2. فانكشن مخصصة للبحث عن الكتاب (مهمة واحدة فقط: البحث وإرجاع النتيجة)
def find_book(query_text):
  query = query_text.strip().lower()
  for book_name, book_link in books_db.items():
    if book_name in query:
      return book_link
  return None


# 3. فانكشن الترحيب (تتفاعل مع أوامر البداية)
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
  welcome_text = (
      "أهلاً بك في مكتبة Aether Nova 📚\n"
      "أرسل لي اسم الكتاب الذي تبحث عنه (مثل: بايثون، برمجة، ذكاء اصطناعي، سي"
      " شارب)، وسأرسل لك رابطه فوراً!"
  )
  bot.reply_to(message, welcome_text)


# 4. فانكشن استقبال الرسائل ومعالجتها والرد على المستخدم
@bot.message_handler(func=lambda message: True)
def handle_message(message):
  user_text = message.text
  print(f"رسالة واردة: {user_text}")

  # البحث عن الكتاب باستخدام الفانكشن المستقلة
  book_link = find_book(user_text)

  if book_link:
    reply_text = f"تم العثور على طلبك! 📖\nرابط تحميل الكتاب:\n{book_link}"
  else:
    reply_text = (
        "عذراً، لم أجد هذا الكتاب حالياً. جرب البحث عن: بايثون، برمجة، ذكاء"
        " اصطناعي، أو سي شارب."
    )

  bot.reply_to(message, reply_text)


# تشغيل البوت بشكل مستمر
if __name__ == "__main__":
  print("البوت يعمل الآن ونظام الكتب جاهز...")
  bot.infinity_polling()
