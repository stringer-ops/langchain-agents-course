from pathlib import Path

#Paths
CONTRACTS_DIR = Path(__file__).parent.parent / "data" / "contracts"
VECTOR_DB_DIR = Path(__file__).parent.parent / "data" / "vector_db"

#Retriever config
SEARCH_TYPE = "mmr" #Search type performed in retriever
MMR_DIVERSITY_LAMBDA = 0.7 #0 -> more diversity, 1 -> more relevant (less diverse)
MMR_FETCH_K = 20 #Chunks initially analyzed before applying MMR
SEARCH_K = 2 #Final chunks obtained

ENABLE_HYBRID_SEARCH = True #Enables hybrid search, combines semantic and keyword search
SIMILARITY_THRESHOLD = 0.75 #Similarity threshold for hybrid search

#Models
#Embedding model used to create the vector database
EMBEDDING_MODEL = "gemini-embedding-001"

#Model used to process user input and generate several queries for retrieval. Simple task
QUERY_MODEL = "gemini-2.0-flash-lite"
GENERATION_MODEL = "gemini-2.0-flash"