from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-5.5", temperature=0.3)

history = ChatPromptTemplate.from_messages([
    SystemMessage(content="You are a useful AI agent"),
    MessagesPlaceholder(variable_name="conversation")
])

chain = history | llm

messages = []

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

    human_message = HumanMessage(content=user_query)

    messages.append(human_message)

    ai_response = chain.invoke({
            "conversation": messages
        }
    )

    messages.append(ai_response)

    print("Agent: ", ai_response.content)

    