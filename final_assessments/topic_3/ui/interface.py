import streamlit as st
from langchain.messages import AIMessage
from langchain.messages import HumanMessage

def clear_chat() -> None:
    st.session_state.messages = []

def main() -> None:
    st.set_page_config(page_title="Document Chat", layout="wide")
    st.title("⚖️ RAG System - Legal Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.sidebar:
        st.header("🗒️ System Information")

        st.subheader("🔎 Retrieval")
        st.markdown("- **LLM**: GPT-4o-mini")

        st.subheader("⚙️ Models")
        st.markdown("- **Algorithms**: RAG + similarity search")

        st.divider()

        st.subheader("Chat Controls")
        st.button("Clear chat", on_click=clear_chat, use_container_width=True)

    chat_col, controls_col = st.columns([2.5, 1.5])
    with chat_col:
        st.title("💬 Chat")

        for message in st.session_state.messages:
            role = "assistant" if isinstance(message, AIMessage) else "user"
            with st.chat_message(role):
                st.write(message.content)

        user_prompt = st.chat_input("Ask a question about your documents...")
        if user_prompt:
            
            with st.chat_message("user"):
                st.write(user_prompt)

            st.session_state.messages.append(HumanMessage(content=user_prompt))

            assistant_reply = (
                "I received your question. Connect this UI to your retrieval/inference layer "
                "to answer using the selected documents."
            )
            try:
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()
                    full_response = assistant_reply

                    #TODO: change this to invoke + stream
                    response_placeholder.markdown(full_response)
                
            except Exception as e:
                st.error(f"Error when generating an answer: {str(e)}")
            else:
                st.session_state.messages.append(AIMessage(content=assistant_reply))

    with controls_col:
        st.subheader("📄 Documents Referenced")

        num_dropdowns = 2

        sample_options = ["All documents", "Document A", "Document B", "Document C"]
        for index in range(num_dropdowns):
            st.selectbox(
                label=f"Selector {index + 1}",
                options=sample_options,
                key=f"selector_{index}",
            )


if __name__ == "__main__":
    main()
