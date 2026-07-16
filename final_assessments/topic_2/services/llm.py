from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_google_genai import ChatGoogleGenerativeAI
from prompts.system_prompt import SYSTEM_PROMPT
from models.models import AnalysisResult

def initialize_evaluator_llm() -> RunnableSequence:
    """Generates a LangChain chain with LLM that evaluates CV + job description"""
    
    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", "CV: {cv_text}"),
            ("human", "Job Description: {job_description}")
        ]
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.4
    )

    structured_llm = llm.with_structured_output(AnalysisResult)

    chain = prompt_template | structured_llm

    return chain