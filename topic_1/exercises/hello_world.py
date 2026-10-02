from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

question = "In which year did the human race get to the Moon for the first time?"
print(f"The question is: '{question}'")

answer = llm.invoke(question)
print(f"The LLM answer is: '{answer.invalid_tool_callscontent}'")

