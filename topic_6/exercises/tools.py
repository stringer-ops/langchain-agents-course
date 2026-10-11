from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI

load_dotenv()

llm = ChatOpenAI(model="gpt-5.5", temperature=0.2)

@tool("user_db_access")
def custom_tool(query: str) -> str:
    """Queries the company's database and returns query result"""

    return f"Data from query: {query}"

llm_with_tools = llm.bind_tools([custom_tool])

# Model doesnt call the tool. It returns a JSON indicating the tool to call and its arguments
response = llm_with_tools.invoke("Sum up information for user UX1234")

# JSON output from the model into the tool to be executed
tool_response = custom_tool.invoke(response.tool_calls[0])

print(tool_response)