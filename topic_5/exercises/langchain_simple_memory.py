from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_openai import ChatOpenAI

from uuid import uuid4

load_dotenv()

llm = ChatOpenAI(model="gpt-5.5", temperature=0.3)

history = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a useful AI agent"),
    MessagesPlaceholder(variable_name="conversation"),
    ("user", "{input}")
])

chain = history | llm

store = {}

def get_session_history(session_id: str):
    if session_id not in store:
        store[session_id] = InMemoryChatMessageHistory()
    
    return store[session_id]

# Chain with automatic session memory
chain_with_memory = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="input",
    history_messages_key="conversation"
)

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

    ai_response = chain_with_memory.invoke(
        {"input": user_query},
        config={"configurable": {"session_id": session_id}}
    )

    print("Agent: ", ai_response.content)

    