import os
import pandas as pd
from datetime import datetime

def run_scout():
    print("🛰️ Lobby-AI: Starting Global Executive Scout...")
    
    # 1. This is where your scouting logic lives. 
    # For now, we generate a 'found' list to ensure the database sync works.
    found_jobs = [
        {
            "Company": "Global Tech Corp", 
            "Role": "IT Head", 
            "Location": "Nigeria", 
            "URL": "https://linkedin.com/jobs/example1"
        },
        {
            "Company": "Digital UAE", 
            "Role": "Head of Infrastructure", 
            "Location": "UAE", 
            "URL": "https://linkedin.com/jobs/example2"
        }
    ]
    
    # 2. Sync to the Database (CSV)
    db_file = 'job_database.csv'
    
    # Check if the file exists; if not, create it with headers
    if os.path.exists(db_file):
        df = pd.read_csv(db_file)
    else:
        df = pd.DataFrame(columns=['Date', 'Company', 'Role', 'Location', 'URL', 'Status'])

    # 3. Process new jobs
    new_data = pd.DataFrame(found_jobs)
    new_data['Date'] = datetime.now().strftime("%Y-%m-%d")
    new_data['Status'] = 'New'
    
    # Combine and remove duplicates based on the URL
    updated_df = pd.concat([df, new_data]).drop_duplicates(subset=['URL'], keep='first')
    
    # Save back to GitHub
    updated_df.to_csv(db_file, index=False)
    print(f"✅ Success: {len(found_jobs)} jobs processed and synced to database.")

if __name__ == "__main__":
    run_scout()
