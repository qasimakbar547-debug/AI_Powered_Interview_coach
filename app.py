import streamlit as st
import json

from database import create_tables, save_interview, get_interview_history
from auth import show_auth
from ai_coach import evaluate_answer, generate_final_report


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎤",
    layout="wide"
)


# =========================================================
# CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        color: #777;
        font-size: 18px;
        margin-bottom: 30px;
    }

    .score-box {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ddd;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 20px;
    }

    .question-box {
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #ddd;
        margin-bottom: 20px;
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
    "navigation": "🏠 Dashboard",
    "interview_started": False,
    "question_index": 0,
    "answers": [],
    "results": [],
    "final_report": None,
    "category": "General",
    "number_of_questions": 5,
    "answer_evaluated": False,
    "current_result": None,
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

    except Exception:

        return {
            "General": [
                "Tell me about yourself.",
                "What are your strengths?",
                "What are your weaknesses?",
                "Why should we hire you?",
                "Where do you see yourself in five years?"
            ],

            "Web Development": [
                "What is HTML?",
                "What is CSS?",
                "What is JavaScript?",
                "What is responsive design?",
                "What is the difference between frontend and backend?"
            ],

            "Python": [
                "What is Python?",
                "What are Python lists?",
                "What is a dictionary in Python?",
                "What is a function?",
                "What is the difference between list and tuple?"
            ],

            "Machine Learning": [
                "What is Machine Learning?",
                "What is supervised learning?",
                "What is classification?",
                "What is regression?",
                "What is overfitting?"
            ]
        }


questions_data = load_questions()


# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    show_auth()

    st.stop()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎤 AI Interview Coach")

    st.divider()

    if st.session_state.user:

        st.write(
            f"👤 {st.session_state.user}"
        )

    st.divider()

    navigation = st.radio(
        "Menu",
        [
            "🏠 Dashboard",
            "🎤 New Interview",
            "📊 Interview History",
            "👤 Profile"
        ],
        index=[
            "🏠 Dashboard",
            "🎤 New Interview",
            "📊 Interview History",
            "👤 Profile"
        ].index(st.session_state.navigation)
    )

    st.session_state.navigation = navigation

    st.divider()

    if st.button(
        "🚪 Logout",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.rerun()


# =========================================================
# DASHBOARD
# =========================================================

if st.session_state.navigation == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">AI-Powered Interview Coach</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Practice interviews and improve your answers with AI.</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3 = st.columns(3)

    history = get_interview_history(
        st.session_state.user
    )

    total_interviews = len(history) if history else 0

    with col1:

        st.metric(
            "🎯 Interviews",
            total_interviews
        )

    with col2:

        st.metric(
            "🤖 AI Feedback",
            "Available"
        )

    with col3:

        st.metric(
            "📚 Practice",
            "Unlimited"
        )

    st.divider()

    st.subheader(
        "👋 Welcome!"
    )

    st.write(
        "Practice common interview questions and get AI-powered feedback on your answers."
    )

    st.write("")

    if st.button(
        "🚀 START NEW INTERVIEW",
        use_container_width=True
    ):

        st.session_state.navigation = "🎤 New Interview"
        st.session_state.interview_started = False
        st.session_state.question_index = 0
        st.session_state.answers = []
        st.session_state.results = []
        st.session_state.final_report = None
        st.session_state.answer_evaluated = False
        st.session_state.current_result = None

        st.rerun()


# =========================================================
# NEW INTERVIEW
# =========================================================

elif st.session_state.navigation == "🎤 New Interview":

    st.markdown(
        '<div class="main-title">🎤 New Interview</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Choose your interview settings and start practicing.</div>',
        unsafe_allow_html=True
    )


    # =====================================================
    # INTERVIEW SETTINGS
    # =====================================================

    if not st.session_state.interview_started:

        st.subheader(
            "⚙️ Interview Settings"
        )

        categories = list(
            questions_data.keys()
        )

        st.session_state.category = st.selectbox(
            "Interview Category",
            categories
        )

        st.session_state.number_of_questions = st.slider(
            "Number of Questions",
            min_value=1,
            max_value=10,
            value=5
        )

        st.write("")

        if st.button(
            "🚀 START INTERVIEW",
            use_container_width=True
        ):

            st.session_state.interview_started = True
            st.session_state.question_index = 0
            st.session_state.answers = []
            st.session_state.results = []
            st.session_state.final_report = None
            st.session_state.answer_evaluated = False
            st.session_state.current_result = None

            st.rerun()


    # =====================================================
    # INTERVIEW QUESTIONS
    # =====================================================

    else:

        category_questions = questions_data.get(
            st.session_state.category,
            []
        )

        selected_questions = category_questions[
            :st.session_state.number_of_questions
        ]


        # =================================================
        # INTERVIEW COMPLETED
        # =================================================

        if (
            st.session_state.question_index
            >= len(selected_questions)
        ):

            st.success(
                "🎉 Interview Completed!"
            )

            st.subheader(
                "📊 Final Interview Report"
            )

            if st.session_state.final_report is None:

                try:

                    st.session_state.final_report = generate_final_report(
                        st.session_state.results
                    )

                except Exception:

                    st.session_state.final_report = (
                        "Your interview has been completed successfully."
                    )


                try:

                    save_interview(
                        st.session_state.user,
                        st.session_state.category,
                        st.session_state.results,
                        st.session_state.final_report
                    )

                except Exception:

                    pass


            st.write(
                st.session_state.final_report
            )

            st.divider()

            if st.button(
                "🔄 START NEW INTERVIEW",
                use_container_width=True
            ):

                st.session_state.interview_started = False
                st.session_state.question_index = 0
                st.session_state.answers = []
                st.session_state.results = []
                st.session_state.final_report = None
                st.session_state.answer_evaluated = False
                st.session_state.current_result = None

                st.rerun()


        # =================================================
        # CURRENT QUESTION
        # =================================================

        else:

            current_question = selected_questions[
                st.session_state.question_index
            ]

            question_number = (
                st.session_state.question_index + 1
            )

            total_questions = len(
                selected_questions
            )

            st.progress(
                question_number / total_questions
            )

            st.write(
                f"Question {question_number} of {total_questions}"
            )

            st.markdown(
                '<div class="question-box">',
                unsafe_allow_html=True
            )

            st.subheader(
                current_question
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


            # =================================================
            # ANSWER BOX
            # =================================================

            answer = st.text_area(
                "✍️ Your Answer",
                height=180,
                placeholder="Type your interview answer here..."
            )


            # =================================================
            # EVALUATE ANSWER
            # =================================================

            if not st.session_state.answer_evaluated:

                if st.button(
                    "🤖 EVALUATE MY ANSWER",
                    use_container_width=True
                ):

                    if not answer.strip():

                        st.warning(
                            "Please write an answer first."
                        )

                    else:

                        with st.spinner(
                            "🤖 AI is evaluating your answer..."
                        ):

                            try:

                                result = evaluate_answer(
                                    current_question,
                                    answer
                                )

                                st.session_state.current_result = result

                                st.session_state.answers.append(
                                    answer
                                )

                                st.session_state.results.append(
                                    result
                                )

                                st.session_state.answer_evaluated = True

                                st.rerun()

                            except Exception as e:

                                st.error(
                                    f"Error evaluating answer: {e}"
                                )


            # =================================================
            # SHOW RESULT
            # =================================================

            if st.session_state.answer_evaluated:

                result = st.session_state.current_result

                if result:

                    st.success(
                        "✅ Answer Evaluated Successfully"
                    )

                    st.subheader(
                        "⭐ Your Score"
                    )

                    st.markdown(
                        f"# {result['score']}/10"
                    )

                    st.subheader(
                        "📝 Grammar Correction"
                    )

                    st.info(
                        result["grammar_correction"]
                    )

                    st.subheader(
                        "💬 AI Feedback"
                    )

                    st.write(
                        result["feedback"]
                    )

                    st.subheader(
                        "💡 Better Answer"
                    )

                    st.info(
                        result["better_answer"]
                    )

                    st.divider()


                    # =================================================
                    # NEXT QUESTION
                    # =================================================

                    if st.button(
                        "➡️ NEXT QUESTION",
                        use_container_width=True
                    ):

                        st.session_state.question_index += 1

                        st.session_state.answer_evaluated = False

                        st.session_state.current_result = None

                        st.rerun()


# =========================================================
# INTERVIEW HISTORY
# =========================================================

elif st.session_state.navigation == "📊 Interview History":

    st.markdown(
        '<div class="main-title">📊 Interview History</div>',
        unsafe_allow_html=True
    )

    history = get_interview_history(
        st.session_state.user
    )

    if not history:

        st.info(
            "No interview history found yet."
        )

    else:

        for i, interview in enumerate(
            history,
            start=1
        ):

            with st.expander(
                f"Interview #{i}"
            ):

                st.write(
                    interview
                )


# =========================================================
# PROFILE
# =========================================================

elif st.session_state.navigation == "👤 Profile":

    st.markdown(
        '<div class="main-title">👤 Profile</div>',
        unsafe_allow_html=True
    )

    st.write(
        f"**User:** {st.session_state.user}"
    )

    history = get_interview_history(
        st.session_state.user
    )

    st.write(
        f"**Total Interviews:** {len(history) if history else 0}"
    )

    st.divider()

    st.info(
        "Keep practicing to improve your interview performance. 🚀"
    )
