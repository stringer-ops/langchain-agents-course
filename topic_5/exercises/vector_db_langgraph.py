import uuid
from pathlib import Path
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_chroma import Chroma
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
import chromadb

load_dotenv()

VECTOR_DB_DIR = Path(__file__).parent / "vector_db"

llm = ChatOpenAI(model="gpt-5.5", temperature=0)

# Vector DB configuration + insertion and retrieval
vector_db = Chroma(
    collection_name="memoria_chat",
    embedding_function=OpenAIEmbeddings(model="text-embedding-3-large"),
    persist_directory=VECTOR_DB_DIR
)

client = chromadb.PersistentClient(path=VECTOR_DB_DIR)
collection = client.get_collection("memoria_chat")

def store_memory(text):
    """Stores relevant user info in vector DB"""

    collection.add(
        documents=[text],
        ids=[str(uuid.uuid4())]
    )
    print(f"Stored '{text}' on memory")


def search_memory(query, k=3):
    """Searchs relevant chunks in vector DB"""

    results = collection.query(
        query_texts=[query],
        n_results=k
    )

    return results['documents'][0] if results['documents'] else []

# Graph

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

extraction_chain = generate_personal_info_extraction_chain()

def chatbot_node(state):
    """Main graph node"""
    messages = state['messages']
    last_message = messages[-1].content if messages else ""

    #1. Search vector db for content
    db_data = search_memory(last_message)

    #2. Prompt for RAG
    prompt = "You are an assistant that remembers important information"

    if db_data:
        prompt += "\n\nInformation that you remember:"
        for chunk in db_data:
            prompt += f"\n - {chunk}"

    #3. Generate response
    messages_with_system = [SystemMessage(content=prompt)] + messages

    response = llm.invoke(messages_with_system)

    #4. Store relevant info from the user into vector db
    info_extracted = extraction_chain.invoke({"message": last_message})
    
    if info_extracted.content:
        relevant_sentences = info_extracted.content.split('\n')

        for sentence in relevant_sentences:
            store_memory(sentence)

    return {"messages": [response]}

graph = StateGraph(state_schema=MessagesState)
graph.add_node("chatbot", chatbot_node)
graph.add_edge(START, "chatbot")

compiled = graph.compile(
    checkpointer=MemorySaver()
)

def chat(message, thread_id="terminal_session"):
    config = {"configurable": {"thread_id": thread_id}}
    result = compiled.invoke({"messages": HumanMessage(content=message)}, config)

    return result["messages"][-1].content

def show_memories():
    """Show all user data collected"""

    all_memories = collection.get()

    if all_memories['documents']:
        print("Stored user data")
        for i, memory in enumerate(all_memories['documents'], 1):
            print(f"{i} - {memory}")
    else:
        print('No data stored from the user')

print("Terminal Chat (write 'quit' to exit the chat)")

while True:
    try:
        user_query = input("You: ").strip()

    except (EOFError, KeyboardInterrupt):
        print("Bye bye")
        break

    if not user_query:
        continue

    if user_query.lower() in ["exit", "quit"]:
        print("Bye bye")
        break

    if user_query.lower() == 'user_data':
        show_memories()
        continue

    ai_response = chat(user_query)

    print("Agent: ", ai_response)




