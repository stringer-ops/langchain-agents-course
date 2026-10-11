from dotenv import load_dotenv
from langchain.agents import create_agent
from langgraph.prebuilt import create_react_agent
from langgraph_supervisor import create_supervisor
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-5.5", temperature=0)

power_llm = ChatOpenAI(model="gpt-6.1-sol", use_responses_api=True, reasoning_effort="low")

#Define tools
@tool
def search_web(query: str) -> str:
    """Search information on the Internet"""

    return f"Search results for : {query}"

@tool
def calculate(expression: str) -> str:
    """Perform math calculation"""

    return f"Result: {eval(expression)}"

# Create specialized agents
investigation_agent = create_agent(
    model=llm,
    tools=[search_web],
    system_prompt="You are a specialist investigatin on the Internet",
    name="investigation_agent"
)

calculation_agent = create_agent(
    model=llm,
    tools=[calculate],
    system_prompt="You are a specialist doint maths calculation",
    name="calculation_agent"
)

# Create supervisor agent
supervisor_graph = create_supervisor(
    agents=[investigation_agent, calculation_agent],
    model=power_llm,
    prompt="You are supervisor that delegates tasks to specialists depending on the task",
    verbose=True
)

supervisor = supervisor_graph.compile()

#Response (as seen in LangGraph) contains the final state of the Graph
response = supervisor.invoke({
    "messages": [{
            "role": "user",
            "content": "Search information about 3.1415 and calculate its value multiplying by 2"
        }
    ]}
)

for message in response["messages"]:
    print(message.content)