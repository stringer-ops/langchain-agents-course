import numpy as np
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()

embeddings = GoogleGenerativeAIEmbeddings(
    model="gemini-embedding-001"
)

query_1 = "The capital of France is Paris"
query_2 = "Paris is the city which is capital of France"

vector_1 = embeddings.embed_query(query_1)
vector_2 = embeddings.embed_query(query_2)

cos_sim = np.dot(vector_1, vector_2) / (np.linalg.norm(vector_1) * np.linalg.norm(vector_2))

print(f"Dimension of vectors: {len(vector_1)}")
print(f"Similarity between vector 1 and vector 2: {cos_sim:.3f}")