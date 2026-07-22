from pathlib import Path

import streamlit as st
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.documents import Document
from langchain_classic.retrievers import MultiQueryRetriever, EnsembleRetriever
from langchain_classic.schema import StrOutputParser
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma

from final_assessments.topic_3.prompts.prompts import MULTI_QUERY_PROMPT, RAG_TEMPLATE
from config.config import (
    ENABLE_HYBRID_SEARCH, SIMILARITY_THRESHOLD, VECTOR_DB_DIR, EMBEDDING_MODEL, QUERY_MODEL, GENERATION_MODEL, SEARCH_TYPE, MMR_DIVERSITY_LAMBDA,
    SEARCH_K, MMR_FETCH_K
)

#Stored the function as cache to speed up creating the web interface, since this is immutable
@st.cache_resource
def create_rag_chain() -> tuple[RunnableSerializable, MultiQueryRetriever]:
    """Generates the RAG LCEL chain to process the user input and generate the final answer"""

    if Path(VECTOR_DB_DIR).exists():
        vector_db = Chroma(
            persist_directory=str(VECTOR_DB_DIR),
            embedding_function=GoogleGenerativeAIEmbeddings(model = EMBEDDING_MODEL)
        )
    else:
        raise ValueError("Vector database is not created or is not configured properly")

    #Model to process the user input fot the vector db query
    llm_query = ChatGoogleGenerativeAI(model=QUERY_MODEL, temperature=0)

    #Model ****
    llm_generation = ChatGoogleGenerativeAI(model=GENERATION_MODEL, temperature=0)

    #Retrievers
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

    #Similarity retriever. Used along MultiQueryRetriever to perform hybrid search
    similarity_retriever = vector_db.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": SEARCH_K
        }
    )

    #Retriever instanced. MultiQuery generates several queries with simple LLM model
    multi_query_prompt = PromptTemplate.from_template(MULTI_QUERY_PROMPT)
    mmr_multi_retriever = MultiQueryRetriever.from_llm(
        base_retriever=base_retriever,
        llm=llm_query,
        prompt=multi_query_prompt
    )

    if ENABLE_HYBRID_SEARCH:
        hybrid_retriever = EnsembleRetriever(
            retrievers=[mmr_multi_retriever, similarity_retriever],
            weights=[0.7, 0.3],  # More weight for MMR
            # It is applied once the results are obtained, to filter the final results. It is applied to the similarity retriever results
            similarity_threshold=SIMILARITY_THRESHOLD 
        )
        final_retriever = hybrid_retriever
    else:
        final_retriever = mmr_multi_retriever

    system_prompt = PromptTemplate.from_template(RAG_TEMPLATE)

    #Function to format and preprocess retrieved documents
    def format_docs(docs: list[Document]) -> str:
        """Formats the retrieved documents by adding context information to help LLM reasoning process"""

        formatted_docs = []
        for i, doc in enumerate(docs, 1):
            header = f"[Fragment {i}]"

            if doc.metadata:
                if 'source' in doc.metadata:
                    source = doc.metadata['source'].split("\\")[-1] if '\\' in doc.metadata['source'] else doc.metadata['source']
                    header += f" (Source: {source})"
                if 'page' in doc.metadata:
                    header += f" (Page: {doc.metadata['page']})"

            content = doc.page_content.strip()
            formatted_docs.append(f"{header}\n{content}")

        return "\n\n".join(formatted_docs)

    #RAG chain
    #The dictionary are the arguments that the "system_prompt > RAG_TEMPLATE" expects
    chain = ( {
        "context": final_retriever | format_docs,
        #Placeholder for the question. It is not defined yet
        "question": RunnablePassthrough(),
        } 
        | system_prompt
        | llm_generation
        | StrOutputParser()
    )

    return chain, final_retriever

def query_rag(question: str) -> tuple[str | None, list[dict] | None]:
    """Queries the RAG chain with the user question and returns the answer and relevant documents"""
    try:
        rag_chain, retriever = create_rag_chain()

        #Get answer
        response = rag_chain.invoke(question)

        #Get relevant documents
        docs = retriever.invoke(question)

        docs_info = []
        for i, doc in enumerate(docs[:SEARCH_K], 1):
            docs_info.append({
                "fragment": i,
                "content": doc.page_content[:1000] + "..." if len(doc.page_content) > 1000 else doc.page_content,
                "source": doc.metadata.get("source", "Unknown"),
            })

    except Exception as e:
        st.error(f"Error processing the query: {e}")
        return None, None
    else:
        return response, docs_info