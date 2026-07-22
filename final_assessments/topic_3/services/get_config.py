

from final_assessments.topic_3.config.config import (
    ENABLE_HYBRID_SEARCH, SEARCH_TYPE, EMBEDDING_MODEL, GENERATION_MODEL, MMR_DIVERSITY_LAMBDA, QUERY_MODEL, SEARCH_K, 
    MMR_FETCH_K, SIMILARITY_THRESHOLD
)


def get_retriever_info():
    """Returns the retriever information for display in the UI"""
    return {
        "search_type": f"{SEARCH_TYPE.upper()} + Multiquery" + (" + Hybrid" if ENABLE_HYBRID_SEARCH else ""),
        "total_chunks": SEARCH_K,
        "candidate_chunks": MMR_FETCH_K,
        "diversity": MMR_DIVERSITY_LAMBDA,
        "umbral": SIMILARITY_THRESHOLD if ENABLE_HYBRID_SEARCH else "N/A"
    }

def get_model_info():
    """Returns the model information for display in the UI"""
    return {
        "embedding": EMBEDDING_MODEL,
        "query": QUERY_MODEL,
        "generation": GENERATION_MODEL
    }