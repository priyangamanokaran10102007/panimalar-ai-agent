import streamlit as st
import google.generativeai as genai
from pypdf import PdfReader

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
    st.error("❌ Gemini API key missing. Add it in Streamlit Secrets.")
    st.stop()

# Configure Gemini (STABLE SDK)
genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-flash")


# ---------------- UI ----------------
st.title("🏛️ PICA – Panimalar AI Assistant")
st.caption("Official AI Guide | Tamil + English | Panimalar Engineering College")

# ---------------- CORE KNOWLEDGE ----------------
CAMPUS_DATA = """
Panimalar Engineering College (Autonomous), Chennai.

Facilities:
- Asia’s largest college mess (2.45 lakh sq. ft)
- Separate vegetarian & non-vegetarian mess
- 100+ college buses
- Separate boys & girls hostels
- Wi-Fi enabled campus
- 24/7 medical care
- Strong placement training

Top Recruiters:
L&T, Infosys, Oracle, TCS, Tech Mahindra
"""

# ---------------- DEPARTMENT DATA ----------------
DEPARTMENTS = {
    "CSE": "Computer Science Engineering focuses on programming, AI, ML, and data structures.",
    "IT": "Information Technology focuses on software systems, networking, and databases.",
    "ECE": "Electronics and Communication focuses on VLSI and communication systems.",
    "EEE": "Electrical and Electronics focuses on power systems and machines.",
    "MECH": "Mechanical Engineering focuses on design, manufacturing, and thermal systems.",
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
        st.success("Admin access granted")

        pdf = st.file_uploader("📄 Upload College Notice / PDF", type=["pdf"])
        if pdf:
            reader = PdfReader(pdf)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            st.session_state.pdf_text = text
            st.success("PDF uploaded and indexed")

    elif pwd:
        st.error("Incorrect password")

# ---------------- CHAT HISTORY ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------- VOICE INPUT (SAFE PLACEHOLDER) ----------------
st.info("🎤 Tamil voice input will be enabled in future version (text-only for now).")

# ---------------- USER INPUT ----------------
question = st.chat_input("Panimalar pathi kelunga / Ask about Panimalar")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    # Conversation memory (last 6 messages)
    memory = ""
    for msg in st.session_state.messages[-6:]:
        memory += f"{msg['role']}: {msg['content']}\n"

    # ---------------- PROMPT ----------------
    prompt = f"""
You are **PICA**, the official AI assistant of Panimalar Engineering College.

STRICT RULES:
1. Answer ONLY questions related to Panimalar Engineering College.
2. Use ONLY the data provided below.
3. Respond in simple English + Tamil (Tanglish).
4. If the question is unrelated, politely refuse.

College Information:
{CAMPUS_DATA}

Department Information:
{DEPARTMENTS}

Admin Uploaded Notices (PDF):
{st.session_state.pdf_text}

Conversation History:
{memory}

User Question:
{question}

If unrelated, reply exactly:
"Sorry 😔 indha question Panimalar Engineering College-ku sambandham illa."
"""

    try:
        response = model.generate_content(prompt)
        answer = response.text or "⚠️ Enakku indha kelvikku badhil theriyala."
    except Exception as e:
        answer = f"❌ Error: {e}"

    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})


