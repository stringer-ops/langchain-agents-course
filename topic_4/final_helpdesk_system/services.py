from dotenv import load_dotenv

from langchain_core.prompts import PromptTemplate
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document
from langchain_core.load import dumps, loads

from schemas import RAGResponse

from config import VECTOR_DB_DIR, EMBEDDING_MODEL, RAG_MODEL, RAG_TEMPERATURE

load_dotenv()

class RAGSystem:

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

        self.rag_chain = self._build_rag_chain()

    def _generate_multiple_queries_chain(self) -> RunnableSerializable:

        template = """
            You are a professional HelpDesk assistant. You will be given a description of an issue and you
            have to create 3 similar questions to the given issue description that target the same problem
            separated by a newline. The questions will be send to a RAG (Retrieval-Augmented Generation) 
            system for further processing. Separate each question with a newline
            
            Issue description: {query}
        """
        prompt = PromptTemplate.from_template(template)

        return prompt | self.model | StrOutputParser() | (lambda x: x.split('\n'))


    def _generate_multi_query_retrieval_chain(self) -> RunnableSerializable:

        retriever = self.vector_db.as_retriever(
            search_type="similarity",
        )

        def parse_retrieved_response(docs: list[list]):

            unique_docs = list(set([dumps(doc) for sublist in docs for doc in sublist]))
            unique_docs = [loads(doc_str, allowed_objects=[Document]) for doc_str in unique_docs]

            formated = '\n\n'.join([
                f"""
                    Source name: {doc.metadata["source"]}
                    Content: {doc.page_content}
                """ for doc in unique_docs
            ])

            # Return both the prompt-ready text and the original documents.
            return {"chunks": formated, "documents": unique_docs}

        return retriever.map() | RunnableLambda(parse_retrieved_response)


    def _build_rag_chain(self) -> RunnableSerializable:
    
        template = """
            You are a professional RAG entity. You will be given retrieved information and a given issue.
            Your goal is to issue that question using that information.

            The issue might not be related at all with the information given by the RAG system or it might be difficult
            to precisely asses a solution with this. A human technician

            Issue: {issue}

            Information: {chunks}
        """

        prompt = PromptTemplate.from_template(template)

        multi_query_chain = self._generate_multiple_queries_chain()
        retrieval_chain = self._generate_multi_query_retrieval_chain()
        
        # Retrieval is executed once. Its text goes to the model and its raw
        # Document objects are retained in the final result.
        return (
            {
                "retrieval": multi_query_chain | retrieval_chain,
                "issue": RunnablePassthrough(),
            }
            | RunnablePassthrough.assign(
                chunks=lambda value: value["retrieval"]["chunks"]
            )
            | RunnablePassthrough.assign(
                response=prompt | self.model.with_structured_output(RAGResponse)
            )
            | {
                "response": lambda value: value["response"],
                "documents": lambda value: value["retrieval"]["documents"],
            }
        )


    def consult_query(self, query: str) -> dict:

        if self.rag_chain is None:
            self.rag_chain = self._build_rag_chain()

        return self.rag_chain.invoke(query)

class EnrichContext:

    def __init__(self):

        self.model = ChatOpenAI(
            model=RAG_MODEL,
            temperature=RAG_TEMPERATURE
        )

        self.chain = self._create_chain_context_for_humans()

    def _create_chain_context_for_humans(self):

        template = """
            You are an expert HelpDesk assistant. You have a long, proven record solving IT issues.
            You are practical and precise, you can extract the most of available documentation but also
            know which battles aren't worth fighting, if you dont know or the documentation isn't clear you delegate.

            Your duty is to give context for another fellow assistant to help solve an issue given some documentation.

            Issue: {issue}
            Documentation: {documentation}
        """
        prompt = PromptTemplate.from_template(template)

        return prompt | self.model | StrOutputParser()

    def _parse_docs(self, docs: list[Document]):

        return '\n\n'.join([str(doc) for doc in docs])

    def geneate_context(self, docs: list[Document], issue: str):

        parsed_docs = self._parse_docs(docs)
        return self.chain.invoke({"documentation": parsed_docs, "issue": issue})



if __name__ == "__main__":
    r = RAGSystem()
    result = r.consult_query("Como puedo pausar mi suscripción temporalmetne?")

    documents = result["documents"]
    conclusion = result["response"].conclusion

    print(conclusion)
    print(documents)
