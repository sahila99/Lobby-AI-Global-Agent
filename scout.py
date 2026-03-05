import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def run_scout():
    print("🚀 Lobby-AI: Starting Real-Time Executive Scout...")
    db_file = 'job_database.csv'
    
    # Target Roles and Locations
    queries = [
        "Head of IT jobs in Lagos Nigeria",
        "IT Director jobs in Dubai UAE",
        "CIO jobs in Bangalore India",
        "Head of Information Technology jobs India"
    ]
    
    found_jobs = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

    for query in queries:
        print(f"🔍 Searching for: {query}")
        search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # This logic finds links in Google Search results
            for g in soup.find_all('div', class_='tF2Cxc'):
                title = g.find('h3').text if g.find('h3') else "Executive Role"
                url = g.find('a')['href'] if g.find('a') else "#"
                
                # Filter to ensure we only get high-quality links (LinkedIn, Indeed, etc.)
                if any(site in url for site in ['linkedin.com', 'indeed.com', 'glassdoor']):
                    found_jobs.append({
                        'Date': datetime.now().strftime("%Y-%m-%d"),
                        'Company': 'Verified Lead',
                        'Role': title,
                        'Location': query.split('in ')[-1],
                        'URL': url,
                        'Status': 'New 🆕'
                    })
        except Exception as e:
            print(f"⚠️ Error scouting {query}: {e}")

    # Save to Database
    if found_jobs:
        new_df = pd.DataFrame(found_jobs)
        if os.path.exists(db_file):
            old_df = pd.read_csv(db_file)
            final_df = pd.concat([old_df, new_df], ignore_index=True).drop_duplicates(subset=['URL'])
        else:
            final_df = new_df
        
        final_df.to_csv(db_file, index=False)
        print(f"✅ Success: {len(found_jobs)} new leads added to Lobby-AI.")
    else:
        print("poc: No new leads found in this cycle.")

if __name__ == "__main__":
    run_scout()
