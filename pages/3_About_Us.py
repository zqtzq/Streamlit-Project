import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.write(" With the diverse construction workforce in Singapore, many construction workers and supervisors hail from different countries, and may struggle to fully understand the safety materials, circulars and guidelines due to language barriers. Although the Construction Safety Orientation Course (CSOC) that is compulsory for all workers to attend introduces some English terms, the time constrains in the course does not allow the course instructors to fully introduce the technical terms specialised in each trade [1]." )
         
st.write("The importance of considering language and cultural diversity in occupational safety cannot be overstated, as depicted in [2]. This app aims to bridge the gap by providing a user-friendly interface for workers to ask questions about workplace safety and health in their native language. The app then provide responses in English, along with translations in the workers' native language, and accompanied by relevant URLs to the circulars, for further verfication to enhance the trustworthiness and reliability of the information provided.")

st.header("Project Scope & Objectives")
st.markdown(
    """
    This project aims to enhance workplace safety and health knowledge among workers in Singapore’s construction industry by:

    1. Providing a user-friendly interface for workers to ask questions about workplace safety and health in English or their native language.
    2. Extracting key information from the circulars published on MOM's website and translating it into the workers' native language.
    3. Providing URLs to cite the responses for verification and to obtain further information on the topic.

    By providing easy access to these information, the app seeks to empower workers with the knowledge they need to work safely.
    """
)


st.header("Data Sources")
st.write("""
- **Ministry of Manpower (MOM)**: The primary source of data currently includes PDF circulars related to workplace safety and health, released by MOM since year 2000.
""")

st.header("Features")
st.write("""
- **User-Friendly Interface**: Simple input method for users to ask questions about workplace safety and health in the language most comfortable to them, with the ability to search for relevant information from the circulars even when the question is not in English language.
- **Source Citations**: Each response is accompanied by relevant excerpts from MOM documents, enhancing transparency.
- **Translation of Responses**: Each response is translated to Chinese and Bengali if the user asks the question in English. If the user asks the question in Chinese or Bengali, the response will be in Chinese or Bengali.

""")