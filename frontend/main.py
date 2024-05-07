import streamlit as st
import os

import logic

if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False


def check_credentials(username, password):
    correct_username = os.getenv("TMP_USERNAME")
    correct_password = os.getenv("TMP_PASSWORD")
    return username == correct_username and password == correct_password


if not st.session_state["authenticated"]:
    with st.form("login_form"):
        st.write("TARS (Early Access) - Please Login To Continue")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

        if login_button:
            if check_credentials(username, password):
                st.session_state["authenticated"] = True
                st.experimental_rerun()
            else:
                st.error("Incorrect username or password. Please try again.")

if st.session_state["authenticated"]:
    logic.main_app()
