import streamlit as st

def main():

    st.set_page_config(page_title="AI CV Analysis System")
    st.title("CV Analysis System")
    st.markdown("""
        This system analyzes applicants to a job offer and its CVs using AI.
        The result of the analysis is the likeliness of getting that job offer as well as an analysis
        of the strengths and points of improvement.
            
        The steps it takes are:
        1. Extract key information from PDF CV
        2. Analyzes the applicant's experience and skills
        3. Evaluates the likeliness to get that job offer
        4. Provides objective recommendation
        ---
    """)