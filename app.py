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


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="AI-Powered Interview Coach",
    page_icon="🎤",
    layout="wide"
)


# ==========================================
# CREATE DATABASE TABLES
# ==========================================

create_tables()


# ==========================================
# SESSION STATE
# ==========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

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

# NEW: keeps evaluation result visible
if "answer_evaluated" not in st.session_state:
    st.session_state.answer_evaluated = False

if "current_result" not in st.session_state:
    st.session_state.current_result = None


# ==========================================
# LOAD QUESTIONS
# ==========================================

def load_questions():

    try:

        with open(
            "questions.json",
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except FileNotFoundError:

        st.error(
            "questions.json file was not found."
        )

        return {}

    except json.JSONDecodeError:

        st.error(
            "There is an error inside questions.json."
        )

        return {}


questions = load_questions()


# ==========================================
# LOGIN / SIGNUP
# ==========================================

if not st.session_state.logged_in:

    show_auth()

    st.stop()


# ==========================================
# CURRENT USER
# ==========================================

user = st.session_state.user


# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:

    st.title("🎤 Interview Coach")

    st.write(
        f"👤 {user['name']}"
    )

    st.write(
        f"📧 {user['email']}"
    )

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


# ==========================================
# DASHBOARD
# ==========================================

if page == "🏠 Dashboard":

    st.title(
        "🎤 AI-Powered Interview Coach"
    )

    st.subheader(
        f"Welcome, {user['name']}! 👋"
    )

    st.write(
        "Practice your interview with AI, "
        "improve your English, and track your progress."
    )

    st.divider()

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

    st.info(
        "Select '🎤 New Interview' from the sidebar "
        "to start your AI interview."
    )


# ==========================================
# NEW INTERVIEW
# ==========================================

elif page == "🎤 New Interview":

    st.title(
        "🎤 AI Interview"
    )


    # ======================================
    # INTERVIEW NOT STARTED
    # ======================================

    if not st.session_state.interview_started:

        st.subheader(
            "⚙️ Interview Settings"
        )

        if not questions:

            st.error(
                "No interview questions are available."
            )

            st.stop()


        category = st.selectbox(
            "Choose Interview Category",
            list(questions.keys())
        )


        number_of_questions = st.slider(
            "Number of Questions",
            min_value=3,
            max_value=min(
                10,
                len(questions[category])
            ),
            value=min(
                5,
                len(questions[category])
            )
        )


        st.write(
            f"Category: {category}"
        )

        st.write(
            f"Questions: {number_of_questions}"
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


    # ======================================
    # INTERVIEW RUNNING
    # ======================================

    else:

        category = (
            st.session_state.category
        )

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


        # ==================================
        # INTERVIEW COMPLETED
        # ==================================

        if current_index >= len(question_list):

            st.success(
                "🎉 Interview Completed Successfully!"
            )

            st.subheader(
                "📊 Final Interview Report"
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


                st.metric(
                    "⭐ Overall Score",
                    f"{average_score:.1f}/10"
                )


                st.divider()


                # ==========================
                # QUESTION RESULTS
                # ==========================

                st.subheader(
                    "📝 Question-by-Question Results"
                )


                for index, result in enumerate(
                    st.session_state.results,
                    start=1
                ):

                    with st.expander(
                        f"Question {index} — "
                        f"Score: {result['score']}/10"
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


                # ==========================
                # GENERATE FINAL REPORT
                # ==========================

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


                # ==========================
                # FINAL AI REPORT
                # ==========================

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


        # ==================================
        # CURRENT QUESTION
        # ==================================

        else:

            current_question = (
                question_list[current_index]
            )


            progress = (
                current_index /
                len(question_list)
            )


            st.progress(
                progress
            )


            st.subheader(
                f"Question {current_index + 1} "
                f"of {len(question_list)}"
            )


            st.info(
                current_question
            )


            # ==================================
            # ANSWER INPUT
            # ==================================

            answer = st.text_area(
                "📝 Your Answer",
                height=200,
                placeholder=(
                    "Write your answer in English..."
                ),
                key=f"answer_{current_index}"
            )


            # ==================================
            # EVALUATE ANSWER
            # ==================================

            if not st.session_state.answer_evaluated:

                if st.button(
                    "🤖 Evaluate My Answer",
                    use_container_width=True
                ):

                    if not answer.strip():

                        st.warning(
                            "Please write your answer first."
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


                                # Save answer
                                st.session_state.answers.append(
                                    answer
                                )


                                # Save result
                                st.session_state.results.append(
                                    result
                                )


                                # Save current result
                                st.session_state.current_result = (
                                    result
                                )


                                # Mark as evaluated
                                st.session_state.answer_evaluated = True


                                st.rerun()


                            except Exception as error:

                                st.error(
                                    "❌ AI evaluation failed."
                                )

                                st.write(
                                    "Please check your API key "
                                    "and internet connection."
                                )

                                st.code(
                                    str(error)
                                )


            # ==================================
            # SHOW EVALUATION RESULT
            # ==================================

            if st.session_state.answer_evaluated:

                result = (
                    st.session_state.current_result
                )


                if result:

                    st.success(
                        "✅ Your answer has been evaluated!"
                    )


                    st.subheader(
                        f"⭐ Score: "
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


                    # ==================================
                    # NEXT QUESTION
                    # ==================================

                    if st.button(
                        "➡️ Next Question",
                        use_container_width=True
                    ):

                        st.session_state.question_index += 1

                        st.session_state.answer_evaluated = False

                        st.session_state.current_result = None

                        st.rerun()


# ==========================================
# INTERVIEW HISTORY
# ==========================================

elif page == "📊 Interview History":

    st.title(
        "📊 Interview History"
    )

    history = get_interview_history(
        user["id"]
    )


    if not history:

        st.info(
            "You have not completed any interviews yet."
        )


    else:

        for interview in history:

            interview_id = interview[0]

            category = interview[1]

            score = interview[2]

            total_questions = interview[3]

            date = interview[4]

            report = interview[5]


            with st.expander(
                f"🎤 {category} | "
                f"⭐ {score:.1f}/10 | "
                f"{date}"
            ):

                st.write(
                    f"Interview ID: "
                    f"{interview_id}"
                )

                st.write(
                    f"Category: {category}"
                )

                st.write(
                    f"Score: {score:.1f}/10"
                )

                st.write(
                    f"Total Questions: "
                    f"{total_questions}"
                )

                st.write(
                    f"Date: {date}"
                )

                st.divider()

                st.subheader(
                    "📋 Final Report"
                )

                st.write(
                    report
                )


# ==========================================
# PROFILE
# ==========================================

elif page == "👤 Profile":

    st.title(
        "👤 My Profile"
    )

    st.write(
        "### Personal Information"
    )

    st.write(
        f"Name: {user['name']}"
    )

    st.write(
        f"Email: {user['email']}"
    )

    st.divider()

    history = get_interview_history(
        user["id"]
    )

    st.write(
        "### 📊 Your Statistics"
    )

    st.write(
        f"Total interviews: {len(history)}"
    )

    if history:

        average = sum(
            item[2]
            for item in history
        ) / len(history)

        st.write(
            f"Average score: {average:.1f}/10"
        )

    else:

        st.write(
            "Average score: No interviews yet"
        )

    st.success(
        "Your interview data is stored separately "
        "for your account."
    
