import streamlit as st
from langchain.messages import AIMessage
from langchain.messages import HumanMessage

from services.rag import query_rag
from services.get_config import get_retriever_info, get_model_info

def clear_chat() -> None:
    st.session_state.messages = []

def main() -> None:
    st.set_page_config(page_title="Document Chat", layout="wide")
    st.title("⚖️ RAG System - Legal Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "docs_info" not in st.session_state:
        st.session_state.docs_info = []

    with st.sidebar:

        st.header("🗒️ System Information")
        model_info = get_model_info()

        st.markdown("⚙️ Retriever")
        for key, value in model_info.items():
            st.markdown(f"- **{key.capitalize()} Model**: {value}")

        st.divider()

        st.subheader("🔎 RAG Configuration")
        retriever_info = get_retriever_info()
        for key, value in retriever_info.items():
            st.markdown(f"- **{key.replace('_', ' ').capitalize()}**: {value}")

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

            try:
                with st.chat_message("assistant"):
                    response_placeholder = st.empty()

                    #TODO: change this to invoke + stream
                    rag_response, docs_info = query_rag(user_prompt)
                    if rag_response:
                        response_placeholder.markdown(rag_response)
                    st.session_state.docs_info = docs_info if docs_info else []
                
            except Exception as e:
                st.error(f"Error when generating an answer: {str(e)}")
            else:
                st.session_state.messages.append(AIMessage(content=rag_response))

    with controls_col:
        st.subheader("📄 Documents Referenced")
        docs_info = st.session_state.get("docs_info", [])

        if docs_info:
            st.markdown("📄 Documents referenced")
            for index, doc_info in enumerate(docs_info, start=1):
                title = None
                if isinstance(doc_info, dict):
                    title = doc_info.get("document") or doc_info.get("source") or doc_info.get("title")

                label = title if title else f"Document {index}"
                with st.expander(label):
                    if isinstance(doc_info, dict):
                        for key, value in doc_info.items():
                            st.markdown(f"**{key.replace('_', ' ').title()}**: {value}")
                    else:
                        st.write(doc_info)
        else:
            st.caption("No referenced documents yet.")


if __name__ == "__main__":
    main()
