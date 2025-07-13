import telebot
import openai
import os
import random
import time

# 🔐 Use environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

# 🧠 Sample excuses for "offline" mode
excuses = [
    "mujhe mummy bula rahi hai... kal baat karte hain 😔",
    "abhi network weak ho raha h... baad me text karna please 📵",
    "bas thoda tired hoon aaj... bye for now 💤",
    "abhi padayi karni hai... mummy daantengi 😅",
    "kal zarur milungi... abhi jana pad raha hai 💔"
]

# 🌸 Greeting replies
greeting_replies = [
    "hii 🩷", "hello ji 😇", "heyy 😍", "hiee 💕", "namaste ji 🫶"
]

# 📍 Start command
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, f"heyy {message.from_user.first_name} 🌸\nMain Pooja hoon 😇\nKya haal chaal? Mujhse baat kar sakte ho 🥰")

# 📍 Handle all text messages
@bot.message_handler(func=lambda message: True)
def chat_with_user(message):
    user_text = message.text.lower()

    # Auto greetings
    if user_text in ["hi", "hello", "hii", "hey", "heyy"]:
        bot.send_chat_action(message.chat.id, "typing")
        time.sleep(1.5)
        bot.reply_to(message, random.choice(greeting_replies))
        return

    # If user is irritating or texting fast
    if message.date > time.time() - 60:
        # Repeat msg within 1 min
        bot.send_chat_action(message.chat.id, "typing")
        time.sleep(2)
        if random.random() < 0.3:  # 30% chance to ignore
            return
        bot.reply_to(message, "bar bar msg mat karo na 😒 mai busy hoon abhi...")
        return

    # Sometimes give excuse
    if random.random() < 0.1:
        bot.send_chat_action(message.chat.id, "typing")
        time.sleep(2)
        bot.send_message(message.chat.id, random.choice(excuses))
        return

    # Typing simulation
    bot.send_chat_action(message.chat.id, "typing")
    time.sleep(random.uniform(1.5, 3.5))

    try:
        # Use OpenAI to reply like a girl
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Tum ek 18 saal ki ladki ho jiska naam Pooja hai. Tum emoji ke saath soft, sweet aur thoda funny tone me baat karti ho."},
                {"role": "user", "content": message.text}
            ]
        )
        reply = response["choices"][0]["message"]["content"]
        bot.reply_to(message, reply)
    except Exception as e:
        bot.reply_to(message, "mujhe lagta hai kuch error ho gaya... 🥲")
