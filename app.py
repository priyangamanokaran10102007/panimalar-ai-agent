import streamlit as st
import google.generativeai as genai

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
st.set_page_config(
    page_title="PICA: Panimalar AI Assistant",
    page_icon="🏛️",
    layout="centered"
)

# ---------------- API KEY CHECK ----------------
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ GEMINI_API_KEY not found in Streamlit secrets")
    st.stop()

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# ---------------- APP TITLE ----------------
st.title("🏛️ PICA: Panimalar Campus AI Assistant")
st.markdown("Your 24/7 guide to **Panimalar Engineering College**")

# ---------------- KNOWLEDGE BASE ----------------
CAMPUS_DATA = """
Panimalar Engineering College (Autonomous) is located in Chennai, Varadharajapuram.

Mess:
- One of Asia’s largest college mess facilities (2.45 lakh sq. ft)
- Separate Veg and Non-Veg dining
- Hygienic environment

Transport:
- 100+ college buses covering Chennai, Kancheepuram, Thiruvallur

Placements:
- Recruiters include L&T, Tech Mahindra, Oracle, Infosys, TCS

Hostels:
- Separate hostels for boys and girls
- 24/7 medical care
- Wi-Fi enabled
- Strict discipline
"""

# ---------------- CHAT HISTORY ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- USER INPUT ----------------
user_prompt = st.chat_input("Ask about mess, transport, hostel, placements...")

if user_prompt:
    # Store user message
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # ---------------- GEMINI RESPONSE ----------------
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        full_prompt = f"""
You are PICA, an AI assistant for Panimalar Engineering College.

Use the following campus data when relevant:
{CAMPUS_DATA}

If the question is not about Panimalar, answer normally.

Student question:
{user_prompt}
"""

        response = model.generate_content(full_prompt)
        reply = response.text if response.text else "⚠️ No response generated."

    except Exception as e:
        reply = f"❌ Error generating response: {e}"

    # Assistant reply
    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})





