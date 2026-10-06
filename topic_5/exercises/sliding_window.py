from dotenv import load_dotenv
from langgraph.graph import MessagesState, StateGraph, START
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage, trim_messages
from langchain_openai import ChatOpenAI

from uuid import uuid4

load_dotenv()

# Class used as messages. It uses this change of name for improved readability
class WindowedState(MessagesState):
    pass

llm = ChatOpenAI(model="gpt-5.5", temperature=0.3)

# State is not defined, we pass it one predefined
graph = StateGraph(state_schema=WindowedState)

# Keeps the last 6 messages. The first message kept is always from human
# and System Prompt is always kept
trimmer = trim_messages(
    strategy="last",
    max_tokens=50,
    token_counter=len,
    start_on="human",
    include_system=True
)

# Message history is kept fully on the graph, but only the trimmed messages are passed to the LLM
def chatbot_node(state):
    """Node that processes messages and generates responses"""

    trimed_messages = trimmer.invoke(state["messages"])

    system_prompt = """You are a friendly assistant"""
    messages = [SystemMessage(content=system_prompt)] + trimed_messages

    response = llm.invoke(messages)

    # "messages" is a list, when we return the new message like that is added
    return {"messages": [response]}

graph.add_node("chatbot", chatbot_node)
graph.add_edge(START, "chatbot")

# Chat will be saved in RAM with MemorySaver()
compiled = graph.compile(
    checkpointer=MemorySaver()
)

def chat(message, thread_id="terminal_session"):
    config = {"configurable": {"thread_id": thread_id}}
    result = compiled.invoke({"messages": [HumanMessage(content=message)]}, config)

    return result["messages"][-1].content

print("Terminal Chat (write 'quit' to exit the chat)")

session_id = uuid4()

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

    ai_response = chat(user_query)

    print("Agent: ", ai_response)

    