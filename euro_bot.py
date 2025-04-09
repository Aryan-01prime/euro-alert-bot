import requests
import time
import threading
from telegram import Bot

# ✅ Your bot token and user ID (already filled in)
TOKEN = '7514499433:AAFi0kU_vxbuJFRyg40MpBrrM75DxrJiAek'
CHAT_ID = '1866841971'

alarm_active = False
LOW = 90
HIGH = 94.5

def get_euro_rate():
    try:
        url = 'https://api.exchangerate.host/latest?base=EUR&symbols=INR'
        response = requests.get(url, timeout=10).json()
        rate = response.get('rates', {}).get('INR')
        if rate is not None:
            return rate
        else:
            print("⚠️ INR rate missing:", response)
            return None
    except Exception as e:
        print(f"🚨 API error: {e}")
        return None

def alarm_loop(bot):
    global alarm_active
    while alarm_active:
        bot.send_message(chat_id=CHAT_ID, text='🚨 *ALERT!* Euro is between ₹90 and ₹94.5! 🔊', parse_mode='Markdown')
        time.sleep(60)

def check_price(bot):
    global alarm_active
    rate = get_euro_rate()
    if rate is None:
        return
    print(f"EUR/INR = ₹{rate}")
    if LOW <= rate <= HIGH and not alarm_active:
        alarm_active = True
        threading.Thread(target=alarm_loop, args=(bot,)).start()

def main():
    bot = Bot(token=TOKEN)
    print("✅ Bot started and tracking EUR/INR...")
    while True:
        check_price(bot)
        time.sleep(120)

if __name__ == '__main__':
    main()

