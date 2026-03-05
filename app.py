import streamlit as st
import docx
import requests
import asyncio
import time
import random
from playwright.async_api import async_playwright

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(page_title="Lobby-AI Global Executive", layout="wide", page_icon="🌎")

st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stButton>button { background-color: #0f172a; color: white; border-radius: 8px; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #334155; border: 1px solid #38bdf8; }
    .country-card { background: white; padding: 10px; border-radius: 8px; border-left: 5px solid #38bdf8; margin-bottom: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# --- 2. GLOBAL DATA & CONFIG ---
african_hubs = ["Nigeria", "Kenya", "Ethiopia", "Tanzania", "South Africa"]
other_hubs = ["India", "UAE", "UK", "USA", "Singapore"]
all_countries = african_hubs + other_hubs

executive_roles = ["IT Head", "Senior IT Manager", "Head of Digital Transformation", "VP IT", "CIO", "CTO"]

# --- 3. STEALTH SCOUTING ENGINE (SIMULATED) ---
async def stealth_scout(url, country):
    """Mimics human browsing to avoid blacklisting."""
    # In a real deployment, you would run playwright here.
    # This simulation follows the 'Human-Jitter' rules we discussed.
    time.sleep(random.uniform(1.5, 3.5)) 
    return {
        "company": f"{country} Global Tech",
        "role": "Head of IT Operations",
        "score": random.randint(85, 95),
        "gaps": ["Disaster Recovery", "ISO 27001", "Regional Compliance"],
        "jd": f"Seeking an IT leader in {country} to manage infrastructure and WhatsApp-based automation flows."
    }

# --- 4. SIDEBAR CONTROLS ---
with st.sidebar:
    st.title("🛡️ Lobby-AI Command")
    uploaded_cv = st.file_uploader("Upload Master CV (.docx)", type="docx")
    
    st.divider()
    target_roles = st.multiselect("Designations", executive_roles, default=["IT Head"])
    
    select_all = st.checkbox("Target All Countries")
    target_countries = all_countries if select_all else st.multiselect("Target Countries", all_countries, default=["Nigeria", "India"])
    
    if uploaded_cv:
        doc = docx.Document(uploaded_cv)
        st.session_state.resume_text = "\n".join([p.text for p in doc.paragraphs])
        st.success("CV Loaded & Ready")

# --- 5. MAIN INTERFACE ---
if 'view' not in st.session_state: st.session_state.view = 'home'

if st.session_state.view == 'home':
    st.title("Global Executive Career Agent")
    st.info(f"Ready to scout across {len(target_countries)} countries for {len(target_roles)} leadership roles.")

    if st.button("🚀 START GLOBAL SCOUT"):
        if not uploaded_cv:
            st.warning("Please upload your Master CV first.")
        else:
            with st.spinner("Scouting Job Boards with Stealth AI..."):
                # Mocking the discovery of a high-value match
                st.session_state.match = asyncio.run(stealth_scout("https://linkedin.com", target_countries[0]))
                st.session_state.view = 'review'
                st.rerun()

elif st.session_state.view == 'review':
    m = st.session_state.match
    st.title(f"Match Found: {m['role']} in {m['company']}")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.metric("Alignment Score", f"{m['score']}%")
        st.write(f"**Job Summary:** {m['jd']}")
    with col2:
        if st.button("New Search"):
            st.session_state.view = 'home'
            st.rerun()

    st.divider()

    # THE BRIDGE (Zero-Cost Tailoring)
    st.subheader("⚠️ Strategic Skill Gaps")
    st.write("Click to bridge these requirements using your Lobby-AI experience:")
    
    gap_cols = st.columns(len(m['gaps']))
    for i, gap in enumerate(m['gaps']):
        if gap_cols[i].button(f"Inject {gap}", key=gap):
            bridge_phrase = f"\n• Orchestrated {gap} protocols within the Lobby-AI booking system to ensure high-availability."
            st.session_state.resume_text += bridge_phrase
            st.toast(f"Added {gap} to your CV!")

    st.divider()

    # FINAL REVIEW & MAKE.COM SYNC
    st.subheader("📄 Tailored Executive Document")
    final_text = st.text_area("Final Polish", st.session_state.resume_text, height=350)

    if st.button("✅ FINALIZE & SEND TO TELEGRAM"):
        # This sends to your Make.com Webhook (FREE)
        webhook_url = "https://hook.eu1.make.com/yqy3wmxomg9e5536qiokz0kja3vwgart"
        payload = {"cv_content": final_text, "role": m['role'], "company": m['company']}
        
        try:
            requests.post(webhook_url, json=payload)
            st.balloons()
            st.success("Success! Your tailored CV is being sent to your Telegram.")
        except:
            st.error("Connection to Make.com failed. Ensure your Webhook is ON.")
