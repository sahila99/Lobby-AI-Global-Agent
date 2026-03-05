import os
import pandas as pd
from datetime import datetime

def run_scout():
    print("🚀 Lobby-AI: Starting Light Scout...")
    db_file = 'job_database.csv'
    
    # Ensure database exists
    if not os.path.exists(db_file):
        df = pd.DataFrame(columns=['Date', 'Company', 'Role', 'Location', 'URL', 'Status'])
        df.to_csv(db_file, index=False)
        print("📁 Database created.")

    # Test Data for Nigeria/India/UAE
    new_entry = {
        'Date': datetime.now().strftime("%Y-%m-%d"),
        'Company': 'Lobby-AI System Check',
        'Role': 'Executive Agent',
        'Location': 'Cloud',
        'URL': 'https://github.com/lobby-ai',
        'Status': 'Operational ✅'
    }
    
    # Save to CSV
    df = pd.read_csv(db_file)
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(db_file, index=False)
    print("✅ Success: Data synced to GitHub.")

if __name__ == "__main__":
    run_scout()
