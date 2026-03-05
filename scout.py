import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime

# --- CONFIGURATION: Telegram Setup ---
def send_telegram_msg(message):
    token = os.getenv('TELEGRAM_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not token or not chat_id:
        print("⚠️ Missing Telegram Secrets in GitHub!")
        return

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id, 
        "text": message, 
        "parse_mode": "Markdown",
        "disable_web_page_preview": False
    }
    
    try:
        response = requests.post(url, data=payload)
        print(f"📡 Telegram Server Response: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

# --- CORE LOGIC: The Job Hunter ---
def run_scout():
    print("🚀 Lobby-AI: Starting Executive Search...")
    db_file = 'job_database.csv'
    
    # Target Roles and Locations for your Executive Hub
    queries = [
        "Head of IT jobs in Lagos Nigeria",
        "IT Director jobs in Dubai UAE",
        "CIO jobs in Bangalore India",
        "Chief Information Officer roles UAE"
    ]
    
    found_jobs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    for query in queries:
        print(f"🔍 Searching: {query}")
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extracting search results (Google results often use 'tF2Cxc' class)
            for g in soup.find_all('div', class_='tF2Cxc'):
                title = g.find('h3').text if g.find('h3') else "Executive Role"
                url = g.find('a')['href'] if g.find('a') else "#"
                
                # Filter for high-value job sites
                if any(site in url for site in ['linkedin.com', 'indeed.com', 'glassdoor', 'bayt.com']):
                    job_data = {
                        'Date': datetime.now().strftime("%Y-%m-%d"),
                        'Company': 'Verified Source',
                        'Role': title,
                        'Location': query.split('in ')[-1],
                        'URL': url,
                        'Status': 'New 🆕'
                    }
                    found_jobs.append(job_data)
        except Exception as e:
            print(f"⚠️ Search error for {query}: {e}")

    # --- SAVE AND NOTIFY ---
    if found_jobs:
        # 1. Update CSV for Streamlit
        new_df = pd.DataFrame(found_jobs)
        if os.path.exists(db_file):
            old_df = pd.read_csv(db_file)
            final_df = pd.concat([old_df, new_df], ignore_index=True).drop_duplicates(subset=['URL'])
        else:
            final_df = new_df
        
        final_df.to_csv(db_file, index=False)
        print(f"✅ Database updated with {len(found_jobs)} jobs.")

        # 2. Send Telegram Alert for the single best lead found
        top_job = found_jobs[0]
        alert_msg = (
            f"💼 *New Executive Lead Found!*\n\n"
            f"*Role:* {top_job['Role']}\n"
            f"*Location:* {top_job['Location']}\n\n"
            f"🔗 [View Opportunity]({top_job['URL']})\n\n"
            f"📱 _Check your Streamlit Dashboard for the full list._"
        )
        send_telegram_msg(alert_msg)
    else:
        print("poc: No new jobs detected this round.")
        # Fallback test message to confirm Telegram is working even if no jobs found
        send_telegram_msg("🤖 *Lobby-AI Status:* Scout ran successfully, but no new unique jobs were found in this cycle.")

if __name__ == "__main__":
    run_scout()
