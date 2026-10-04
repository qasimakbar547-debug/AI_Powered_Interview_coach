import streamlit as st
import json
import html

from database import create_tables, save_interview, get_interview_history
from auth import show_auth
from ai_coach import evaluate_answer, generate_final_report


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       MAIN APP
    ========================= */

    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }


    /* =========================
       SIDEBAR
    ========================= */

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        font-size: 15px;
        padding: 6px 0;
    }


    /* =========================
       HEADINGS
    ========================= */

    h1, h2, h3 {
        color: #111827;
    }

    h1 {
        font-weight: 800;
    }


    /* =========================
       HERO
    ========================= */

    .hero {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #2563eb 55%,
            #7c3aed 100%
        );

        padding: 38px;
        border-radius: 24px;
        color: white;
        margin-bottom: 30px;

        box-shadow: 0 15px 35px rgba(37, 99, 235, 0.20);
    }

    .hero h1 {
        color: white;
        font-size: 42px;
        margin-bottom: 8px;
    }

    .hero p {
        color: #e5e7eb;
        font-size: 17px;
        margin-bottom: 0;
    }


    /* =========================
       CARDS
    ========================= */

    .card {
        background: white;
        padding: 25px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
        margin-bottom: 20px;
    }

    .stat-card {
        background: white;
        padding: 24px;
        border-radius: 18px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
        text-align: center;
    }

    .stat-number {
        font-size: 32px;
        font-weight: 800;
        color: #2563eb;
    }

    .stat-label {
        color: #6b7280;
        font-size: 14px;
    }


    /* =========================
       QUESTION CARD
    ========================= */

    .question-card {
        background: white;
        padding: 32px;
        border-radius: 20px;
        border-left: 6px solid #2563eb;
        box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
        margin: 20px 0;
    }

    .question-number {
        color: #2563eb;
        font-weight: 700;
        font-size: 14px;
        margin-bottom: 10px;
    }

    .question-text {
        color: #111827;
        font-size: 25px;
        font-weight: 700;
        line-height: 1.4;
    }


    /* =========================
       RESULT CARD
    ========================= */

    .result-card {
        background: white;
        padding: 28px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.07);
        margin-top: 20px;
    }

    .score {
        font-size: 48px;
        font-weight: 800;
        color: #2563eb;
    }

    .result-title {
        font-size: 18px;
        font-weight: 700;
        color: #111827;
        margin-top: 15px;
    }

    .result-text {
        color: #4b5563;
        line-height: 1.7;
    }


    /* =========================
       PROFILE
    ========================= */

    .profile-card {
        background: white;
        padding: 30px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    }

    .profile-name {
        font-size: 30px;
        font-weight: 800;
        color: #111827;
    }

    .profile-email {
        color: #6b7280;
        font-size: 16px;
    }


    /* =========================
       BUTTONS
    ========================= */

    .stButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 45px;
        border: none;
        transition: 0.2s;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
    }


    /* =========================
       INPUTS
    ========================= */

    textarea,
    input,
    select {
        border-radius: 10px !important;
    }


    /* =========================
       FOOTER
    ========================= */

    .footer {
        text-align: center;
        color: #6b7280;
        padding: 35px 10px 10px 10px;
        font-size: 13px;
    }


    /* =========================
       HISTORY
    ========================= */

    .history-card {
        background: white;
        padding: 20px;
        border-radius: 16px;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
        box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
    }

    .history-category {
        font-size: 18px;
        font-weight: 700;
        color: #111827;
    }

    .history-date {
        color: #6b7280;
        font-size: 13px;
    }


    /* =========================
       REMOVE STREAMLIT MENU
    ========================= */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# DATABASE
# =========================================================

create_tables()


# =========================================================
# SESSION STATE
# =========================================================

defaults = {
    "logged_in": False,
    "user": None,

    "interview_started": False,
    "question_index": 0,

    "answers": [],
    "results": [],

    "final_report": "",

    "category": "",
    "number_of_questions": 5,

    "answer_evaluated": False,
    "current_result": None,
    "current_answer": "",

    "interview_saved": False,

    "interview_session_id": 0,

    "nav_page": "🏠 Dashboard"
}


for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# LOAD QUESTIONS
# =========================================================

def load_questions():
    try:
        with open("questions.json", "r", encoding="utf-8") as file:
            return json.load(file)

    except FileNotFoundError:
        st.error(
            "❌ questions.json file نہیں ملی۔ "
            "براہِ کرم check کریں کہ questions.json اسی folder میں موجود ہے۔"
        )
        return {}

    except json.JSONDecodeError:
        st.error(
            "❌ questions.json میں JSON format کی غلطی ہے۔"
        )
        return {}

    except Exception as error:
        st.error(f"❌ Questions load نہیں ہو سکے: {error}")
        return {}


questions_data = load_questions()


# =========================================================
# RESET INTERVIEW
# =========================================================

def reset_interview():

    st.session_state.interview_started = False
    st.session_state.question_index = 0

    st.session_state.answers = []
    st.session_state.results = []

    st.session_state.final_report = ""

    st.session_state.category = ""

    st.session_state.answer_evaluated = False
    st.session_state.current_result = None
    st.session_state.current_answer = ""

    st.session_state.interview_saved = False

    st.session_state.interview_session_id += 1


# =========================================================
# LOGOUT
# =========================================================

def logout():

    reset_interview()

    st.session_state.logged_in = False
    st.session_state.user = None

    st.session_state.nav_page = "🏠 Dashboard"

    st.rerun()


# =========================================================
# LOGIN / SIGNUP
# =========================================================

if not st.session_state.logged_in:

    show_auth()

    st.markdown(
        """
        <div class="footer">
            🎤 AI Interview Coach • Practice smarter, interview better.
        </div>
        """,
        unsafe_allow_html=True
    )

    st.stop()


# =========================================================
# USER INFORMATION
# =========================================================

user = st.session_state.user

if isinstance(user, dict):

    user_name = user.get("name", "User")
    user_email = user.get("email", "")

else:

    user_name = "User"
    user_email = ""


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px 0 25px 0;
        ">
            <div style="font-size:45px;">🎤</div>
            <h2 style="margin:0;">AI Interview Coach</h2>
            <p style="
                color:#cbd5e1 !important;
                font-size:13px;
            ">
                Practice • Improve • Succeed
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            background:rgba(255,255,255,0.08);
            padding:15px;
            border-radius:12px;
            margin-bottom:20px;
        ">
            <b>👋 Welcome</b><br>
            <span style="font-size:14px;">
                {html.escape(user_name)}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🎤 New
