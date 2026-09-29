from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from config import VECTOR_DB_DIR, EMBEDDING_MODEL


class RAG:

    def __init__(self):

        self.vector_db = Chroma(
            persist_directory=VECTOR_DB_DIR,
            embedding_function=OpenAIEmbeddings(
                model=EMBEDDING_MODEL
            )
        )

    def query_vector_db(query: str):
        pass

class MultyQueryRetriever:
    pass