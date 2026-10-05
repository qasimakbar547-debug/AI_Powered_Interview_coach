import streamlit as st
import json

from database import (
    create_tables,
    save_interview,
    get_interview_history
)

from auth import show_auth

from ai_coach import (
    evaluate_answer,
    generate_final_report
)


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
# CUSTOM CSS — MODERN AI DESIGN
# =========================================================

st.markdown("""
<style>

    /* ---------- Main Background ---------- */

    .stApp {
        background:
            radial-gradient(
                circle at top left,
                rgba(99, 102, 241, 0.12),
                transparent 35%
            ),
            radial-gradient(
                circle at top right,
                rgba(14, 165, 233, 0.10),
                transparent 30%
            ),
            #f8fafc;
    }


    /* ---------- Main Container ---------- */

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }


    /* ---------- Hide Streamlit Branding ---------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }


    /* ---------- Hero ---------- */

    .hero {
        background:
            linear-gradient(
                135deg,
                #111827 0%,
                #1e3a8a 55%,
                #2563eb 100%
            );

        padding: 40px;
        border-radius: 28px;
        color: white;
        margin-bottom: 28px;

        box-shadow:
            0 20px 45px rgba(37, 99, 235, 0.18);
    }

    .hero-title {
        font-size: 46px;
        font-weight: 800;
        line-height: 1.1;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        font-size: 18px;
        color: #dbeafe;
        line-height: 1.7;
    }


    /* ---------- Cards ---------- */

    .card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;

        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.06);

        margin-bottom: 20px;
    }


    /* ---------- Stat Cards ---------- */

    .stat-card {
        background: white;
        padding: 24px;
        border-radius: 20px;
        border: 1px solid #e5e7eb;

        box-shadow:
            0 8px 25px rgba(15, 23, 42, 0.05);

        min-height: 140px;
    }

    .stat-icon {
        font-size: 28px;
    }

    .stat-title {
        color: #64748b;
        font-size: 14px;
        margin-top: 8px;
    }

    .stat-value {
        color: #0f172a;
        font-size: 32px;
        font-weight: 800;
        margin-top: 5px;
    }


    /* ---------- Question Card ---------- */

    .question-card {
        background:
            linear-gradient(
                135deg,
                #eff6ff,
                #ffffff
            );

        padding: 30px;
        border-radius: 24px;

        border: 1px solid #bfdbfe;

        box-shadow:
            0 10px 30px rgba(37, 99, 235, 0.08);

        margin: 20px 0;
    }

    .question-label {
        color: #2563eb;
        font-weight: 700;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .question-text {
        color: #0f172a;
        font-size: 24px;
        font-weight: 700;
        line-height: 1.5;
        margin-top: 10px;
    }


    /* ---------- AI Result ---------- */

    .result-card {
        background:
            linear-gradient(
                135deg,
                #f0fdf4,
                #ffffff
            );

        border: 1px solid #bbf7d0;

        padding: 28px;
        border-radius: 22px;

        box-shadow:
            0 10px 30px rgba(22, 163, 74, 0.07);

        margin: 20px 0;
    }


    /* ---------- Score ---------- */

    .score-card {
        background:
            linear-gradient(
                135deg,
                #fef3c7,
                #ffffff
            );

        border: 1px solid #fde68a;

        padding: 25px;
        border-radius: 20px;

        text-align: center;
        margin: 20px 0;
    }

    .score-number {
        font-size: 52px;
        font-weight: 900;
        color: #d97706;
    }


    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 14px;
        min-height: 48px;

        font-weight: 700;

        border: none;

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .stButton > button:hover {
        transform: translateY(-2px);

        box-shadow:
            0 8px 20px rgba(37, 99, 235, 0.18);
    }


    /* ---------- Text Area ---------- */

    textarea {
        border-radius: 16px !important;
    }


    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #0f172a,
                #111827
            );
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }


    /* ---------- Progress ---------- */

    .progress-text {
        color: #64748b;
        font-size: 14px;
        font-weight: 600;
    }


    /* ---------- Footer ---------- */

    .app-footer {
        text-align: center;
        color: #64748b;
        padding: 30px 0 10px;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


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
    "current_result": None
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# LOAD QUESTIONS
# =========================================================

def load_questions():

    try:

        with open(
            "questions.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        st.error("questions.json file was not found.")

        return {}

    except json.JSONDecodeError:

        st.error("There is an error inside questions.json.")

        return {}


questions = load_questions()


# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    show_auth()

    st.stop()


user = st.session_state.user


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:15px 0 25px 0;
        ">
            <div style="font-size:45px;">🎤</div>
            <div style="
                font-size:22px;
                font-weight:800;
            ">
                AI Interview
            </div>
            <div style="
                font-size:13px;
                opacity:0.7;
            ">
                Your Personal AI Coach
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.write(f"👤 *{user['name']}*")
    st.caption(user["email"])

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🎤 New Interview",
            "📊 Interview History",
            "👤 Profile"
        ]
    )

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.interview_started = False
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.session_state.results = []
        st.session_state.final_report = ""
        st.session_state.answer_evaluated = False
        st.session_state.current_result = None

        st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

if page == "🏠 Dashboard":

    st.markdown(
        """
        <div class="hero">

            <div class="hero-title">
                🎤 AI-Powered<br>
                Interview Coach
            </div>

            <div class="hero-subtitle">
                Practice smarter. Speak better.
                Build confidence and become interview-ready
                with your personal AI coach.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    st.markdown(
        f"""
        <div class="card">

            <h2 style="margin-bottom:5px;">
                Welcome, {user['name']}! 👋
            </h2>

            <p style="
                color:#64748b;
                font-size:16px;
            ">
                Your AI-powered interview preparation
                starts here.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    history = get_interview_history(
        user["id"]
    )

    total_interviews = len(history)


    if total_interviews > 0:

        average_score = sum(
            interview[2]
            for interview in history
        ) / total_interviews

    else:

        average_score = 0


    col1, col2, col3 = st.columns(3)


    with col1:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">🎤</div>

                <div class="stat-title">
                    Interviews Completed
                </div>

                <div class="stat-value">
                    {total_interviews}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">⭐</div>

                <div class="stat-title">
                    Average Score
                </div>

                <div class="stat-value">
                    {average_score:.1f}/10
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        st.markdown(
            f"""
            <div class="stat-card">

                <div class="stat-icon">📚</div>

                <div class="stat-title">
                    Question Categories
                </div>

                <div class="stat-value">
                    {len(questions)}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(
        """
        <div class="card">

            <h2>🚀 Ready for your next interview?</h2>

            <p style="color:#64748b;">
                Practice real interview questions,
                get AI feedback and improve your answers.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    if st.button(
        "🚀 Start New Interview",
        use_container_width=True
    ):

        st.session_state.interview_started = False

        st.session_state.question_index = 0

        st.session_state.answers = []

        st.session_state.results = []

        st.session_state.final_report = ""

        st.session_state.answer_evaluated = False

        st.session_state.current_result = None

        st.rerun()


# =========================================================
# NEW INTERVIEW
# =========================================================

elif page == "🎤 New Interview":

    st.title("🎤 AI Interview")


    # -----------------------------------------------------
    # START SCREEN
    # -----------------------------------------------------

    if not st.session_state.interview_started:

        st.markdown(
            """
            <div class="hero">

                <div class="hero-title">
                    🚀 Start Your Interview
                </div>

                <div class="hero-subtitle">
                    Choose your interview category and
                    number of questions.
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


        if not questions:

            st.error(
                "No interview questions are available."
            )

            st.stop()


        category = st.selectbox(
            "🎯 Choose Interview Category",
            list(questions.keys())
        )


        max_questions = min(
            10,
            len(questions[category])
        )


        default_questions = min(
            5,
            max_questions
        )


        number_of_questions = st.slider(
            "📝 Number of Questions",
            min_value=3,
            max_value=max_questions,
            value=default_questions
        )


        st.markdown(
            f"""
            <div class="card">

                <b>🎯 Category:</b> {category}<br><br>

                <b>📝 Questions:</b>
                {number_of_questions}<br><br>

                <b>🤖 AI Feedback:</b>
                Grammar + Score + Better Answer

            </div>
            """,
            unsafe_allow_html=True
        )


        if st.button(
            "🚀 Start Interview",
            use_container_width=True
        ):

            st.session_state.interview_started = True

            st.session_state.question_index = 0

            st.session_state.answers = []

            st.session_state.results = []

            st.session_state.final_report = ""

            st.session_state.category = category

            st.session_state.number_of_questions = (
                number_of_questions
            )

            st.session_state.answer_evaluated = False

            st.session_state.current_result = None

            st.rerun()


    # -----------------------------------------------------
    # INTERVIEW RUNNING
    # -----------------------------------------------------

    else:

        category = st.session_state.category

        number_of_questions = (
            st.session_state.number_of_questions
        )

        question_list = questions[category]

        question_list = question_list[
            :number_of_questions
        ]

        current_index = (
            st.session_state.question_index
        )


        # -------------------------------------------------
        # INTERVIEW COMPLETED
        # -------------------------------------------------

        if current_index >= len(question_list):

            st.success(
                "🎉 Interview Completed Successfully!"
            )


            st.markdown(
                """
                <div class="hero">

                    <div class="hero-title">
                        🏆 Interview Complete
                    </div>

                    <div class="hero-subtitle">
                        Great work! Here is your
                        complete AI performance report.
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )


            if st.session_state.results:

                total_score = sum(
                    result["score"]
                    for result in st.session_state.results
                )


                average_score = (
                    total_score /
                    len(st.session_state.results)
                )


                st.markdown(
                    f"""
                    <div class="score-card">

                        <div style="
                            font-size:18px;
                            font-weight:700;
                        ">
                            ⭐ Overall Score
                        </div>

                        <div class="score-number">
                            {average_score:.1f}/10
                        </div>

                        <div style="
                            color:#64748b;
                        ">
                            Based on
                            {len(st.session_state.results)}
                            questions
                        </div>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.divider()


                st.subheader(
                    "📝 Question Results"
                )


                for index, result in enumerate(
                    st.session_state.results,
                    start=1
                ):

                    with st.expander(
                        f"Question {index}  •  "
                        f"Score: {result['score']}/10"
                    ):

                        st.write("### ⭐ Score")

                        st.write(
                            f"{result['score']}/10"
                        )


                        st.write(
                            "### ✅ Grammar Correction"
                        )

                        st.write(
                            result[
                                "grammar_correction"
                            ]
                        )


                        st.write(
                            "### 💬 AI Feedback"
                        )

                        st.write(
                            result["feedback"]
                        )


                        st.write(
                            "### 💡 Better Answer"
                        )

                        st.info(
                            result[
                                "better_answer"
                            ]
                        )


                st.divider()


                # -------------------------------------------------
                # FINAL REPORT
                # -------------------------------------------------

                if not st.session_state.final_report:

                    with st.spinner(
                        "🤖 AI is preparing your final report..."
                    ):

                        try:

                            report = (
                                generate_final_report(
                                    st.session_state.results
                                )
                            )


                            st.session_state.final_report = (
                                report
                            )


                            save_interview(
                                user_id=user["id"],
                                category=category,
                                score=average_score,
                                total_questions=len(
                                    question_list
                                ),
                                report=report
                            )


                        except Exception as error:

                            st.error(
                                "Could not create final report."
                            )

                            st.code(
                                str(error)
                            )


                if st.session_state.final_report:

                    s
