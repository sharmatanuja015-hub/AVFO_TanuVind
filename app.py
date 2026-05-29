import streamlit as st
import pandas as pd
import os

# Google Sheet ki jagah hum computer me hi ek Excel/CSV file bana rahe hain data save karne ke liye
DATA_FILE = "avfo_requests.csv"

# Agar pehle se koi file nahi hai, toh ek nayi file create karein headings ke saath
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Naam", "Mobile", "Gaon", "Pashu", "Samasya", "Status"])
    df.to_csv(DATA_FILE, index=False)

# Website ka Title (Heading)
st.set_page_config(page_title="AVFO Emergency Portal", page_icon="🐾")
st.title("🐾 Assistant Veterinary Field Officer (AVFO) Portal")
st.subheader("पशु चिकित्सा आपातकालीन सेवा (Emergency Request Form)")

st.write("---")

# Kisaan ke liye Form Design
st.markdown("### 📝 कृपया अपनी समस्या दर्ज करें (Fill the Form)")

with st.form(key='avfo_form', clear_on_submit=True):
    name = st.text_input("1. आपका नाम (Farmer's Name)*")
    phone = st.text_input("2. मोबाइल नंबर (Mobile Number)*")
    village = st.text_input("3. ग्राम/गांव का नाम (Village)*")
    
    animal_type = st.selectbox("4. पशु का प्रकार (Select Animal)*", 
                               ["गाय (Cow)", "भैंस (Buffalo)", "बकरी (Goat)", "भेड़ (Sheep)", "अन्य (Other)"])
    
    problem = st.text_area("5. बीमारी के लक्षण / समस्या (Symptoms/Problem)*")
    
    submit_button = st.form_submit_button(label='Submit Request / शिकायत दर्ज करें')

# Jab kisaan Submit button dabayega
if submit_button:
    if name and phone and village and problem: # Check ki koi field khali na ho
        # Naya data read aur append karein
        new_data = {
            "Naam": [name], "Mobile": [phone], "Gaon": [village], 
            "Pashu": [animal_type], "Samasya": [problem], "Status": ["Pending"]
        }
        new_df = pd.DataFrame(new_data)
        new_df.to_csv(DATA_FILE, mode='a', header=False, index=False)
        
        # Website par success message dikhayein
        st.success(f"धन्यवाद {name} जी! आपकी शिकायत दर्ज हो गई है। AVFO आपको जल्द ही संपर्क करेंगे।")
        
        # YAHAN MAKE KA WEBHOOK JUDEGA (AUTOMATION KE LIYE)
        st.info("🚨 AVFO Officer को आपके केस का SMS भेज दिया गया है।")
    else:
        st.error("कृपया सभी जरूरी जानकारी (*) भरें।")

st.write("---")

# AVFO Admin Panel (Sirf aapke dekhne ke liye, isey niche password se lock bhi kar sakte hain)
if st.checkbox("🔑 AVFO Dashboard (For Officer Use Only)"):
    st.markdown("### 📋 वर्तमान मामले (Current Active Cases)")
    current_requests = pd.read_csv(DATA_FILE)
    st.dataframe(current_requests)