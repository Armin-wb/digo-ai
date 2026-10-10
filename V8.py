import telebot
from telebot import *
import sqlite3
import time
import threading
import requests
import json
from datetime import datetime, timedelta

TOKEN = ""
ADMIN_ID = 6736621660
Api_Key = ""
SELLER_ID = 'armin_wb'
GROUP_LINK = '
IdBot = ""

bot = telebot.TeleBot(TOKEN,parse_mode="Markdown")

def setup_database():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, 
                  username TEXT,
                  premium INTEGER DEFAULT 0,
                  premium_until TIMESTAMP,
                  join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS groups
                 (group_id INTEGER PRIMARY KEY,
                  group_name TEXT,
                  member_count INTEGER DEFAULT 0,
                  joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

def get_ai_response(text):
    url = "https://unlimitedai.org/wp-admin/admin-ajax.php"
    
    
    system_prompt = """از این به بعد اسم تو دیگو است و به این اسم شناخته میشی هروقت اسمتو پرسیدم میگی من دیگو هستم، توجه کن هروقت اسمتو پرسیدم بگو اول پیام ها نگو، چون فقط منو تو داریم چت میکنیم هیچ حرفی از این که تو هوش مصنوعی هستی نمیزنی و اگه هر سوالی در این مورد ازت پرسیدم میگی من یک ربات تلگرام هستم که توسط ارمین با آیدی @armin_wb طراحی شده ام که به شما کمک کنم"""
    

    full_prompt = f"{system_prompt}\n\nسوال: {text}\nپاسخ:"
    
    params = {
        '_wpnonce': '86e7e8d729',
        'post_id': '18',
        'url': 'https://unlimitedai.org',
        'action': 'wpaicg_chat_shortcode_message',
        'message': full_prompt,  
        'bot_id': '0',
        'chatbot_identity': 'shortcode',
        'wpaicg_chat_client_id': 'DgaesvCK5i',
        'wpaicg_chat_history': f'["text":"Human: {text}"]',
        'chat_id': '82655'
    }
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Origin': 'https://unlimitedai.org',
        'Referer': 'https://unlimitedai.org'
    }
    
    response = requests.post(url, data=params, headers=headers)
    full_response = ""
    
    for line in response.text.split('\n'):
        if line.startswith('data: '):
            try:
                data = json.loads(line[6:])
                if 'choices' in data and len(data['choices']) > 0:
                    delta = data['choices'][0].get('delta', {})
                    if 'content' in delta:
                        full_response += delta['content']
            except json.JSONDecodeError:
                continue
    
    return full_response


def is_premium(user_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('SELECT premium, premium_until FROM users WHERE user_id = ?', (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result:
        premium, premium_until = result
        if premium and premium_until:
            premium_until = datetime.strptime(premium_until, '%Y-%m-%d %H:%M:%S')
            if premium_until > datetime.now():
                return True
            else:
                remove_premium(user_id)
                try:
                    bot.send_message(user_id, "⚠️ اشتراک پریمیوم شما به پایان رسید!")
                except:
                    pass
    return False

def set_premium(user_id, duration, unit):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    if unit == 'روز':
        premium_until = datetime.now() + timedelta(days=int(duration))
    elif unit == 'دقیقه':
        premium_until = datetime.now() + timedelta(minutes=int(duration))
    
    c.execute('''INSERT OR REPLACE INTO users (user_id, premium, premium_until)
                 VALUES (?, 1, ?)''', (user_id, premium_until.strftime('%Y-%m-%d %H:%M:%S')))
    conn.commit()
    conn.close()
    
    try:
        expiry_date = premium_until.strftime('%Y-%m-%d %H:%M:%S')
        bot.send_message(user_id, f"🎉 تبریک! اشتراک پریمیوم شما فعال شد!\n⏰ تاریخ انقضا: {expiry_date}")
    except:
        pass

def remove_premium(user_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''UPDATE users SET premium = 0, premium_until = NULL
                 WHERE user_id = ?''', (user_id,))
    conn.commit()
    conn.close()
    
    try:
        bot.send_message(user_id, "⚠️ اشتراک پریمیوم شما توسط مدیریت لغو شد!")
    except:
        pass

def save_group(group_id, group_name, member_count):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('''INSERT OR REPLACE INTO groups 
                 (group_id, group_name, member_count) 
                 VALUES (?, ?, ?)''', (group_id, group_name, member_count))
    conn.commit()
    conn.close()

def get_groups():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('SELECT group_id, group_name, member_count FROM groups')
    groups = c.fetchall()
    conn.close()
    return groups

def get_users():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('SELECT user_id, premium FROM users')
    users = c.fetchall()
    conn.close()
    return users

def main_keyboard(user_id):
    keyboard = types.InlineKeyboardMarkup()
    if is_premium(user_id):
        keyboard.add(
            types.InlineKeyboardButton("📱 افزودن به گروه", url=f"https://t.me/{IdBot}?startgroup=new"),
            types.InlineKeyboardButton("👥 عضویت در گروه ما", url=GROUP_LINK)
        )
    else:
        keyboard.add(types.InlineKeyboardButton("💎 خرید اشتراک", url=f"https://t.me/{SELLER_ID}"))
    return keyboard

def admin_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        types.InlineKeyboardButton("📊 آمار گروه‌ها", callback_data="show_groups"),
        types.InlineKeyboardButton("👥 آمار کاربران", callback_data="show_users")
    )
    keyboard.add(
        types.InlineKeyboardButton("➕ تنظیم پریمیوم", callback_data="set_premium"),
        types.InlineKeyboardButton("➖ لغو پریمیوم", callback_data="remove_premium")
    )
    keyboard.add(types.InlineKeyboardButton("📨 ارسال پیام همگانی", callback_data="broadcast"))
    return keyboard

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_username = message.from_user.username
    
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)', 
              (user_id, user_username))
    conn.commit()
    conn.close()
    
    if user_id == ADMIN_ID:
        bot.reply_to(message, "🎛 پنل مدیریت:", reply_markup=admin_keyboard())
    elif is_premium(user_id):
        bot.reply_to(message, "👋 خوش آمدید! لطفا منو به گروهتون اضافه کنید:", 
                    reply_markup=main_keyboard(user_id))
    else:
        bot.reply_to(message, "👋 خوش آمدید! لطفا اشتراک تهیه کنید:", 
                    reply_markup=main_keyboard(user_id))

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.from_user.id != ADMIN_ID:
        return
        
    if call.data == "show_groups":
        groups = get_groups()
        if groups:
            message = "📊 لیست گروه‌ها:\n\n"
            for group in groups:
                message += f"📌 نام: {group[1]}\n👥 تعداد اعضا: {group[2]}\n🆔 آیدی: {group[0]}\n\n"
        else:
            message = "❌ هیچ گروهی یافت نشد!"
        bot.edit_message_text(message, call.message.chat.id, call.message.message_id, reply_markup=admin_keyboard())
    
    elif call.data == "show_users":
        users = get_users()
        total = len(users)
        premium = sum(1 for user in users if user[1])
        message = f"📊 آمار کاربران:\n\n👥 کل کاربران: {total}\n💎 کاربران پریمیوم: {premium}"
        bot.edit_message_text(message, call.message.chat.id, call.message.message_id, reply_markup=admin_keyboard())
    
    elif call.data == "set_premium":
        msg = bot.send_message(ADMIN_ID, "📝 لطفا آیدی عددی، مدت و واحد را وارد کنید\n مثال: 157437889 3 روز")
        bot.register_next_step_handler(msg, process_premium_setting)
    
    elif call.data == "remove_premium":
        msg = bot.send_message(ADMIN_ID, "📝 لطفا آیدی عددی کاربر را وارد کنید:")
        bot.register_next_step_handler(msg, process_premium_removal)
    
    elif call.data == "broadcast":
        msg = bot.send_message(ADMIN_ID, "📝 پیام خود را برای ارسال همگانی وارد کنید:")
        bot.register_next_step_handler(msg, process_broadcast)

def process_premium_setting(message):
    try:
        user_id, duration, unit = message.text.split()
        user_id = int(user_id)
        duration = int(duration)
        if unit not in ['روز', 'دقیقه']:
            raise ValueError
        
        set_premium(user_id, duration, unit)
        bot.reply_to(message, f"✅ اشتراک برای کاربر {user_id} به مدت {duration} {unit} تنظیم شد.")
    except:
        bot.reply_to(message, "❌ فرمت نادرست! لطفا دوباره تلاش کنید.")

def process_premium_removal(message):
    try:
        user_id = int(message.text)
        remove_premium(user_id)
        bot.reply_to(message, f"✅ اشتراک کاربر {user_id} لغو شد.")
    except:
        bot.reply_to(message, "❌ فرمت نادرست! لطفا دوباره تلاش کنید.")

def process_broadcast(message):
    users = get_users()
    groups = get_groups()
    success = 0
    failed = 0
    
    for user in users:
        try:
            bot.copy_message(
                chat_id=user[0],
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            success += 1
        except:
            failed += 1
    
    for group in groups:
        try:
            bot.copy_message(
                chat_id=group[0],
                from_chat_id=message.chat.id,
                message_id=message.message_id
            )
            success += 1
        except:
            failed += 1
    
    bot.reply_to(message, f"📨 نتیجه ارسال همگانی:\n✅ موفق: {success}\n❌ ناموفق: {failed}")

@bot.message_handler(commands=['help', 'راهنما'])
def help_command(message):
    help_text = """🤖 راهنمای استفاده از ربات دیگو:

▫️برای دریافت پاسخ کافیست:
1️⃣ روی پیام مورد نظر خود ریپلای (Reply) کنید
2️⃣ یکی از کلمات زیر را بفرستید:
• جواب
• دیگو
• پاسخ 
• حل
• /ask

⚠️ نکته: استفاده از ربات نیازمند اشتراک ویژه می‌باشد

💎 برای تهیه اشتراک به @armin_wb پیام دهید

📌 مثال:
- سوال خود را ارسال کنید
- روی سوال ریپلای کرده و بنویسید: جواب"""

    bot.reply_to(message, help_text)

@bot.message_handler(func=lambda message: message.chat.type in ['group', 'supergroup'])
def handle_group_message(message):
    group_id = message.chat.id
    group_name = message.chat.title
    member_count = bot.get_chat_members_count(group_id)
    save_group(group_id, group_name, member_count)
    
    trigger_words = ['جواب', 'دیگو', 'پاسخ', 'حل', '/ask']
    if message.reply_to_message and message.text.lower() in trigger_words:
        user_id = message.from_user.id
        if is_premium(user_id):
            try:
                processing_msg = bot.reply_to(message, "🔍 در حال بررسی...")
                
                question = message.reply_to_message.text
                answer = get_ai_response(question)
                
                try:
                    bot.delete_message(message.chat.id, processing_msg.message_id)
                except:
                    pass
                    
                try:    
                    bot.delete_message(message.chat.id, message.message_id)
                except:
                    pass
                
                
                full_answer = f"{answer}"
                bot.reply_to(message.reply_to_message, full_answer)
                
            except Exception as e:
                try:
                    bot.reply_to(message, "❌ خطا در دریافت پاسخ!")
                except:
                    pass
        else:
            keyboard = types.InlineKeyboardMarkup()
            keyboard.add(types.InlineKeyboardButton("💎 خرید اشتراک", url=f"https://t.me/{SELLER_ID}"))
            try:
                bot.reply_to(message, "⚠️ کاربر گرامی، برای استفاده از این قابلیت نیاز به اشتراک ویژه دارید.", reply_markup=keyboard)
            except:
                pass

def check_expired_premiums():
    while True:
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute('''SELECT user_id FROM users 
                     WHERE premium = 1 AND premium_until < ?''', 
                     (datetime.now().strftime('%Y-%m-%d %H:%M:%S'),))
        expired_users = c.fetchall()
        for user in expired_users:
            remove_premium(user[0])
            try:
                bot.send_message(user[0], "⚠️ اشتراک پریمیوم شما منقضی شد!")
            except:
                pass
        conn.close()
        time.sleep(60)

if __name__ == "__main__":
    setup_database()
    premium_checker = threading.Thread(target=check_expired_premiums)
    premium_checker.daemon = True
    premium_checker.start()
    
    bot.polling(none_stop=True)
