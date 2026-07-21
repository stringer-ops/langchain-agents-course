from pathlib import Path

from langchain_classic.retrievers import MultiQueryRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_docling import DoclingLoader
from dotenv import load_dotenv

from prompts.system_prompt import SYSTEM_PROMPT
from config.config import CONTRACTS_DIR, VECTOR_DB_DIR

load_dotenv()

def main() -> None:

    files_paths = [
        str(path) for path in Path(CONTRACTS_DIR).glob("*.pdf")
    ]

    print(f"Loading a total amount of {len(files_paths)} documents")

    #Text splitting with chunk overlap to enhance chunk context and avoid data loss
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=1000,
    )

    docs_splitted = text_splitter.split_documents(
        DoclingLoader(files_paths).load()
    )

    print(f"Successfully generated {len(docs_splitted)} chunks of text from the documents")

    # Create embedding model and vector store
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001"
    )

    if not VECTOR_DB_DIR.exists():
        VECTOR_DB_DIR.mkdir(parents=True)

        vector_store = Chroma.from_documents(
            docs_splitted,
            embedding_function=embedding_model,
            persist_directory=str(VECTOR_DB_DIR)
        )

        print(f"Created vector database at {VECTOR_DB_DIR}")

    else:
        vector_store = Chroma(
            persist_directory=str(VECTOR_DB_DIR),
            embedding_function=embedding_model
        )

        print(f"Recovered existing vector database at {VECTOR_DB_DIR}")

def test():

    files_paths = [
        str(path) for path in Path(CONTRACTS_DIR).glob("*.pdf")
    ]

    print(f"Loading a total amount of {len(files_paths)} documents")

    #Text splitting with chunk overlap to enhance chunk context and avoid data loss
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=5000,
        chunk_overlap=1000,
    )


    docs_splitted = text_splitter.split_documents(
        DoclingLoader(files_paths).load()
    )

    print(f"Successfully generated {len(docs_splitted)} chunks of text from the documents")

main()