import streamlit as st

# region <--------- Streamlit App Configuration --------->
st.set_page_config(
    layout="centered",
    page_title="My Streamlit App"
)
# endregion <--------- Streamlit App Configuration --------->

st.title("About this App")

st.header("Project Scope & Objectives")
st.write("This project aims to enhance workplace safety and health knowledge among  workers in Singapore’s construction industry by providing easy access to data published on MOM's website. By providing easy access to vital information, the app seeks to empower workers with the knowledge they need to work safely.")

st.header("Data Sources")
st.write("""
- **Ministry of Manpower (MOM)**: The primary source of data currently includes PDF circulars related to workplace safety and health, released by MOM since year 2000.
""")

st.header("Features")
st.write("""
- **User-Friendly Interface**: Simple input method for users to ask questions about workplace safety and health.
- **Source Citations**: Each response is accompanied by relevant excerpts from MOM documents, enhancing transparency and trust.
""")