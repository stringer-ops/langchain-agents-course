from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

from config import VECTOR_DB_DIR, EMBEDDING_MODEL, RAG_MODEL, RAG_TEMPERATURE


class RAG:

    def __init__(self):

        self.vector_db = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=OpenAIEmbeddings(
                model=EMBEDDING_MODEL
            )
        )

        self.model = ChatOpenAI(
            model=RAG_MODEL,
            temperature=RAG_TEMPERATURE
        )

    def query_vector_db(self, query: str):
        template_queries = """
            You are a professional HelpDesk assistant. You will be given a description of an issue and you
            have to create 3 similar questions to the given issue description that target the same problem
            separated by a newline. The questions will be send to a RAG (Retrieval-Augmented Generation) system for further processing.
            
            Issue description: {query}
        """
        prompt_queries = PromptTemplate.from_template(template_queries)

        template_retrieval = """
            You are a professional HelpDesk assistant. You will be given a list of information retrieved from
            a RAG (Retrieval-Augmented Generation) system. Your task is to synthesize the information and provide a concise and helpful response.

            Query: {query}
            Retrieved information: {responses}
        """
        prompt_retrieval = PromptTemplate.from_template(template_retrieval)

        rag_chain = (
            prompt_queries | 
            self.model | 
            StrOutputParser() | 
            (lambda queries: [self.vector_db.similarity_search(query) for query in queries.split('\n')]) |
            {
                "responses": (lambda x: '\n\n'.join([str(item) for item in x])),
                "query": RunnablePassthrough()
            } |
            prompt_retrieval |
            self.model |
            StrOutputParser()
        )
        
        result = rag_chain.invoke({"query": query})
        return result








    def query_vector_db(query: str):
        pass

class MultyQueryRetriever:
    pass