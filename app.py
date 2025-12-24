import streamlit as st
from google import genai
import PyPDF2

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="PICA – Panimalar AI Assistant",
    page_icon="🏛️",
    layout="centered"
)

# ---------------- API + ADMIN ----------------
api_key = st.secrets.get("GEMINI_API_KEY")
admin_password = st.secrets.get("ADMIN_PASSWORD")

if not api_key:
    st.error("❌ Gemini API key missing.")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------------- UI ----------------
st.title("🏛️ PICA – Panimalar AI Assistant")
st.caption("Official AI guide | Tamil + English | Panimalar Engineering College")

# ---------------- CORE KNOWLEDGE ----------------
CAMPUS_DATA = """
Panimalar Engineering College (Autonomous), Chennai.

Facilities:
- Asia’s largest college mess (2.45 lakh sq. ft)
- Separate veg & non-veg mess
- 100+ college buses
- Boys & Girls hostels
- Wi-Fi, 24/7 medical care
- Strong placement training

Top Recruiters:
L&T, Infosys, Oracle, TCS, Tech Mahindra
"""

# ---------------- DEPARTMENT DATA ----------------
DEPARTMENTS = {
    "CSE": "Computer Science Engineering focuses on programming, AI, ML, data structures.",
    "IT": "Information Technology focuses on software systems, networks, databases.",
    "ECE": "Electronics and Communication focuses on VLSI, communication systems.",
    "EEE": "Electrical and Electronics focuses on power systems and machines.",
    "MECH": "Mechanical Engineering focuses on design, manufacturing, thermal systems.",
    "CIVIL": "Civil Engineering focuses on construction, structures, and surveying."
}

# ---------------- SESSION STATE ----------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""

# ---------------- ADMIN PANEL ----------------
with st.sidebar:
    st.header("🔐 Admin Panel")
    pwd = st.text_input("Admin Password", type="password")

    if pwd == admin_password:
        st.success("Admin Access Granted")

        pdf = st.file_uploader("📄 Upload Notice / PDF", type=["pdf"])
        if pdf:
            reader = PyPDF2.PdfReader(pdf)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            st.session_state.pdf_text = text
            st.success("PDF uploaded & indexed")

    elif pwd:
        st.error("Wrong password")

# ---------------- CHAT HISTORY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- VOICE INPUT (Tamil) ----------------
audio = st.audio_input("🎤 Tamil voice input (optional)")

voice_text = ""
if audio:
    response = client.models.generate_content(
        model="models/gemini-1.5-flash",
        contents=audio
    )
    voice_text = response.text
    st.info(f"🎙️ You said: {voice_text}")

# ---------------- USER INPUT ----------------
question = st.chat_input("Panimalar pathi kelunga / Ask about Panimalar")

final_question = voice_text if voice_text else question

if final_question:
    st.session_state.messages.append({"role": "user", "content": final_question})
    with st.chat_message("user"):
        st.markdown(final_question)

    # MEMORY
    memory = ""
    for msg in st.session_state.messages[-6:]:
        memory += f"{msg['role']}: {msg['content']}\n"

    # PROMPT
    prompt = f"""
You are **PICA**, official AI assistant of Panimalar Engineering College.

STRICT RULES:
- Answer ONLY Panimalar-related questions
- Respond in Tamil + English (Tanglish)
- Use ONLY given data
- If unrelated → politely refuse

College Info:
{CAMPUS_DATA}

Departments:
{DEPARTMENTS}

Admin Notices (PDF):
{st.session_state.pdf_text}

Conversation Memory:
{memory}

User Question:
{final_question}

If unrelated reply:
"Sorry 😔 indha question Panimalar-ku sambandham illa."
"""

    try:
        response = client.models.generate_content(
            model="models/gemini-1.5-flash",
            contents=prompt
        )
        answer = response.text
    except Exception as e:
        answer = f"❌ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

