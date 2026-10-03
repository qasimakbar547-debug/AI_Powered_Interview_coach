import streamlit as st

from database import create_user, login_user


def show_auth():

    st.title("🎤 AI-Powered Interview Coach")

    st.write(
        "Create an account or login to start your interview."
    )

    login_tab, signup_tab = st.tabs(
        ["🔐 Login", "📝 Sign Up"]
    )

    with login_tab:

        st.subheader("Login")

        email = st.text_input(
            "Email",
            key="login_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            use_container_width=True
        ):

            if not email or not password:

                st.error(
                    "Please enter email and password."
                )

            else:

                user = login_user(
                    email,
                    password
                )

                if user:

                    st.session_state.logged_in = True
                    st.session_state.user = user

                    st.success(
                        "Login successful! 🎉"
                    )

                    st.rerun()

                else:

                    st.error(
                        "Invalid email or password."
                    )

    with signup_tab:

        st.subheader("Create Account")

        name = st.text_input(
            "Full Name",
            key="signup_name"
        )

        email = st.text_input(
            "Email",
            key="signup_email"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="signup_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="signup_confirm_password"
        )

        if st.button(
            "📝 Create Account",
            use_container_width=True
        ):

            if not name or not email or not password:

                st.error(
                    "Please fill all fields."
                )

            elif password != confirm_password:

                st.error(
                    "Passwords do not match."
                )

            elif len(password) < 6:

                st.error(
                    "Password must be at least 6 characters."
                )

            else:

                success, user_id = create_user(
                    name,
                    email,
                    password
                )

                if success:

                    st.success(
                        "Account created successfully! "
                        "Please login. 🎉"
                    )

                else:

                    st.error(
                        "This email is already registered."
                    )