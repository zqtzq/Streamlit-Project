import streamlit as st
# import sys
# import os

# sys.path.append(os.path.dirname(os.path.abspath(__file__)))


import streamlit as st  
from helper_functions.utility import check_password  

# Check if the password is correct.  
if not check_password():  
    st.stop()

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->
from logics.query_handler import process_user_message
from logics.query_handler import translate_output_chinese
from logics.query_handler import translate_output_bengali


with st.expander("IMPORTANT NOTICE (expand to view):"):
        st.write(
            "This web application is a prototype developed for educational purposes only. "
            "The information provided here is NOT intended for real-world usage and should not be relied upon for making any decisions, "
            "especially those related to financial, legal, or healthcare matters. "
            "Furthermore, please be aware that the LLM may generate inaccurate or incorrect information. "
            "You assume full responsibility for how you use any generated output. "
            "Always consult with qualified professionals for accurate and personalized advice."
        )

# Title of the app
st.title("Ask your questions on MOM's published circulars:")

# Form for user input
form = st.form(key="form")
form.subheader("Question:")

user_prompt = form.text_area("eg. Can excavators be used as lifting machines? What are the trainings requirements for workplace safety and health coordinator?", height=200)

if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    
    # Call the process_user_message function and get the response
    response = process_user_message(user_prompt)
    
    # Display the response
    st.write("Response:")
    st.write(response['result'])
    
    # Display source documents as clickable links
    st.write("Source URL(s):")
    urls = [doc.metadata['url'] for doc in response['source_documents']]
    unique_urls = list(set(urls))  # Use set to ensure URLs are unique

    clickable_urls = [f"[{url}]({url})" for url in unique_urls]  # Create clickable links
    st.markdown(", ".join(clickable_urls), unsafe_allow_html=True)


    translated_message_chinese = translate_output_chinese(response)
    st.write("Chinese translation:")
    st.write(translated_message_chinese)

    translated_message_bengali = translate_output_bengali(response)
    st.write("Bengali translation:")
    st.write(translated_message_bengali)