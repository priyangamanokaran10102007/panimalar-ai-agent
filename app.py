import streamlit as st
from google import genai


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PICA: Panimalar AI Assistant",
    page_icon="🏛️",
    layout="centered"
)

# ---------------- API KEY ----------------
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("❌ Gemini API key missing. Add it in Streamlit Secrets.")
    st.stop()

genai.configure(api_key=api_key)

# ---------------- TITLE ----------------
st.title("🏛️ PICA: Panimalar Campus AI Assistant")
st.markdown("Your 24/7 guide to **Panimalar Engineering College**")

# ---------------- KNOWLEDGE BASE ----------------
CAMPUS_DATA = """
Panimalar Engineering College (Autonomous) is located in Chennai, Varadharajapuram.

Mess:
- One of Asia’s largest college mess facilities (2.45 lakh sq. ft)
- Separate Veg and Non-Veg dining

Transport:
- 100+ college buses (Chennai, Kancheepuram, Thiruvallur)

Placements:
- L&T, Tech Mahindra, Oracle, Infosys, TCS

Hostels:
- Separate hostels
- 24/7 medical care
- Wi-Fi enabled
- Strict discipline
"""

# ---------------- CHAT STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# ---------------- CHAT INPUT ----------------
question = st.chat_input("Ask anything about Panimalar or general questions")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    try:
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are PICA, an AI assistant for Panimalar Engineering College.

Use this information when relevant:
{CAMPUS_DATA}

Answer clearly and politely.

Question:
{question}
"""
        response = model.generate_content(prompt)
        answer = response.text or "⚠️ No response generated."

    except Exception as e:
        answer = f"❌ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})








