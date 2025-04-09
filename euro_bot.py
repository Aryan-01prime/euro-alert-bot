import requests
import time
import threading
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater

# ✅ Your bot token and user ID (already filled in)
TOKEN = '7514499433:AAFi0kU_vxbuJFRyg40MpBrrM75DxrJiAek'
CHAT_ID = '1866841971'

# Alarm state and range
alarm_active = False
LOW = 90
HIGH = 94.5

# Get live Euro to INR rate
def get_euro_rate():
    url = 'https://api.exchangerate.host/latest?base=EUR&symbols=INR'
    response = requests.get(url).json()
    return response['rates']['INR']

# Send repeating alerts
def alarm_loop(bot):
    global alarm_active
    while alarm_active:
        bot.send_message(chat_id=CHAT_ID, text='🚨 *ALERT!* Euro is between ₹90 and ₹94.5! 🔊', parse_mode='Markdown')
        time.sleep(60)  # Alert every 1 minute

# Check rate and start alarm
def check_price(bot):
    global alarm_active
    rate = get_euro_rate()
    print(f"EUR/INR = ₹{rate}")
    if LOW <= rate <= HIGH and not alarm_active:
        alarm_active = True
        threading.Thread(target=alarm_loop, args=(bot,)).start()

# /start command
def start(update: Update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="👋 I'm now tracking Euro for you!")

# /stop command
def stop(update: Update, context):
    global alarm_active
    alarm_active = False
    context.bot.send_message(chat_id=update.effective_chat.id, text="🔕 Alert stopped.")

# Main bot loop
def main():
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("stop", stop))

    updater.start_polling()

    bot = Bot(token=TOKEN)

    # Check every 2 minutes
    while True:
        check_price(bot)
        time.sleep(120)

if __name__ == '__main__':
    main()
