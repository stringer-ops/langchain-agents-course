"""Central configuration for the multi-user chat application."""

from pathlib import Path

# Chroma stores each user's long-term memory in a collection under this folder.
VECTOR_DB_DIR = Path(__file__).parent / "vector_db"

# Model choices are kept here so the UI and backend share the same settings.
EMBEDDING_MODEL = "text-embedding-3-large"

LLM_MODEL = "gpt-5.5"
