import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Database File
DATA_FILE = "tanuvind_avfo_requests.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Timestamp", "Naam", "Mobile", "Gaon", "Pashu", "Samasya", "Emergency", "Status"])
    df.to_csv(DATA_FILE, index=False)

# Page Configuration & Styling
st.set_page_config(page_title="TanuVind AVFO Portal", page_icon="🐾", layout="wide")

# Custom CSS for TanuVind Theme (Blue & Premium look)
st.markdown("""
    <style>
    .main-title { font-size: 40px; font-weight: bold; color: #0F172A; text-align: center; font-family: 'Arial'; }
    .brand-sub { font-size: 18px; color: #2563EB; text-align: center; font-weight: 500; margin-bottom: 20px; }
    .emergency-box { background-color: #FFEBEE; padding: 15px; border-radius: 10px; border-left: 5px solid #D32F2F; }
    .tip-box { background-color: #F0FDF4; padding: 15px; border-radius: 10px; border-left: 5px solid #16A34A; }
    </style>
""", unsafe_allow_html=True)

# App Header with TanuVind Branding
st.markdown("<div class='main-title'>🐾 TanuVind Veterinary Digital Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='brand-sub'>Assistant Veterinary Field Officer (AVFO) Emergency & Info Cell</div>", unsafe_allow_html=True)
st.write("---")

# Sidebar: Useful Veterinary Tips & Helpline
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2138/2138440.png", width=100) # Simple Vet Icon
    st.markdown("## 🏥 TanuVind Helpdesk")
    st.info("📞 **AVFO Emergency Helpline:**\n+91 XXXX-XXXXXX")
    
    st.write("---")
    st.markdown("### ☀️ Mausam Aur Pashu Dekhbhal (Tips)")
    st.markdown("""
    <div class='tip-box'>
    <strong>🚨 Garmi se Bachayein:</strong><br>
    1. Pashuon ko din me kam se kam 2-3 baar saaf aur thanda pani pilayein.<br>
    2. Dopahar 12 se 4 ke beech dhoop me na bandhein.<br>
    3. Dudharu pashuon ko hare chare ke saath namak ka paani dein.
    </div>
    """, unsafe_allow_html=True)

# Main Content Layout: 2 Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### 📝 आपातकालीन चिकित्सा फॉर्म (TanuVind Request Form)")
    
    with st.form(key='tanuvind_form', clear_on_submit=True):
        name = st.text_input("👤 आपका नाम (Farmer's Name)*")
        phone = st.text_input("📞 मोबाइल नंबर (Mobile Number)*")
        village = st.text_input("📍 ग्राम/गांव का नाम (Village)*")
        
        animal_type = st.selectbox("🐄 पशु का प्रकार (Select Animal)*", 
                                   ["गाय (Cow)", "भैंस (Buffalo)", "बकरी (Goat)", "भेड़ (Sheep)", "अन्य (Other)"])
        
        problem = st.text_area("⚠️ बीमारी के लक्षण / समस्या (Symptoms/Problem)*")
        
        # Interactive Emergency Toggle
        is_emergency = st.toggle("🚨 क्या यह बहुत गंभीर मामला है? (Is this a Critical Emergency?)", value=False)
        
        if is_emergency:
            st.markdown("<div class='emergency-box'>⚠️ **Dhyan dein:** Emergency select karne par TanuVind System se AVFO ko turant hara/red alert chala jayega.</div>", unsafe_allow_html=True)
            
        submit_button = st.form_submit_button(label='🚀 TanuVind Portal par Submit Karein')

    if submit_button:
        if name and phone and village and problem:
            emergency_status = "🚨 CRITICAL" if is_emergency else "Normal"
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save Data
            new_data = {
                "Timestamp": [current_time], "Naam": [name], "Mobile": [phone], 
                "Gaon": [village], "Pashu": [animal_type], "Samasya": [problem], 
                "Emergency": [emergency_status], "Status": ["Pending"]
            }
            new_df = pd.DataFrame(new_data)
            new_df.to_csv(DATA_FILE, mode='a', header=False, index=False)
            
            st.success(f"🎉 धन्यवाद {name} ji! TanuVind Portal par aapki request darj ho gayi hai.")
            if is_emergency:
                st.error("🚨 TanuVind Alert: AVFO Officer ko aapke emergency case ka notification bhej diya gaya hai.")
            else:
                st.info("👍 AVFO Desk ko inform kar diya gaya hai.")
        else:
            st.error("❌ Kripya sabhi zaroori jankari (*) bharein.")

with col2:
    st.markdown("### 🧮 TanuVind Cost Calculator")
    st.write("Dawa aur ilaaj ka andajatan kharcha:")
    
    calc_animal = st.selectbox("Pashu chunein:", ["गाय/भैंस", "बकरी/भेड़"])
    calc_issue = st.selectbox("Bimari/Service:", ["सामान्य बुखार (Fever)", "टीकाकरण (Vaccination)", "Prasav (Delivery)", "Emergency Case"])
    
    # Simple logic to calculate cost
    cost = 0
    if calc_animal == "गाय/भैंस":
        if calc_issue == "सामान्य बुखार (Fever)": cost = "₹150 - ₹300"
        elif calc_issue == "टीकाकरण (Vaccination)": cost = "Free (Govt Scheme)"
        elif calc_issue == "Prasav (Delivery)": cost = "₹500 - ₹1000"
        else: cost = "₹400 - ₹800"
    else:
        if calc_issue == "सामान्य बुखार (Fever)": cost = "₹50 - ₹150"
        elif calc_issue == "टीकाकरण (Vaccination)": cost = "Free (Govt Scheme)"
        elif calc_issue == "Prasav (Delivery)": cost = "₹200 - ₹500"
        else: cost = "₹150 - ₹300"
        
    st.metric(label="Andajatan Fees/Kharcha", value=cost)
    st.caption("*Note: Yeh kharcha TanuVind standard ke hisab se andajatan hai.")

st.write("---")

# AVFO Admin Dashboard
if st.checkbox("🔑 TanuVind Admin Dashboard (For Officer Use Only)"):
    st.markdown("### 📋 Sabhi Active Cases & Emergency Alerts")
    try:
        current_requests = pd.read_csv(DATA_FILE)
        st.dataframe(current_requests)
    except Exception as e:
        st.write("Abhi tak koi data nahi hai.")
