import os
import pandas as pd
from datetime import datetime

def run_scout():
    print("🚀 Lobby-AI: Starting Light Scout...")
    db_file = 'job_database.csv'
    
    # Safety Check: Create file if it's missing
    if not os.path.exists(db_file):
        df = pd.DataFrame(columns=['Date', 'Company', 'Role', 'Location', 'URL', 'Status'])
        df.to_csv(db_file, index=False)
        print("📁 Created new database file.")

    # Add a success marker to the database
    new_entry = {
        'Date': datetime.now().strftime("%Y-%m-%d"),
        'Company': 'System Check',
        'Role': 'Cloud Agent',
        'Location': 'GitHub Cloud',
        'URL': 'https://github.com',
        'Status': 'Operational ✅'
    }
    
    df = pd.read_csv(db_file)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(db_file, index=False)
    print("✅ System Check Complete: Database Updated.")

if __name__ == "__main__":
    run_scout()
