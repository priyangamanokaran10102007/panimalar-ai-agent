import streamlit as st
from google import genai

# ---------------- PAGE CONFIG (MUST BE FIRST) ----------------
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

# ✅ Correct client initialization (NEW SDK)
client = genai.Client(api_key=api_key)

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
- Separate hostels for boys and girls
- 24/7 medical care
- Wi-Fi enabled
- Strict discipline
"""

# ---------------- CHAT STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- CHAT INPUT ----------------
question = st.chat_input("Ask anything about Panimalar or general questions")

if question:
    # User message
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    try:
        prompt = f"""
You are **PICA**, an AI assistant for Panimalar Engineering College.

If the question is about Panimalar, use this data:
{CAMPUS_DATA}

If it is a general question, answer normally.

Be clear, polite, and student-friendly.

Question:
{question}
"""
response = client.models.generate_content(
    model="gemini-1.0-pro",
    contents=prompt
)

       
        )

        answer = response.text or "⚠️ I couldn’t generate a response."

    except Exception as e:
        answer = f"❌ Error: {e}"

    # Assistant message
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})











