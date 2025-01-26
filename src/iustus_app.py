import streamlit as st
import random
import time


# page config
st.set_page_config(page_title="Login", page_icon=None, layout="centered" , initial_sidebar_state="collapsed" , menu_items=None)
#import pages.chat_session_UI as chat_session_UI
if "logged_in" not in st.session_state:
        st.session_state.logged_in=False

if st.session_state.logged_in:
    import pages

# Function to check login credentials
def check_login(username, password):
    # Replace with your own authentication logic
    return username == "admin" and password == "password"

# Initialize session state for login
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# Login page
if not st.session_state.logged_in:
    st.title("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Login")
    guest_button = st.button("Continue as Guest")

    if login_button:
        if check_login(username, password):
            st.session_state.logged_in = True
            st.success("Login successful")
        else:
            st.error("Invalid username or password")
    elif guest_button:
        st.session_state.logged_in = True
        st.success("Continuing as Guest")
        time.sleep(1)
        st.switch_page("pages/session_UI.py")

