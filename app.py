\import streamlit as st
import pandas as pd

# Set up the page for Mobile
st.set_page_config(page_title="Lobby-AI Executive Scout", layout="centered")

st.title("💼 Executive Job Hub")
st.subheader("Real-time Global Leads")

# Load the Database from your GitHub
try:
    df = pd.read_csv('job_database.csv')
    
    # Show statistics
    col1, col2 = st.columns(2)
    col1.metric("Total Leads", len(df))
    col2.metric("New Today", len(df[df['Status'] == 'New']))

    st.markdown("---")

    # Display Jobs as Cards
    for index, row in df.iterrows():
        with st.container():
            st.write(f"### {row['Role']}")
            st.write(f"**{row['Company']}** | 📍 {row['Location']}")
            st.write(f"📅 Found: {row['Date']}")
            
            # Button to open the job link
            st.link_button("View Job / Apply", row['URL'])
            st.markdown("---")

except Exception as e:
    st.error("Database is warming up. Please check back in a moment!")
    st.info("Make sure 'job_database.csv' exists in your GitHub repository.")
