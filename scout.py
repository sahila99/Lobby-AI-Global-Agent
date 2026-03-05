import os
import requests
import pandas as pd
from datetime import datetime

def send_telegram_msg(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    if token and chat_id:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}
        try:
            requests.post(url, data=payload)
        except Exception as e:
            print(f"Error sending Telegram: {e}")

def run_scout():
    # This is where your search logic lives
    # For now, let's send a Test Alert to your phone!
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    test_msg = f"🚀 *Lobby-AI System Online*\n\n✅ Scout is active.\n📅 Time: {now}\n🌍 Regions: Nigeria, India, UAE\n\n_Your next job lead will appear here._"
    
    send_telegram_msg(test_msg)
    print("Test alert sent to Telegram!")

if __name__ == "__main__":
    run_scout()
