import streamlit as st
from services.inference import evaluate_candidate_chances

def main():

    st.set_page_config(page_title="AI CV Analysis System", layout="wide")
    st.title("📄 CV Analysis System")
    st.markdown("""
        This system analyzes applicants to a job offer and its CVs using AI.
            
        The steps it takes are:
        1. Extract key information from PDF CV
        2. Analyzes the applicant's experience and skills
        3. Evaluates the likeliness to get that job offer
        4. Provides objective recommendation
        ---
    """)

    left_col, right_col = st.columns([1, 2])

    # ---------- LEFT COLUMN --------------

    with left_col:
        
        # -------- UPPER SECTION ------------
        st.subheader("📝 Input Data")
        st.subheader("CV Upload")
        st.markdown(
            """Upload your CV
            The only supported format is: **PDF**"""
        )

        cv = st.file_uploader(
            "Choose a file",
            type=["pdf"]
        )

        st.divider()

        # -------- LOWER SECTION ------------
        st.subheader("Job Offer Description")
        st.markdown("""
            Enter the job offer description you would like to
            apply to
        """)
        job_offer = st.text_area(
            "Job description",
            height=300,
            placeholder="Pase the text here"
        )

        are_all_inputs_completed = (
            cv is not None and job_offer.strip() != ""
        )

        process_clicked = st.button("🔍 Perform Analysis", disabled=not are_all_inputs_completed)
    
    # ---------- RIGHT COLUMN --------------

    with right_col:
        
        # -------- UPPER SECTION ------------
        st.header("📊 Final Analysis")
        st.divider()

        if process_clicked:
            analysis_result = evaluate_candidate_chances(cv, job_offer)

            with st.container(border=True):
                st.markdown("Final conclusions")
                st.write(f"You are {analysis_result['conclusion']['mark']}% likely to get the job")
                st.write(f"Summary: {analysis_result['conclusion']['summary']}")

            with st.container(border=True):
                st.markdown("Strengths")
                st.write("Your strengths are...")
                st.write(analysis_result["pros"])

            with st.container(border=True):
                st.markdown("Points of improvement")
                st.write("Your points to improve are...")
                st.write(analysis_result["cons"])