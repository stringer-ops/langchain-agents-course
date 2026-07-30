from langchain_chroma import Chroma
from langchain_classic.prompts import PromptTemplate
from pathlib import Path
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_classic.retrievers import MultiQueryRetriever
from langchain_openai import ChatOpenAI

from config import *
from models import RetrievalAnalysisModel
from items import Ticket

class TicketRAGProcessor:
    def __init__(self):
        self.retriever = self.create_rag_retriever()

    def create_rag_retriever(self) -> MultiQueryRetriever:

        # Initialize the Chroma vector store
        if Path(VECTOR_DB_DIR).exists():
            vector_store = Chroma(
                persist_directory=str(VECTOR_DB_DIR),
                embedding_function=OpenAIEmbeddings(model = EMBEDDING_MODEL)
            )
        else:
            raise ValueError("Vector database is not created or is not configured properly")

        base_retriever = vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={
                "k": SEARCH_K,
            }
        )

        llm_query = ChatOpenAI(model=MODEL, temperature=0)

        MULTI_QUERY_PROMPT = """You are an expert IT support agent. 
            You will be given a ticket description of an incidence and your task is to generate 
            3-5 relevant queries that can be used to retrieve information from a knowledge base. 
            The queries should be concise, clear, and focused on the key issues presented in the ticket. 
            Avoid redundancy and ensure that each query addresses a unique aspect of the problem.
            Ticket Description: {ticket_description}
        """
        multi_query_prompt = PromptTemplate.from_template(MULTI_QUERY_PROMPT)
        mmr_multi_retriever = MultiQueryRetriever.from_llm(
            retriever=base_retriever,
            llm=llm_query,
            prompt=multi_query_prompt
        )

        return mmr_multi_retriever

    def retrieve_relevant_documents(self, ticket: Ticket):
        """Analyze a ticket and retrieve relevant documents."""
        query = ticket.description
        retrieved_docs = self.retriever.invoke({"ticket_description": query})
        return retrieved_docs

    def format_retrieved_documents(self, retrieved_docs: list[Document]) -> str:
        """Format the retrieved documents into a string for further processing."""
        formatted_docs = "\n\n".join(
            [
                f"Document {doc.metadata.get('source', 'Unknown source')}:\n{doc.page_content}" 
                for doc in retrieved_docs
            ]
        )
        return formatted_docs
    
    def analyze_ticket(self, ticket: Ticket):
        """Analyze a ticket and retrieve relevant documents."""
        retrieved_docs = self.retrieve_relevant_documents(ticket)

        formatted_docs = self.format_retrieved_documents(retrieved_docs)

        RETRIEVAL_ANALYSIS_PROMPT = """You are an expert IT support agent.
            You will be given a ticket description and a set of retrieved documents.
            Your task is to analyze the ticket and the documents, and provide a response for the issue
            
            Documents: {retrieved_documents}
            Ticket Description: {ticket_description}"""

        retrieval_analysis_prompt = PromptTemplate.from_template(RETRIEVAL_ANALYSIS_PROMPT)
        llm_analysis = ChatOpenAI(model=MODEL, temperature=0)
        llm_structured_analysis = llm_analysis.with_structured_output(RetrievalAnalysisModel)

        chain = retrieval_analysis_prompt | llm_structured_analysis
        analysis_result = chain.invoke({
            "ticket_description": ticket.description,
            "retrieved_documents": formatted_docs
        })
        return analysis_result