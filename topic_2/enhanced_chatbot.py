from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.messages.system import SystemMessage
from langchain_core.prompts import ChatPromptTemplate
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

#Configuring the web page
st.set_page_config(page_title="Basic Chatbot", page_icon="🤖")
st.title("🤖 Basic Chatbot with Langchain")
st.markdown("This is an *example chabot* built with Langchain + Streamlit. Write down your message to get started!")

#Defining a sidebar for configurating temperature and model
with st.sidebar:
    st.header("Configuration")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.5, 0.1)
    model_name = st.selectbox("Model", ["gemini-2.5-flash"])

    if st.button("New Conversation"):
        st.session_state.messages = []
    
    # ¿Cómo recrearías el modelo con los nuevos parámetros?
    chat_model = ChatGoogleGenerativeAI(model=model_name, temperature=temperature)

system_prompt = """
    You are a personal assistant called Chatbot PRO. Your duty is to help
    the user in the tasks and questions that could come across. It is important
    to take in count the whole given context and to answer any question in a clear concise way
"""

#Initializing the Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "{system_prompt}"),
    ("placeholder", "{message_history}"),
    ("human", "{user_input}")
])

chain = prompt | chat_model

#Initializing the message history
if "messages" not in st.session_state:
    st.session_state.messages = []

#Showing current message history
for message in st.session_state.messages:
    #System Messages aren't showed
    if isinstance(message, SystemMessage):
        continue

    role = "assistant" if isinstance(message, AIMessage) else "user"

    with st.chat_message(role):
        st.markdown(message.content)

#Input textbox for the user input
question = st.chat_input("Write your message: ")

if question:
    #Show immediately the message on the screen
    with st.chat_message("user"):
        st.markdown(question)

    try:
        #Show answer on the interface with streaming
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""
 
            #Generate answer using the LLM model. Answer is received in streaming mode (one chunk at a time)
            for chunk in chain.stream({
                "system_prompt": system_prompt,
                "user_input": question,
                "message_history": st.session_state.messages
            }):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")  # El cursor parpadeante
            
            response_placeholder.markdown(full_response)
    
    except Exception as e:
        st.error(f"Error when generating an answer: {str(e)}")
    else:
        #Human question is stored on the chat history Streamlit memory
        st.session_state.messages.append(HumanMessage(content=question))
        #Answer is stored in the message history (is already an AIMessage object)
        st.session_state.messages.append(AIMessage(content=full_response))