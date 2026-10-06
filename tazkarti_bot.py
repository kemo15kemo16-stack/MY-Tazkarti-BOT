import cloudscraper
import requests
import time

# بيانات تليجرام الخاصة بك
TELEGRAM_TOKEN = "8994442523:AAH19a6koPMPbzjUZhJoxDH4myETCYMYLDs"
CHAT_ID = "1194432564"

# رابط صفحة المباريات السري
TAZKARTI_URL = "https://tazkarti.com/data/matches-list-json.json?_=1791305778927"
KEYWORDS = ["النادي الأهلى", "نادى الزمالك", "Al Ahly FC", "Zamalek SC"]

def send_telegram_alert(message):
    """دالة لإرسال إشعار على تليجرام"""
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("✅ Alert sent successfully!")
        else:
            print(f"❌ Telegram Error: {response.text}")
    except Exception as e:
        print("❌ Error sending alert:", e)

def check_tazkarti():
    """دالة لفحص موقع تذكرتي"""
    # هنا استخدمنا cloudscraper عشان نتخطى الحماية كأننا متصفح حقيقي
    scraper = cloudscraper.create_scraper()
    
    try:
        response = scraper.get(TAZKARTI_URL, timeout=15)
        
        if response.status_code == 200:
            text_content = response.text
            
            for keyword in KEYWORDS:
                if keyword in text_content:
                    # خلينا الرابط اللي هيوصلك هو رابط الحجز المباشر
                    alert_msg = f"🚨 الحق بسرعة! تذاكر ماتش ({keyword}) شكلها نزلت على تذكرتي 🏃‍♂️🔥\nالرابط: https://tazkarti.com/#/matches"
                    send_telegram_alert(alert_msg)
                    return True 
            
            print(f"[{time.strftime('%H:%M:%S')}] No tickets yet, checking again...")
        else:
            print(f"⚠ Connection problem. Status code: {response.status_code}")
            
    except Exception as e:
        print("❌ Connection error:", e)
        
    return False

# تشغيل البوت بشكل مستمر
print("🤖 Tazkarti PRO bot started... Monitoring!")
while True:
    match_found = check_tazkarti()
    
    if match_found:
        print("🎉 Match found, stopping bot to avoid spam.")
        break 
        
    time.sleep(60)