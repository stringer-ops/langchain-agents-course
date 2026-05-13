from pydantic import BaseModel, Field
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

class TextAnalysis(BaseModel):
    summary: str = Field(description="Small summary of the text")
    feeling: str = Field(description="Feeling of the text. The only posibles values are (positive, negative or neutrum)")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.6
)

structured_llm = llm.with_structured_output(TextAnalysis)
input_text = "I really liked the new movie I've just seen. Its character development is just too clean."

result = structured_llm.invoke(f"Analyze the next text: {input_text}")
print(result)