import streamlit as st

def main():

    st.set_page_config(page_title="AI CV Analysis System", layout="wide")
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

    left_col, right_col = st.columns([1, 2])

    # ---------- LEFT COLUMN --------------

    with left_col:
        
        # -------- UPPER SECTION ------------
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

        process_clicked = st.button("Perform Analysis", disabled=not are_all_inputs_completed)
    
    # ---------- RIGHT COLUMN --------------

    with right_col:
        
        # -------- UPPER SECTION ------------
        st.header("Final Analysis")
        st.divider()

        if process_clicked:
            with st.container(border=True):
                st.markdown("Strengths")
                st.write("Your strneghts are...")

            with st.container(border=True):
                st.markdown("Points of improvement")
                st.write("Your points to improve are...")
            
            with st.container(border=True):
                st.markdown("Final conclusions")
                st.write("The final conclusions are...")

            
        
    