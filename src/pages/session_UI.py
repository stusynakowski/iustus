
import streamlit as st
import random
import time
from llm_methods.gpt2_api_local import get_local_gpt2_response
import llm_methods.open_ai_api as llm_methods
from PyPDF2 import PdfReader
import copy


def read_pdf_to_string(pdf_path):
    """
    Reads a text-based PDF file and returns its content as a string.
    
    Parameters:
        pdf_path (str): Path to the PDF file.
        
    Returns:
        str: The concatenated text extracted from the PDF.
    """
    text = ""
    
    # Open the PDF file in binary mode.
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        
        # Loop through each page and extract text.
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    
    return text.strip()


st.set_page_config(page_title="Profile", page_icon=None, layout="wide" , initial_sidebar_state="expanded" , menu_items=None)







# Display sidebar
with st.sidebar:
    st.title("Simple chat for Some User")
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
        chat_model=st.selectbox("Chat Model", ["opanai_api", "local"],index=0)


    
if "already_ran_analysis" not in st.session_state.keys():
    st.session_state.already_ran_analysis = False       

if "sessions" not in st.session_state:
    st.session_state.sessions = {"default": []}
if "current_session" not in st.session_state:
    st.session_state.current_session = "default"

if "prompt" not in st.session_state:
    st.session_state.prompt = None

if "document_context" not in st.session_state:
    st.session_state.document_context = ""




# Create new session

# Session tabs
session_names = list(st.session_state.sessions.keys())
tabs = st.tabs(session_names)


st.session_state.default_tasks_and_questions=["What are 5 actionable steps I should take now?","what are some of the watchouts i should be aware of?S"]


for tab_i, session_name in enumerate(session_names):
    context_column,chat_column=st.columns(2,border=True)
    with tabs[tab_i]:

        with context_column:
            st.header("Context")
            with st.expander("Describe Your Situation"):
                st.session_state.situation=st.text_area("just tell me about yourself and the current problems you are facing",value="Hello! I just got a new job and I want to review all of my current health care benefits and understand what I need to do to maximize my benefits.") 
            with st.expander("Upload Any Relevant Documentation?"):
                uploaded_files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)


            with st.expander("Additional Info? "):
                st.session_state.misc_relevant_info=st.text_area("additional info that may be helpful in answering your questions",value="I am 30 years old and I have a family history of heart disease")

            #with st.expander("Misc? (information that may be helpful in answering your questions)"):
            #    st.session_state.misc_relevant_info=st.text_area("additional infor that may be helpful in answering your questions")  ]       
            with st.expander("Default Questions and Tasks"):
                default_tasks=["Actionable Tasks","Common Questions","Common Watchouts"]
                st.session_state.default_tasks_and_questions=st.multiselect("Default Analysis",default_tasks,default=default_tasks)


            if st.button("Curate all Information Provided and Analyze"):

            
                if uploaded_files:
                    for uploaded_file in uploaded_files:
                        #pdf_text=read_pdf_to_string(uploaded_file)
                        reader = PdfReader(uploaded_file)

                        # Loop through each page and extract text.
                        for page in reader.pages:
                            page_text = page.extract_text()
                            if page_text:
                                st.session_state.document_context += page_text + "\n"
                        #@pdf_text = read_pdf(uploaded_file)
                        #st.session_state.relevant_info = pdf_text
                        #st.write(f"Content of {uploaded_file.name}:")
                        #st.write(st.session_state.document_context)
                else:
                    st.session_state.document_context=""

                st.write("processing all information")



                st.session_state.system_messages=llm_methods.generate_context(st.session_state.situation
                    ,st.session_state.document_context
                    ,st.session_state.misc_relevant_info)
                st.session_state.system_messages.append({
                    "role": "user",
                    "content": "### QUESTIONS OR TASKS ###\n" + " ".join(st.session_state.default_tasks_and_questions)
                })
                st.session_state.current_response=llm_methods.get_openai_response(st.session_state.system_messages)
                st.session_state.already_ran_analysis=True
            
            if st.session_state.already_ran_analysis:
                st.write("Base Analysis")
                st.write(st.session_state.current_response.content)
        

        #if  st.session_state.already_ran_analysis:
            



        with chat_column:
            if st.session_state.sessions[session_name]==[]:
                st.session_state.system_messages=llm_methods.generate_context(st.session_state.situation
                    ,st.session_state.document_context
                    ,st.session_state.misc_relevant_info)

            st.header("Ask Additional Questions")
            # Display chat messages
            for session in st.session_state.sessions[session_name]:
                with st.expander(f"{session['role']}"):
                    st.write(session["content"])
            # Chat input
            if st.session_state.prompt:
                # Display user message in chat message container
                with st.expander("user", expanded=True,icon = ":material/person:"):
                    st.write(st.session_state.prompt)
                # Add user message to chat history
                st.session_state.sessions[session_name].append({"role": "user", "content": st.session_state.prompt})

                # Get response from local GPT-2 model

                
                # default to azure openai's model
            

                response=llm_methods.get_openai_response(st.session_state.sessions[session_name]).content


                # Display assistant response in chat message container
                with st.expander("assistant",expanded=True,icon = ":material/smart_toy:"):
                    st.write(response)
                # Add assistant response to chat history
                st.session_state.sessions[session_name].append({"role": "assistant", "content": response})
                st.session_state.prompt=None
            st.session_state.prompt=st.text_area("ask a Question like 'what should i do to maximize my benifets?")