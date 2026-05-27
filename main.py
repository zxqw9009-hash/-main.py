import telebot
from telebot import types

# التوكن الجديد المحدث لبوتك
API_TOKEN = '8901455370:AAF35Amt2olwb_sUAlLzG9oagIDJiHT-doo'

bot = telebot.TeleBot(API_TOKEN)

# عند إرسال /start أو الضغط على انضمام
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "مرحباً بك! أهلاً فيك.. مساعدك الذكي لادارة الاشتراكات والدخول الى قنوات ( سابقاً طاغي 🎀QUEEN 👑 ).\n"
        "حصلت على خصم لاشتراكك الأول بمناسبة دخولك للقناة: اشتراكك الدائم أصبح بـ 150 ريال بدلاً من 200 ريال."
    )
    
    # إنشاء أزرار الكيبورد الأساسية تحت خانة الكتابة
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn_join = types.KeyboardButton("انضمام")
    btn_way = types.KeyboardButton("طريقة شراء بطاقات لايك كارد")
    btn_meet = types.KeyboardButton("المقابلات 🤝")
    btn_warn = types.KeyboardButton("تنبيهات قبل الاشتراك")
    btn_sub_guarantee = types.KeyboardButton("ضمان الاشتراك 📢")
    btn_meet_guarantee = types.KeyboardButton("ضمان المقابلات 📢")
    
    markup.add(btn_join, btn_way, btn_meet, btn_warn, btn_sub_guarantee, btn_meet_guarantee)
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# التعامل مع الضغط على الأزرار النصية
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "انضمام":
        # إنشاء أزرار الانلاين (تحت الرسالة) لاختيار نوع الاشتراك
        inline_markup = types.InlineKeyboardMarkup(row_width=2)
        btn_always = types.InlineKeyboardButton("دائم", callback_data="sub_always")
        btn_monthly = types.InlineKeyboardButton("شهري", callback_data="sub_monthly")
        inline_markup.add(btn_always, btn_monthly)
        
        bot.send_message(message.chat.id, "اختر نوع الاشتراك:", reply_markup=inline_markup)
        
    elif message.text == "طريقة شراء بطاقات لايك كارد":
        bot.send_message(message.chat.id, "شرح طريقة شراء بطاقات لايك كارد...")
        
    elif message.text == "المقابلات 🤝":
        bot.send_message(message.chat.id, "تفاصيل المقابلات...")
        
    elif message.text == "تنبيهات قبل الاشتراك":
        bot.send_message(message.chat.id, "تنبيهات هامة قبل الاشتراك...")
        
    elif message.text == "ضمان الاشتراك 📢":
        bot.send_message(message.chat.id, "تفاصيل ضمان الاشتراك...")
        
    elif message.text == "ضمان المقابلات 📢":
        bot.send_message(message.chat.id, "تفاصيل ضمان المقابلات...")
        
    # إذا أرسل المستخدم كود مكون من 16 خانة (بطاقة لايك كارد)
    elif len(message.text) == 16 and message.text.isdigit():
        bot.send_message(message.chat.id, "جاري التحقق من كود البطاقة، يرجى الانتظار...")
    else:
        # رد تلقائي إذا أرسل كود غلط أو نص غير مفهوم
        bot.send_message(message.chat.id, "عذراً، الكود الذي أدخلته غير صحيح. يرجى التأكد من إدخال كود بطاقة لايك كارد المكون من 16 حرفاً ورقماً فقط. الرجاء المحاولة مرة أخرى.")

# التعامل مع ضغط أزرار الانلاين (دائم / شهري)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "sub_monthly":
        bot.send_message(call.message.chat.id, "اشتراك شهري بقيمة 100 ريال عبر لايك كارد. يرجى إرسال كود البطاقة المكون من 16 خانة الآن:")
    elif call.data == "sub_always":
        bot.send_message(call.message.chat.id, "اشتراك دائم بقيمة 150 ريال عبر لايك كارد. يرجى إرسال كود البطاقة المكون من 16 خانة الآن:")

# تشغيل البوت بشكل مستمر ومحمي من السقوط
if __name__ == '__main__':
    import os
    from flask import Flask
    app = Flask(__name__)
    @app.route('/')
    def index(): return "Bot is running!"
    
    import threading
    threading.Thread(target=lambda: bot.infinity_polling(timeout=10, long_polling_timeout=5)).start()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

