import streamlit as st
import google.generativeai as genai

# 1. Setup API Key (Get yours from Google AI Studio)
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# 2. Define the Panimalar Knowledge Base
CAMPUS_DATA = """
Panimalar Engineering College (Autonomous) is located in Chennai, Varadharajapuram. 
Mess: It is famous for its massive mess (2.45 lakh sq. ft). Separate dining for Veg and Non-Veg. 
Transport: Over 100+ buses covering Chennai, Kancheepuram, and Thiruvallur.
Placements: Major partners include L&T, Tech Mahindra, and Oracle. 
Hostels: 24/7 medical and water supply, Wi-Fi enabled, and strict discipline.
"""

st.set_page_config(page_title="PICA: Panimalar AI Assistant")
st.title("🏛️ PICA: Panimalar Campus Agent")
st.markdown("Your 24/7 guide to life at Panimalar Engineering College.")

# 3. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about mess, transport, or placements..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # 4. AI Response Generation
    model = genai.GenerativeModel('gemini-1.5-flash')
    full_prompt = f"Using this data: {CAMPUS_DATA}. Answer the student's question: {prompt}"
    
    response = model.generate_content(full_prompt)
    
    with st.chat_message("assistant"):
        st.markdown(response.text)
    st.session_state.messages.append({"role": "assistant", "content": response.text})
