from pathlib import Path

from langchain_classic.retrievers import MultiQueryRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_docling import DoclingLoader

from final_assessments.topic_3.prompts.prompts import SYSTEM_PROMPT
from config.config import (
    VECTOR_DB_DIR, EMBEDDING_MODEL, QUERY_MODEL, GENERATION_MODEL, SEARCH_TYPE, MMR_DIVERSITY_LAMBDA,
    SEARCH_K, MMR_FETCH_K
)

def create_rag_chain() -> None:

    if Path(VECTOR_DB_DIR).exists():
        vector_db = Chroma(
            persist_directory=str(VECTOR_DB_DIR),
            embedding_function=GoogleGenerativeAIEmbeddings(model = EMBEDDING_MODEL)
        )
    else:
        raise ValueError(f"Vector database is not created or is not configured properly")

    #Model to process the user input fot the vector db query
    llm_query = ChatGoogleGenerativeAI(model=QUERY_MODEL, temperature=0)

    #Model ****
    llm_generation = ChatGoogleGenerativeAI(model=GENERATION_MODEL, temperature=0)

    #Retriever MMR (Maximal Margin Relevance)
    #Used when retrieving chunks from query. Balances precision with variability
    base_retriever = vector_db.as_retriever(
        search_type=SEARCH_TYPE,
        search_kwargs={
            "k": SEARCH_K,
            "lambda_mult": MMR_DIVERSITY_LAMBDA,
            "fetch_k": MMR_FETCH_K
        }
    )