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
# SIMPLE PROFESSIONAL CSS
# =========================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #64748b;
        margin-bottom: 30px;
    }

    .welcome-box {
        padding: 25px;
        border-radius: 18px;
        background: #eef4ff;
        border: 1px solid #d7e3ff;
        margin-bottom: 25px;
    }

    .question-box {
        padding: 25px;
        border-radius: 18px;
        background: #f8fafc;
        border: 2px solid #dbeafe;
        margin: 20px 0;
    }

    .score-box {
        padding: 25px;
        border-radius: 18px;
        background: #fff7ed;
        border: 2px solid #fed7aa;
        text-align: center;
        margin: 20px 0;
    }

    .feature-box {
        padding: 20px;
        border-radius: 16px;
        background: white;
        border: 1px solid #e5e7eb;
        margin-bottom: 15px;
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

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "navigation" not in st.session_state:
    st.session_state.navigation = "🏠 Dashboard"

if "interview_started" not in st.session_state:
    st.session_state.interview_started = False

if "question_index" not in st.session_state:
    st.session_state.question_index = 0

if "answers" not in st.session_state:
    st.session_state.answers = []

if "results" not in st.session_state:
    st.session_state.results = []

if "final_report" not in st.session_state:
    st.session_state.final_report = ""

if "category" not in st.session_state:
    st.session_state.category = ""

if "number_of_questions" not in st.session_state:
    st.session_state.number_of_questions = 5

if "answer_evaluated" not in st.session_state:
    st.session_state.answer_evaluated = False

if "current_result" not in st.session_state:
    st.session_state.current_result = None


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

            data = json.load(file)

        return data

    except FileNotFoundError:

        st.error("❌ questions.json file was not found.")
        return {}

    except json.JSONDecodeError:

        st.error("❌ questions.json contains invalid JSON.")
        return {}


questions = load_questions()


# =========================================================
# LOGIN
# =========================================================

if not st.session_state.logged_in:

    show_auth()

    st.stop()


# =========================================================
# USER
# =========================================================

user = st.session_state.user


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎤 AI Interview Coach")

    st.caption("Your Personal AI Interview Assistant")

    st.divider()

    st.write("👤 *" + str(user["name"]) + "*")

    st.caption(str(user["email"]))

    st.divider()

    st.session_state.navigation = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🎤 New Interview",
            "📊 Interview History",
            "👤 Profile"
        ],
        key="navigation_radio",
        index=[
            "🏠 Dashboard",
            "🎤 New Interview",
            "📊 Interview History",
            "👤 Profile"
        ].index(st.session_state.navigation)
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

if st.session_state.navigation == "🏠 Dashboard":

    st.markdown(
        '<div class="main-title">🎤 AI-Powered Interview Coach</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">Practice interviews with AI, improve your answers, and build confidence.</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="welcome-box">

        <h2>Welcome, {user["name"]}! 👋</h2>

        <p>
        Your personal AI interview preparation assistant is ready.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )


    history = get_interview_history(user["id"])

    total_interviews = len(history)


    if total_interviews > 0:

        average_score = sum(
            item[2] for item in history
        ) / total_interviews

    else:

        average_score = 0


    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "🎤 Interviews Completed",
            total_interviews
        )


    with col2:

        st.metric(
            "⭐ Average Score",
            f"{average_score:.1f}/10"
        )


    with col3:

        st.metric(
            "📚 Categories",
            len(questions)
        )


    st.divider()


    st.subheader("🚀 Start Practicing")

    st.write(
        "Choose an interview category and practice "
        "your answers with AI feedback."
    )


    if st.button(
        "🚀 Start New Interview",
        use_container_width=True
    ):

        st.session_state.navigation = "🎤 New Interview"

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

elif st.session_state.navigation == "🎤 New Interview":

    st.title("🎤 AI Interview")


    # =====================================================
    # BEFORE INTERVIEW
    # =====================================================

    if not st.session_state.interview_started:

        st.subheader("⚙️ Interview Settings")

        st.write(
            "Choose your category and number of questions."
        )


        # Check questions
        if not questions:

            st.error(
                "❌ No questions found in questions.json."
            )

            st.info(
                "Please make sure questions.json contains your interview questions."
            )

            st.stop()


        # Category
        category = st.selectbox(
            "🎯 Interview Category",
            list(questions.keys())
        )


        # Get questions
        category_questions = questions[category]


        if not isinstance(category_questions, list):

            st.error(
                "❌ The selected category does not contain a list of questions."
            )

            st.stop()


        if len(category_questions) < 3:

            st.warning(
                "⚠️ This category has fewer than 3 questions."
            )

            max_questions = len(category_questions)

        else:

            max_questions = min(
                10,
                len(category_questions)
            )


        default_questions = min(
            5,
            max_questions
        )


        if max_questions >= 1:

            number_of_questions = st.slider(
                "📝 Number of Questions",
                min_value=1,
                max_value=max_questions,
                value=default_questions
            )

        else:

            st.error(
                "❌ No questions are available in this category."
            )

            st.stop()


        st.divider()


        st.info(
            f"""
            🎯 Category: *{category}*

            📝 Questions: *{number_of_questions}*

            🤖 AI will evaluate your answer and provide:
            Score, grammar correction, feedback and a better answer.
            """
        )


        # =================================================
        # START BUTTON
        # =================================================

        if st.button(
            "🚀 START INTERVIEW",
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


    # =====================================================
    # INTERVIEW STARTED
    # =====================================================

    else:

        category = st.session_state.category

        number_of_questions = (
            st.session_state.number_of_questions
        )


        question_list = questions[category][
            :number_of_questions
        ]


        current_index = (
            st.session_state.question_index
        )


        # =================================================
        # COMPLETED
        # =================================================

        if current_index >= len(question_list):

            st.success(
                "🎉 Interview Completed!"
            )


            st.title("🏆 Final Interview Report")


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
                    <div class="score-box">

                    <h2>⭐ Overall Score</h2>

                    <h1>{average_score:.1f}/10</h1>

                    </div>
                    """,
                    unsafe_allow_html=True
                )


                st.subheader(
                    "📝 Question Results"
                )


                for index, result in enumerate(
                    st.session_state.results,
                    start=1
                ):

                    with st.expander(
                        f"Question {index} — Score {result['score']}/10"
                    ):

                        st.write(
                            "### ⭐ Score"
                        )

                        st.write(
                            f"{result['score']}/10"
                        )


                        st.write(
                            "### ✅ Grammar Correction"
                        )

                        st.write(
                            result["grammar_correction"]
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
                            result["better_answer"]
                        )


                # =========================================
                # FINAL REPORT
                # =========================================

                if not st.session_state.final_report:

                    with st.spinner(
                        "🤖 AI is preparing your final report..."
                    ):

                        try:

                            report = generate_final_report(
                                st.session_state.results
                            )


                            st.session_state.final_report = report


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
                                "❌ Could not create final report."
                            )

                            st.code(
                                str(error)
                            )


                if st.session_state.final_report:

                    st.subheader(
                        "📋 AI Final Report"
                    )

                    st.write(
                        st.session_state.final_report
                    )


            st.divider()


            if st.button(
                "🔄 Start New Interview",
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


        # =================================================
        # CURRENT QUESTION
        # =================================================

        else:

            current_question = question_list[
                current_index
            ]


            # Progress
            progress = (
                current_index /
                len(question_list)
            )


            st.progress(
                progress
            )


            st.caption(
                f"Question {current_index + 1} "
                f"of {len(question_list)}"
            )


            # Question card
            st.markdown(
                f"""
                <div class="question-box">

                <h3>🤖 Interview Question</h3>

                <h2>{current_question}</h2>

                </div>
                """,
                unsafe_allow_html=True
            )


            # Answer
            answer = st.text_area(
                "✍️ Your Answer",
                height=220,
                placeholder=(
                    "Write your interview answer in English..."
                ),
                key=f"answer_{current_index}"
            )


            # =================================================
            # EVALUATE BUTTON
            # =================================================

            if not st.session_state.answer_evaluated:

                if st.button(
                    "🤖 Evaluate My Answer",
                    use_container_width=True
                ):

                    if not answer.strip():

                        st.warning(
                            "⚠️ Please write your answer first."
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


                                st.session_state.answers.append(
                                    answer
                                )


                                st.session_state.results.append(
                                    result
                                )


                                st.session_state.current_result = (
                                    result
                                )


                                st.session_state.answer_evaluated = (
                                    True
                                )


                                st.rerun()


                            except Exception as error:

                                st.error(
                                    "❌ AI evaluation failed."
                                )

                                st.write(
                                    "Please check your AI configuration."
                                )

                                st.code(
                                    str(error)
                                )


            # =================================================
            # SHOW RESULT
            # =================================================

            if st.session_state.answer_evaluated:

                result = (
                    st.session_state.current_result
                )


                if result:

                    st.success(
                        "✅ Answer Evaluated Successfully"
                    )


                    st.markdown(
                        f"""
                        <div class="score-box">

                        <h3>⭐ Your Score</h3>

                        <h1>{result['score']}/10</h1>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                    st.subheader(
                        "✅ Grammar Correction"
                    )

                                       st.subheader("💡 Better Answer")

                    st.info(
                        result["better_answer"]
                    )

                    st.divider()

                    # =========================================
                    # NEXT QUESTION
                    # =========================================

                    if st.button(
                        "➡️ NEXT QUESTION",
                        use_container_width=True
                    ):
                        st.session_state.question_index += 1
                        st.session_state.answer_evaluated = False
                        st.session_state.current_result = None
                        st.rerun()
                        st.session_state.question_index += 1
                        st.session_state.answer_evaluated = False
                        st.session_state.current_result = None

                        st.rerun()
