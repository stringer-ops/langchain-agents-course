from pathlib import Path

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_docling import DoclingLoader
from dotenv import load_dotenv

from config import DOCS_DIR, VECTOR_DB_DIR, EMBEDDING_MODEL

load_dotenv()

def main() -> None:

    files_paths = [
        str(path) for path in Path(DOCS_DIR).glob("*.md")
    ]

    print(f"Loading a total amount of {len(files_paths)} documents")

    #Text splitting with chunk overlap to enhance chunk context and avoid data loss
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=40,
    )

    docs_splitted = text_splitter.split_documents(
        DoclingLoader(files_paths).load()
    )

    #Format metadata to the desired format
    final_docs_splitted = []
    for doc in docs_splitted:
        new_metadata = {}
        dl_meta = doc.metadata.get("dl_meta", {})
        origin = dl_meta.get("origin", {})
        new_metadata["source"] = origin.get("filename")
        new_metadata["mimetype"] = origin.get("mimetype")

        doc.metadata = new_metadata
        final_docs_splitted.append(doc)

    docs_splitted = final_docs_splitted

    print(f"Successfully generated {len(docs_splitted)} chunks of text from the documents")

    # Create embedding model and vector store
    embedding_model = OpenAIEmbeddings(
        model=EMBEDDING_MODEL
    )

    if not VECTOR_DB_DIR.exists():
        VECTOR_DB_DIR.mkdir(parents=True)

        vector_store = Chroma.from_documents(
            documents=docs_splitted,
            embedding=embedding_model,
            persist_directory=str(VECTOR_DB_DIR)
        )

        print(f"Created vector database at {VECTOR_DB_DIR}")

    else:
        vector_store = Chroma(
            persist_directory=str(VECTOR_DB_DIR),
            embedding_function=embedding_model
        )

        print(f"Recovered existing vector database at {VECTOR_DB_DIR}")

if __name__ == "__main__":
    main()