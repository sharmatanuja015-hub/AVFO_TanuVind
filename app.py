import streamlit as st
import pandas as pd
import os
import smtplib
from email.mime.text import MIMEText
from datetime import datetime

# --- 📧 EMAIL CONFIGURATION ---
SENDER_EMAIL = "your_email@gmail.com"      
SENDER_PASSWORD = "your_app_password"      
RECEIVER_EMAIL = "your_email@gmail.com"    

# --- 🔑 ADMIN PASSWORD (Aapka Dashboard Password) ---
ADMIN_PASSWORD = "TanuVind@2026"  # Aap is password ko badal sakte hain

# Database File
DATA_FILE = "tanuvind_avfo_requests.csv"

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Timestamp", "Naam", "Mobile", "Gaon", "Pashu", "Samasya", "Emergency", "Status"])
    df.to_csv(DATA_FILE, index=False)

# Function to Send Email Alert
def send_email_alert(name, phone, village, animal, problem, emergency_status):
    subject = f"🚨 TanuVind Alert: New Case Registered ({emergency_status})"
    body = f"""
    🚨 NAYA PASHU CHIKITSA CASE DARJ HUA HAI!
    
    👤 Kisaan/Owner ka Naam: {name}
    📞 Mobile Number: {phone}
    📍 Gaon / Shahar: {village}
    🐄 Pashu ka Prakar: {animal}
    ⚠️ Samasya / Lakshan: {problem}
    ⚡ Emergency Status: {emergency_status}
    
    ---
    TanuVind Care Digital System 🐾
    """
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECEIVER_EMAIL
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, msg.as_string())
        return True
    except Exception as e:
        return False

# Page Configuration
st.set_page_config(page_title="TanuVind AVFO Portal", page_icon="🐾", layout="centered")

st.markdown("""
    <style>
    .main-title { font-size: 38px; font-weight: bold; color: #0F172A; text-align: center; font-family: 'Arial'; margin-top: -20px; }
    .brand-sub { font-size: 18px; color: #2563EB; text-align: center; font-weight: 500; margin-bottom: 20px; }
    .emergency-box { background-color: #FFEBEE; padding: 15px; border-radius: 10px; border-left: 5px solid #D32F2F; margin-bottom: 15px; }
    .tip-box { background-color: #F0FDF4; padding: 15px; border-radius: 10px; border-left: 5px solid #16A34A; }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
col_img1, col_img2, col_img3 = st.columns([1, 1, 1])
with col_img2:
    st.image("https://cdn-icons-png.flaticon.com/512/616/616408.png", width=150, caption="TanuVind Care")

st.markdown("<div class='main-title'>🐾 TanuVind Veterinary Digital Portal</div>", unsafe_allow_html=True)
st.markdown("<div class='brand-sub'>Assistant Veterinary Field Officer (AVFO) Emergency & Info Cell</div>", unsafe_allow_html=True)
st.write("---")

# Sidebar
with st.sidebar:
    st.markdown("## 🏥 TanuVind Helpdesk")
    st.info("📞 **AVFO Emergency Helpline:**\n+91 XXXX-XXXXXX")
    st.write("---")
    st.markdown("### ☀️ Mausam Aur Pashu Dekhbhal (Tips)")
    st.markdown("""
    <div class='tip-box'>
    <strong>🚨 Garmi se Bachayein:</strong><br>
    1. Pashuon ko din me kam se kam 2-3 baar saaf aur thanda pani pilayein.<br>
    2. Kutta/Billi ko dhoop me khadi gaadi me akela na chhodhein.<br>
    3. Dudharu pashuon ko hare chare ke saath namak ka paani dein.
    </div>
    """, unsafe_allow_html=True)

# --- MAIN FORM SECTION ---
st.markdown("### 📝 आपातकालीन चिकित्सा फॉर्म (TanuVind Request Form)")

with st.form(key='tanuvind_form', clear_on_submit=True):
    name = st.text_input("👤 आपका नाम / मालिक का नाम (Owner's Name)*")
    phone = st.text_input("📞 मोबाइल नंबर (Mobile Number)*")
    village = st.text_input("📍 ग्राम / शहर का नाम (Village/City)*")
    animal_type = st.selectbox("🐄 पशु का प्रकार (Select Animal)*", ["गाय (Cow)", "भैंस (Buffalo)", "बकरी (Goat)", "कुत्ता (Dog)", "बिल्ली (Cat)", "अन्य (Other)"])
    problem = st.text_area("⚠️ बीमारी के लक्षण / समस्या (Symptoms/Problem)*")
    is_emergency = st.toggle("🚨 क्या यह बहुत गंभीर मामला है? (Is this a Critical Emergency?)", value=False)
    
    if is_emergency:
        st.markdown("<div class='emergency-box'>⚠️ **Dhyan dein:** Emergency select karne par TanuVind System se AVFO ko turant alert chala jayega.</div>", unsafe_allow_html=True)
        
    submit_button = st.form_submit_button(label='🚀 TanuVind Portal par Submit Karein')

if submit_button:
    if name and phone and village and problem:
        emergency_status = "🚨 CRITICAL EMERGENCY" if is_emergency else "Normal Case"
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
        
        with st.spinner("📧 Email notification bheja aa raha hai..."):
            mail_sent = send_email_alert(name, phone, village, animal_type, problem, emergency_status)
            if mail_sent:
                st.info("📩 AVFO Desk ko email alert kamyabi se bhej diya gaya hai.")
            else:
                st.warning("⚠️ Request save ho gayi hai par email bhejte waqt dikkat aayi.")
    else:
        st.error("❌ Kripya sabhi zaroori jankari (*) bharein.")

st.write("---")

# --- PASSWORD PROTECTED AVFO ADMIN DASHBOARD ---
# Normal users ko sirf ek simple checkbox dikhega, bina password ke data nahi dikhega
if st.checkbox("🔑 AVFO Dashboard (🔒 Staff Only)"):
    password_input = st.text_input("Enter Admin Security PIN/Password:", type="password")
    
    if password_input == ADMIN_PASSWORD:
        st.success("🔓 Access Granted! Welcome Officer.")
        st.markdown("### 📋 Sabhi Active Cases & Emergency Alerts")
        try:
            current_requests = pd.read_csv(DATA_FILE)
            st.dataframe(current_requests)
        except Exception as e:
            st.write("Abhi tak koi data nahi hai.")
    elif password_input:
        st.error("❌ Galat Password! Aapko data dekhne ki permission nahi hai.")
            st.write("Abhi tak koi data nahi hai.")
    elif password_input:
        st.error("❌ Galat Password! Aapko data dekhne ki permission nahi hai.")
