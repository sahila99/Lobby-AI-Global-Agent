import os
import pandas as pd
from datetime import datetime

def run_scout():
    print("🚀 Lobby-AI: Starting Clean Scout...")
    db_file = 'job_database.csv'
    
    # 1. Ensure the database file exists
    if not os.path.exists(db_file):
        df = pd.DataFrame(columns=['Date', 'Company', 'Role', 'Location', 'URL', 'Status'])
        df.to_csv(db_file, index=False)
        print("📁 Created new database file.")

    # 2. Add a 'System Check' entry to prove it works
    new_entry = {
        'Date': datetime.now().strftime("%Y-%m-%d"),
        'Company': 'Lobby-AI Cloud',
        'Role': 'Executive Scout',
        'Location': 'Global-Cloud',
        'URL': 'https://github.com/lobby-ai',
        'Status': 'Operational ✅'
    }
    
    # 3. Load, Append, and Save
    df = pd.read_csv(db_file)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(db_file, index=False)
    
    print("✅ Success: Job database updated on GitHub!")

if __name__ == "__main__":
    run_scout()
