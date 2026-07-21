from pathlib import Path

from langchain_classic.retrievers import MultiQueryRetriever
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableSequence
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_docling import DoclingLoader

from final_assessments.topic_3.prompts.system_prompt import SYSTEM_PROMPT

CONTRACTS_DIR = Path(__file__).parent.parent / "data" / "contracts"
VECTOR_DB_DIR = Path(__file__).parent.parent / "data" / "vector_db"

def create_llm_chain() -> RunnableSequence:
    """Creates a LangChain chain with LLM that answers questions about documents"""
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0
    )

    prompt_template = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("placeholder", "Conversation with the client: {conversation_history}"),
        ]
    )

    llm_chain = prompt_template | llm

    return llm_chain

def create_vector_db():
    """Creates a vector database from the documents in the contracts directory"""
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
        [DoclingLoader(path).load() for path in files_paths]
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

    return vector_store

def create_retriever() -> MultiQueryRetriever:
    """Creates a MultiQueryRetriever that retrieves relevant documents based on user queries"""

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
        [DoclingLoader(path).load() for path in files_paths]
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

    #TODO: cover this case
    else:
        vector_store = Chroma(
            persist_directory=str(VECTOR_DB_DIR),
            embedding_function=embedding_model
        )

        print(f"Recovered existing vector database at {VECTOR_DB_DIR}")

    retriever = MultiQueryRetriever(
        vectorstore=vector_store,
        search_kwargs={"k": 2},
        llm_chain=create_llm_chain()
    )

    print("Successfully created MultiQueryRetriever")

    return retriever