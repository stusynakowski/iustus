
import streamlit as st
import random
import time
from llm_methods.gpt2_api_local import get_local_gpt2_response


st.set_page_config(page_title="Profile", page_icon=None, layout="wide" , initial_sidebar_state="expanded" , menu_items=None)




# Display sidebar
with st.sidebar:
    st.title("Simple chat for Some USer")
    st.write("Sample User Profile")
    st.write("Name: John Doe")
    st.write("Email:")
    with st.expander("Manage Consultations"):

        new_session_name = st.text_input("New Session Name")
        if st.button("Create New Cosultation"):
            if new_session_name and new_session_name not in st.session_state.sessions:
                st.session_state.sessions[new_session_name] = []
                st.session_state.current_session = new_session_name
                st.rerun()


    with st.expander("Settings"):
        st.write("Change Name")
        st.write("Change Password")
        st.write("Change Email")
        st.write("Change Profile Picture")

if "sessions" not in st.session_state:
    st.session_state.sessions = {"default": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "default"

# Create new session

# Session tabs
session_names = list(st.session_state.sessions.keys())
tabs = st.tabs(session_names)

for tab_i, session_name in enumerate(session_names):
    context_column,chat_column=st.columns(2)
    with tabs[tab_i]:

        with context_column:
            st.write("all information needed to help you answer the question")
            with st.expander("Context What information do you need?"):
                st.write("Context 1")
                st.write("Context 2")
                st.write("Context 3")
            
        with chat_column:
            st.write("Chat")
            # Display chat messages
            for session in st.session_state.sessions[session_name]:
                with st.expander(f"{session['role']}"):
                    st.write(session["content"])
            # Chat input
            if prompt := st.text_input("What is up?"):
                # Display user message in chat message container
                with st.expander("user"):
                    st.write(prompt)
                # Add user message to chat history
                st.session_state.sessions[session_name].append({"role": "user", "content": prompt})

                # Get response from local GPT-2 model
                response = get_local_gpt2_response(prompt)

                # Display assistant response in chat message container
                with st.expander("assistant"):
                    st.write(response)
                # Add assistant response to chat history
                st.session_state.sessions[session_name].append({"role": "assistant", "content": response})
