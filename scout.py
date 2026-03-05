import os
import pandas as pd
from datetime import datetime

def run_scout():
    print("🚀 Lobby-AI: Starting Clean Scout...")
    db_file = 'job_database.csv'
    
    # Create file if missing
    if not os.path.exists(db_file):
        df = pd.DataFrame(columns=['Date', 'Company', 'Role', 'Location', 'URL', 'Status'])
        df.to_csv(db_file, index=False)
        print("📁 New database created.")

    # Add a success marker
    new_entry = {
        'Date': datetime.now().strftime("%Y-%m-%d"),
        'Company': 'Lobby-AI System',
        'Role': 'Cloud Agent',
        'Location': 'GitHub Cloud',
        'URL': 'https://github.com/check',
        'Status': 'Operational ✅'
    }
    
    df = pd.read_csv(db_file)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(db_file, index=False)
    print("✅ Success: Data synced to GitHub!")

if __name__ == "__main__":
    run_scout()
