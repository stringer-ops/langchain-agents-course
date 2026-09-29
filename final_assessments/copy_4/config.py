from pathlib import Path

#Paths
DOCS_DIR = Path(__file__).parent / "docs"
VECTOR_DB_DIR = Path(__file__).parent / "vector_db"

#Retriever config
SEARCH_K = 3 #Final chunks obtained

ENABLE_HYBRID_SEARCH = True #Enables hybrid search, combines semantic and keyword search
SIMILARITY_THRESHOLD = 0.75 #Similarity threshold for hybrid search

#Models
#Embedding model used to create the vector database
EMBEDDING_MODEL = "text-embedding-3-large"

#Model used to process user input and generate several queries for retrieval. Simple task
MODEL = "gpt-4.1-mini"

#Use case
CONFIDENCE_THRESHOLD = 0.75 #Confidence threshold for retrieval analysis. If the confidence is below this value, the ticket will be escalated to human intervention