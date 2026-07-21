from pathlib import Path

#Paths
CONTRACTS_DIR = Path(__file__).parent.parent / "data" / "contracts"
VECTOR_DB_DIR = Path(__file__).parent.parent / "data" / "vector_db"

#Retriever config
SEARCH_TYPE = "mmr" #Search type performed in retriever
MMR_DIVERSITY_LAMBDA = 0.7 #0 -> more diversity, 1 -> more relevant (less diverse)
MMR_FETCH_K = 20 #Chunks initially analyzed before applying MMR
SEARCH_K = 2 #Final chunks obtained

#Models
EMBEDDING_MODEL = "gemini-embedding-001"
QUERY_MODEL = ""
GENERATION_MODEL = ""