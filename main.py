__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import streamlit as st
from logics.query_handler import process_user_message # note that this is logics.query_handler and not just query_handler as the query_handler.py file is inside the logics folder

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

# import streamlit as st  
# from helper_functions.utility import check_password  

# # Check if the password is correct.  
# if not check_password():  
#     st.stop()

st.title("Streamlit App")

form = st.form(key="form")
form.subheader("Prompt")

user_prompt = form.text_area("Enter your prompt here", height=200)


if form.form_submit_button("Submit"):
    st.toast(f"User Input Submitted - {user_prompt}")
    response = process_user_message(user_prompt) # This calls the 'process_user_message' function from the 'query_handler.py' file
    st.write(response)
    print(f"User Input is {user_prompt}")

