from pathlib import Path

from dotenv import load_dotenv

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_docling.loader import DoclingLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

from config import DOCS_DIR, VECTOR_DB_DIR, EMBEDDING_MODEL

load_dotenv()

def main():

    # 1 - Document loading
    files_paths = [
        str(path) for path in Path(DOCS_DIR).glob("*.md")
    ]
    
    loader = DoclingLoader(files_paths)
    docs = loader.load()

    print(f"{len(docs)} documents successfully loaded")

    # 2- Document chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 200,
        chunk_overlap = 40
    )

    chunks = splitter.split_documents(docs)

    print(f"{len(chunks)} chunks successfully generated")

    #Format metadata to the desired format
    final_docs_splitted = []
    for doc in chunks:
        new_metadata = {}
        dl_meta = doc.metadata.get("dl_meta", {})
        origin = dl_meta.get("origin", {})
        new_metadata["source"] = origin.get("filename")
        new_metadata["mimetype"] = origin.get("mimetype")

        doc.metadata = new_metadata
        final_docs_splitted.append(doc)

    # 3 - Embbeding of documents
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    vector_db_dir = Path(VECTOR_DB_DIR)
    if not vector_db_dir.exists():

        vector_db_dir.mkdir(parents=True)

        vector_db = Chroma.from_documents(
            documents=final_docs_splitted,
            embedding=embeddings,
            persist_directory=str(vector_db_dir)
        )

        print(f"{len(chunks)} chunks successfully introduced into vector DB at {VECTOR_DB_DIR}")
    else:
        print(f"vector DB at {VECTOR_DB_DIR} already exists")

if __name__ == "__main__":
    main()