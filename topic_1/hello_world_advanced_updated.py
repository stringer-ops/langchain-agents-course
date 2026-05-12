from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

load_dotenv()

chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

template = PromptTemplate(
    input_variables=["name"],
    template="Say hello to the user with their own name.\nName of the user {name}\nAssistant:"
)

#This interface to invoke the chain is based on Linux pipes (e.g, cat my_file.txt | grep "name")
chain = template | chat

result = chain.invoke({"name":"Charlie"})
print(result.content)



