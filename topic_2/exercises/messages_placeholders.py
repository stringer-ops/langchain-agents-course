from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder


chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a useful assistant that keeps track of the context of the conversation"),
    MessagesPlaceholder(variable_name="historic"),
    ("human", "{user_input}")
])

#A message history is simulated
message_history = [
    HumanMessage(content="Which city is the capital of France?"),
    AIMessage(content="The capital of France is Paris"),
    HumanMessage(content="How many people live in Paris?"),
    HumanMessage(content="Paris has approximately 2.2 million people living there")
]

messages = chat_prompt.format_messages(
    historic=message_history,
    user_input="Is there any city in France bigger than Paris?"
)

print(messages)