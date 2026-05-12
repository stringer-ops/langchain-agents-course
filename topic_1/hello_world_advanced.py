from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.chains import LLMChain

load_dotenv()

chat = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7)

template = PromptTemplate(
    input_variables=["name"],
    template="Say hello to the user with their own name.\nName of the user {name}\nAssistant:"
)

chain = LLMChain(llm=chat, prompt=template)

result = chain.run(name="Charlie")
print(result)



