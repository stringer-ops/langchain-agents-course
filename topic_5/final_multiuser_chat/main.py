import sqlite3
import uuid
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langgraph.graph import StateGraph, MessagesState, START
from langgraph.checkpoint.sqlite import SqliteSaver

from config import VECTOR_DB_DIR, EMBEDDING_MODEL, LLM_MODEL

load_dotenv()

checkpoint_connection = sqlite3.connect(
    Path(__file__).parent / "chat_history.db", check_same_thread=False
)

llm = ChatOpenAI(model=LLM_MODEL, temperature=0)

def create_user(user: str):
    vector_db = Chroma(
        collection_name=user,
        embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
        persist_directory=VECTOR_DB_DIR
    )

    print(f"Created vector database for '{user}")

    return vector_db


graph = StateGraph(state_schema=MessagesState)

def search_memory(query: str, user: str, k: int = 4):
    """Searchs relevant chunks in vector DB"""

    collection = Chroma(
            collection_name=user,
            embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
            persist_directory=VECTOR_DB_DIR
        )
    
    results = collection.similarity_search(query, k=k)
    return [document.page_content for document in results]

def store_memory(text: str, user: str):
    """Stores relevant user info in vector DB"""

    if text:

        collection = Chroma(
            collection_name=user,
            embedding_function=OpenAIEmbeddings(model=EMBEDDING_MODEL),
            persist_directory=VECTOR_DB_DIR
        )

        collection.add_texts([text], ids=[str(uuid.uuid4())])
        print(f"Stored '{text}' on memory")

def generate_personal_info_extraction_chain():
    """Chain that extracts user info from a message"""
    template = """
        You are a personal data IT expert. Your goal is to extract relevant personal 
        information in simple sentences separated by newlines if there is any. Return empty string if its 
        not relevant.

        E.g 
        1 - 
        Message("Im Json and I play football every weekend")
        **Info extracted** "His name is Json"\n"He likes playing football"

        2 - Message("What is the weather like today")
        **Info extracted** ""

        Message: {message}
    """
    prompt_personal_info = PromptTemplate.from_template(template)

    return prompt_personal_info | llm

user_retrieval_chain = generate_personal_info_extraction_chain()

chat_node_name = "chat_node"
def chat_node(state: MessagesState, config):
    messages = state["messages"]
    user = config["configurable"]["user"]

    #1. Search vector db for content
    last_message = messages[-1].content
    db_data = search_memory(last_message, user)

    #2. Prompt for RAG
    prompt = """You are an assistant that remembers important information about the user 
    in order to provide a better chat experience"""

    if db_data:
        prompt += "\n\nInformation that you remember:"
        for chunk in db_data:
            prompt += f"\n - {chunk}"

    #3. Generate response
    messages_with_system = [SystemMessage(content=prompt)] + messages

    response = llm.invoke(messages_with_system)

    #4. Store relevant info from the user into vector db
    info_extracted = user_retrieval_chain.invoke({"message": last_message})
    
    if info_extracted.content:
        relevant_sentences = info_extracted.content.split('\n')

        for sentence in relevant_sentences:
            store_memory(sentence, user)

    return {"messages": [response]}

graph.add_node(chat_node_name, chat_node)

graph.add_edge(START, chat_node_name)

app = graph.compile(
    checkpointer=SqliteSaver(checkpoint_connection)
)

def chat(message: str, thread_id: str, user: str):

    config = {"configurable": {"thread_id": thread_id, "user": user}}

    response = app.invoke({"messages": [HumanMessage(content=message)]}, config=config)

    return response["messages"][-1].content

