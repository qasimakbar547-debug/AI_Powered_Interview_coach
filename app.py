import streamlit as st

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
# PREMIUM UI
# =========================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(99, 102, 241, 0.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 90% 20%,
            rgba(59, 130, 246, 0.10),
            transparent 25%
        ),
        #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

section[data-testid="stSidebar"] {
    background:
        linear-gradient(
            180deg,
            #0f172a 0%,
            #111827 55%,
            #172554 100%
        );

    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

section[data-testid="stSidebar"] * {
    color: #f8fafc;
}

section[data-testid="stSidebar"] .stRadio label {
    color: #cbd5e1 !important;
    font-weight: 600;
}

section[data-testid="stSidebar"] .stRadio label:hover {
    color: white !important;
}

h1 {
    font-weight: 800 !important;
    letter-spacing: -1px;
    color: #0f172a;
}

h2 {
    font-weight: 750 !important;
    color: #111827;
}

h3 {
    font-weight: 700 !important;
    color: #1e293b;
}

.stButton > button {
    border-radius: 12px;
    border: 1px solid #dbeafe;
    min-height: 46px;

    background:
        linear-gradient(
            135deg,
            #2563eb,
            #4f46e5
        );

    color: white;
    font-weight: 700;

    box-shadow:
        0 6px 18px rgba(37,99,235,0.20);

    transition:
        transform 0.15s ease,
        box-shadow 0.15s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);

    box-shadow:
        0 10px 25px rgba(37,99,235,0.30);

    color: white;
}

textarea {
    border-radius: 14px !important;
    border: 1px solid #dbe3ef !important;
    background: white !important;
}

textarea:focus {
    border: 1px solid #6366f1 !important;
    box-shadow:
        0 0 0 2px rgba(99,102,241,0.10) !important;
}

div[data-baseweb="select"] {
    border-radius: 12px;
}

div[data-baseweb="input"] {
    border-radius: 12px;
}

div[data-testid="stMetric"] {
    background: rgba(255,255,255,0.95);

    border: 1px solid #e2e8f0;

    border-radius: 18px;

    padding: 20px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.06);
}

div[data-testid="stMetricLabel"] {
    color: #64748b !important;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #0f172a !important;
    font-weight: 800;
}

div[data-testid="stAlert"] {
    border-radius: 14px;
}

details {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    margin-bottom: 12px;
}

details summary {
    font-weight: 700;
}

.hero {
    position: relative;
    overflow: hidden;

    padding: 42px;

    border-radius: 26px;

    margin-bottom: 28px;

    color: white;

    background:
        linear-gradient(
            135deg,
            #0f172a 0%,
            #1e3a8a 48%,
            #4f46e5 100%
        );

    box-shadow:
        0 18px 45px rgba(37,99,235,0.20);
}

.hero:after {
    content: "";

    position: absolute;

    width: 280px;
    height: 280px;

    border-radius: 50%;

    right: -80px;
    top: -100px;

    background:
        rgba(255,255,255,0.08);
}

.hero-title {
    font-size: 42px;
    font-weight: 850;
    margin-bottom: 10px;
}

.hero-text {
    font-size: 17px;
    color: #dbeafe;
    max-width: 720px;
}

.badge {
    display: inline-block;

    padding: 7px 13px;

    border-radius: 30px;

    background: rgba(255,255,255,0.12);

    border: 1px solid rgba(255,255,255,0.18);

    color: #e0f2fe;

    font-size: 13px;

    font-weight: 700;

    margin-bottom: 16px;
}

.card {
    background: rgba(255,255,255,0.96);

    border: 1px solid #e2e8f0;

    border-radius: 20px;

    padding: 26px;

    margin-bottom: 20px;

    box-shadow:
        0 8px 25px rgba(15,23,42,0.05);
}

.question-card {
    background:
        linear-gradient(
            135deg,
            #ffffff,
            #f8fbff
        );

    border: 1px solid #dbeafe;

    border-left: 5px solid #4f46e5;

    border-radius: 20px;

    padding: 30px;

    margin: 18px 0 22px 0;

    box-shadow:
        0 10px 30px rgba(30,64,175,0.07);
}

.question-label {
    color: #4f46e5;

    font-size: 13px;

    font-weight: 800;

    letter-spacing: 1px;

    text-transform: uppercase;

    margin-bottom: 10px;
}

.question-text {
    color: #0f172a;

    font-size: 25px;

    line-height: 1.45;

    font-weight: 750;
}

.score-card {
    background:
        linear-gradient(
            135deg,
            #eef2ff,
            #dbeafe
        );

    border: 1px solid #c7d2fe;

    border-radius: 22px;

    padding: 30px;

    text-align: center;

    margin: 20px 0;

    box-shadow:
        0 10px 30px rgba(79,70,229,0.12);
}

.score-small {
    color: #475569;

    font-size: 13px;

    font-weight: 800;

    letter-spacing: 1px;

    text-transform: uppercase;
}

.score-number {
    color: #4338ca;

    font-size: 58px;

    font-weight: 900;

    margin-top: 5px;
}

.feedback-card {
    background: white;

    border: 1px solid #e2e8f0;

    border-radius: 18px;

    padding: 24px;

    margin: 14px 0;

    box-shadow:
        0 6px 20px rgba(15,23,42,0.04);
}

.feedback-title {
    color: #1e293b;

    font-size: 18px;

    font-weight: 750;

    margin-bottom: 8px;
}

.profile-card {
    background:
        linear-gradient(
            135deg,
            #ffffff,
            #f8fafc
        );

    border: 1px solid #e2e8f0;

    border-radius: 22px;

    padding: 30px;

    box-shadow:
        0 10px 30px rgba(15,23,42,0.06);
}

.footer {
    text-align: center;

    color: #94a3b8;

    padding: 35px 0 10px 0;

    font-size: 13px;
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
    "current_result": None
}

for key, value in defaults.items():

    if key not in st.session_state:
        st.session_state[key] = value


# =========================================================
# ENGLISH INTERVIEW QUESTION BANK
# =========================================================
#
# IMPORTANT:
# These are NOT coding questions.
# These are English-speaking interview questions.
#
# The user reads the question in English
# and answers in English.
#
# =========================================================

questions = {

    "Python": [
        "What is Python?",
        "Why is Python popular?",
        "What are the main features of Python?",
        "What is a variable in Python?",
        "What is a function in Python?",
        "What is a Python library?",
        "What is the difference between a list and a tuple in Python?",
        "What is a dictionary in Python?",
        "What is object-oriented programming?",
        "Why is Python commonly used in machine learning?"
    ],

    "Web Development": [
        "What is HTML?",
        "What is CSS?",
        "What is JavaScript?",
        "What is a website?",
        "What is a web browser?",
        "What is frontend development?",
        "What is backend development?",
        "What is responsive web design?",
        "What is an API?",
        "What is the difference between frontend and backend development?"
    ],

    "Machine Learning": [
        "What is machine learning?",
        "Why is machine learning important?",
        "What is supervised learning?",
        "What is unsupervised learning?",
        "What is a dataset?",
        "What is training data?",
        "What is testing data?",
        "What is a machine learning model?",
        "What is overfitting?",
        "What is the difference between classification and regression?"
    ],

    "Computer Science": [
        "What is computer science?",
        "What is an algorithm?",
        "What is a programming language?",
        "What is an operating system?",
        "What is a database?",
        "What is a computer network?",
        "What is software development?",
        "What is cybersecurity?",
        "What is Git?",
        "What is GitHub?"
    ],

    "Computer Basics": [
        "What is a computer?",
        "What is a CPU?",
        "What is RAM?",
        "What is a hard drive?",
        "What is an operating system?",
        "What is a webcam?",
        "What is a keyboard?",
        "What is a computer network?",
        "What is the internet?",
        "What is cloud computing?"
    ]
}


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
            padding: 10px 0 20px 0;
            text-align:center;
        ">

            <div style="
                font-size:42px;
                margin-bottom:5px;
            ">
                🎤
            </div>

            <div style="
                font-size:21px;
                font-weight:800;
            ">
                AI Interview Coach
            </div>

            <div style="
                font-size:12px;
                color:#94a3b8;
                margin-top:5px;
            ">
                AI-powered interview practice
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown(
        f"""
        <div style="
            background:rgba(255,255,255,0.06);
            border:1px solid rgba(255,255,255,0.08);
            border-radius:14px;
            padding:15px;
            margin-bottom:15px;
        ">

            <div style="
                font-size:14px;
                font-weight:700;
            ">
                👋 {user['name']}
            </div>

            <div style="
                font-size:11px;
                color:#94a3b8;
                margin-top:5px;
            ">
                {user['email']}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.caption("MAIN MENU")

    page = st.radio(
        "Navigation",
        [
            "🏠 Dashboard",
            "🎤 New Interview",
            "📊 Interview History",
            "👤 Profile"
        ],
        label_visibility="collapsed"
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

            <div class="badge">
                🤖 AI POWERED
            </div>

            <div class="hero-title">
                AI-Powered Interview Coach
            </div>

            <div class="hero-text">
                Practice English interview questions,
                improve your answers and receive
                intelligent AI feedback.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    history = get_interview_history(
        user["id"]
    )

    total_interviews = len(history)

    if total_interviews:

        average_score = sum(
            item[2]
            for item in history
        ) / total_interviews

    else:

        average_score = 0

    st.subheader(
        f"Welcome back, {user['name']} 👋"
    )

    st.write(
        "Practice answering technical interview questions in English."
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "🎤 Interviews",
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

    st.write("")

    st.markdown(
        """
        <div class="card">

            <h3>🚀 Ready to practice?</h3>

            <p>
                Go to <b>New Interview</b>,
                select a category and answer
                English interview questions.
            </p>

            <p>
                💬 The interviewer will ask you
                questions in English and you should
                answer in English.
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.info(
        "💡 Use the sidebar → 🎤 New Interview to start your practice session."
    )


# =========================================================
# NEW INTERVIEW
# =========================================================

elif page == "🎤 New Interview":

    st.markdown(
        """
        <div class="hero">

            <div class="badge">
                🎤 ENGLISH INTERVIEW MODE
            </div>

            <div class="hero-title">
                New Interview
            </div>

            <div class="hero-text">
                Answer professional interview questions
                in English and receive AI-powered feedback.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    # =====================================================
    # SETUP
    # =====================================================

    if not st.session_state.interview_started:

        st.markdown(
            """
            <div class="card">

                <h3>⚙️ Interview Setup</h3>

                <p>
                    Select your interview category and
                    number of English questions.
                </p>

            </div>
            """,
            unsafe_allow_html=True
        )

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
            "❓ Number of Questions",
            min_value=1,
            max_value=max_questions,
            value=default_questions
        )

        col1, col2 = st.columns(2)

        with col1:

            st.info(
                f"🎯 **Category**\n\n{category}"
            )

        with col2:

            st.info(
                f"❓ **Questions**\n\n{number_of_questions}"
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

            st.session_state.final_report = ""

            st.session_state.category = category

            st.session_state.number_of_questions = (
                number_of_questions
            )

            st.session_state.answer_evaluated = False

            st.session_state.current_result = None

            st.rerun()

    # =====================================================
    # RUNNING INTERVIEW
    # =====================================================

    else:

        category = (
            st.session_state.category
        )

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

            st.markdown(
                """
                <div class="hero">

                    <div class="badge">
                        🎉 COMPLETED
                    </div>

                    <div class="hero-title">
                        Interview Complete
                    </div>

                    <div class="hero-text">
                        Great work! Here is your complete
                        English interview performance.
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

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "⭐ Overall Score",
                        f"{average_score:.1f}/10"
                    )

                with col2:

                    st.metric(
                        "📝 Questions",
                        len(question_list)
                    )

                with col3:

                    st.metric(
                        "🎯 Completion",
                        "100%"
                    )

                st.divider()

                st.subheader(
                    "📊 Your Results"
                )

                for index, result in enumerate(
                    st.session_state.results,
                    start=1
                ):

                    with st.expander(
                        f"Question {index}  •  ⭐ {result['score']}/10"
                    ):

                        st.write(
                            f"### ⭐ Score: {result['score']}/10"
                        )

                        st.write(
                            "### ✅ Grammar Correction"
                        )

                        st.info(
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

                st.divider()

                # =========================================
                # FINAL REPORT
                # =========================================

                if not st.session_state.final_report:

                    with st.spinner(
                        "🤖 Preparing your final AI report..."
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

                    st.subheader(
                        "🤖 AI Final Report"
                    )

                    st.info(
                        st.session_state.final_report
                    )

            st.write("")

            if st.button(
                "🔄 START NEW INTERVIEW",
                use_container_width=True
            ):

                st.session_state.interview_started = False
                st.session_state.question_index = 0
                st.session_state.answers = []
                st.session_state.results = []
                st.session_state.final_report = ""
                st.session_state.category = ""
                st.session_state.answer_evaluated = False
                st.session_state.current_result = None

                st.rerun()

        # =================================================
        # CURRENT QUESTION
        # =================================================

        else:

            current_question = (
                question_list[current_index]
            )

            # Correct progress:
            progress = (
                (current_index + 1) /
                len(question_list)
            )

            st.progress(
                progress
            )

            st.caption(
                f"QUESTION {current_index + 1} OF {len(question_list)}"
            )

            # =================================================
            # ENGLISH QUESTION CARD
            # =================================================

            st.markdown(
                f"""
                <div class="question-card">

                    <div class="question-label">
                        🎤 Interview Question
                    </div>

                    <div class="question-text">
                        {current_question}
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.subheader(
                "✍️ Your Answer"
            )

            answer = st.text_area(
                "Type your answer below",
                height=190,
                placeholder=(
                    "Answer this question in English..."
                ),
                key=f"answer_{current_index}",
                label_visibility="collapsed"
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
                            "⚠️ Please write your answer first."
                        )

                    else:

                        with st.spinner(
                            "🤖 AI is analyzing your English answer..."
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
                                    "Please check your API key and internet connection."
                                )

                                st.code(
                                    str(error)
                                )

            # =================================================
            # RESULT
            # =================================================

            if st.session_state.answer_evaluated:

                result = (
                    st.session_state.current_result
                )

                if result:

                    st.success(
                        "✅ Answer evaluated successfully!"
                    )

                    # =========================================
                    # SCORE
                    # =========================================

                    st.markdown(
                        f"""
                        <div class="score-card">

                            <div class="score-small">
                                AI SCORE
                            </div>

                            <div class="score-number">
                                {result['score']}/10
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # =========================================
                    # GRAMMAR
                    # =========================================

                    st.markdown(
                        """
                        <div class="feedback-card">

                            <div class="feedback-title">
                                ✅ Grammar Correction
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.info(
                        result["grammar_correction"]
                    )

                    # =========================================
                    # FEEDBACK
                    # =========================================

                    st.markdown(
                        """
                        <div class="feedback-card">

                            <div class="feedback-title">
                                💬 AI Feedback
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.write(
                        result["feedback"]
                    )

                    # =========================================
                    # BETTER ANSWER
                    # =========================================

                    st.markdown(
                        """
                        <div class="feedback-card">

                            <div class="feedback-title">
                                💡 Better Answer
                            </div>

                        </div>
                        """,
                        unsafe_allow_html=True
                    )

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


# =========================================================
# INTERVIEW HISTORY
# =========================================================

elif page == "📊 Interview History":

    st.markdown(
        """
        <div class="hero">

            <div class="badge">
                📊 PERFORMANCE
            </div>

            <div class="hero-title">
                Interview History
            </div>

            <div class="hero-text">
                Review your previous interview
                performance and AI reports.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    history = get_interview_history(
        user["id"]
    )

    if not history:

        st.info(
            "📭 You have not completed any interviews yet."
        )

    else:

        for interview in history:

            category = interview[1]
            score = interview[2]
            total_questions = interview[3]
            date = interview[4]
            report = interview[5]

            with st.expander(
                f"🎤 {category}   •   ⭐ {score:.1f}/10   •   {date}"
            ):

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "⭐ Score",
                        f"{score:.1f}/10"
                    )

                with col2:

                    st.metric(
                        "📝 Questions",
                        total_questions
                    )

                with col3:

                    st.write(
                        "**📅 Date**"
                    )

                    st.write(
                        str(date)
                    )

                st.divider()

                st.subheader(
                    "📋 Final AI Report"
                )

                st.info(
                    report
                )


# =========================================================
# PROFILE
# =========================================================

elif page == "👤 Profile":

    st.markdown(
        """
        <div class="hero">

            <div class="badge">
                👤 ACCOUNT
            </div>

            <div class="hero-title">
                My Profile
            </div>

            <div class="hero-text">
                Your account information and
                interview statistics.
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="profile-card">

            <h3>👤 Personal Information</h3>

            <p>
                <b>Name:</b> {user['name']}
            </p>

            <p>
                <b>Email:</b> {user['email']}
            </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.write("")

    history = get_interview_history(
        user["id"]
    )

    st.subheader(
        "📊 Your Statistics"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "🎤 Total Interviews",
            len(history)
        )

    with col2:

        if history:

            average = sum(
                item[2]
                for item in history
            ) / len(history)

            st.metric(
                "⭐ Average Score",
                f"{average:.1f}/10"
            )

        else:

            st.metric(
                "⭐ Average Score",
                "No interviews yet"
            )

    st.write("")

    st.success(
        "🔐 Your interview data is stored separately for your account."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">

        🎤 AI Interview Coach
        &nbsp; • &nbsp;
        English Practice
        &nbsp; • &nbsp;
        Improve
        &nbsp; • &nbsp;
        Succeed

    </div>
    """,
    unsafe_allow_html=True
)
