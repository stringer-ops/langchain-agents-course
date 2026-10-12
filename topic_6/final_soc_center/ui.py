import requests
import streamlit as st

from generate_incidents import generate_incident

PROCESS_INCIDENT_URL = "http://127.0.0.1:8000/api/process_incident"


def main():
    st.set_page_config(page_title="SOC Center", page_icon="🛡️")
    st.title("SOC Center")
    st.caption("Generate a mock incident to investigate.")

    if "incident" not in st.session_state:
        st.session_state.incident = None
    if "analysis" not in st.session_state:
        st.session_state.analysis = None
    if "analysis_error" not in st.session_state:
        st.session_state.analysis_error = None

    if st.button("Generate incident", type="primary"):
        st.session_state.incident = generate_incident()
        st.session_state.analysis = None
        st.session_state.analysis_error = None

        # The mock incidents omit this API-required field. Keep it disabled for
        # generated examples unless the UI later exposes it as a user option.
        payload = {**st.session_state.incident, "real_apis": False}

        try:
            with st.spinner("Analyzing incident..."):
                api_response = requests.post(
                    PROCESS_INCIDENT_URL,
                    json=payload,
                    timeout=180,
                )
                api_response.raise_for_status()
                st.session_state.analysis = api_response.json()
        except requests.RequestException as error:
            st.session_state.analysis_error = str(error)


    st.subheader("Incident")
    response_area = st.container(border=True)

    with response_area:
        if st.session_state.incident is None:
            st.info("Generate an incident to see its details here.")
        else:
            st.json(st.session_state.incident)

    st.subheader("Analysis")
    analysis_area = st.container(border=True)

    with analysis_area:
        if st.session_state.analysis_error:
            st.error(
                "The backend could not process the incident. "
                f"{st.session_state.analysis_error}"
            )
        elif st.session_state.analysis is None:
            st.info("The supervisor's conclusion will appear here.")
        else:
            st.json(st.session_state.analysis)


if __name__ == "__main__":
    main()
