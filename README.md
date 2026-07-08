# Curso Completo: LangChain, LangGraph y AI Agents with Python

This repository contains exercises and final assessments for the Udemy Business course:

- [Course: Curso Completo: LangChain, LangGraph y Agentes IA con Python | Udemy](https://www.udemy.com/course/curso-completo-langchain-langgraph-y-agentes-ia-con-python/)

## Purpose

This project gathers hands-on examples to learn how to build applications with:

- Foundations of LangChain & LLM Apps — Build LangChain LLM applications with prompts, chains, and LCEL.

- Memory & Context Management — Manage conversational context and different types of memory with LangGraph.

- AI Agents & Tool Integration — Create tool-using agents that interact with APIs and external service.

- RAG & Vector Databases — Implement retrieval pipelines using embeddings and vector databases for accurate knowledge retrieval.

- Production-Ready AI Systems — Develop scalable AI workflows with FastAPI, Streamlit, and multi-agent architectures.

## Repository Structure

```text
.
|- topic_<n>/                 # Exercises for each course topic (topic_1, topic_2, ...)
|- final_assessments/
|  \- topic_<n>/             # Final assessment for each topic
|- pyproject.toml            # Project metadata and dependencies
\- README.md                # Project documentation
```

### Generic folder conventions

- `topic_<n>/`: incremental topic folders that contain scripts, examples, and experiments.
- `final_assessments/topic_<n>/`: final project or assessment implementation for each topic.
- `pyproject.toml`: dependency and Python version management.

## Requirements

- Python 3.10 or higher
- A valid API key for Google AI Studio (Gemini)

## Installation

### Option 1: using `uv` (recommended)

```bash
uv sync
```

### Option 2: using `venv` + `pip`

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Environment Variables

Create a `.env` file in the repository root:

```env
GOOGLE_API_KEY=your_api_key_here
```

## Running Exercises

Examples by topic:

```bash
python topic_1/hello_world.py
python topic_1/hello_world_advanced.py
python topic_2/example_runnables.py
python topic_2/output_parser.py
```

Streamlit examples:

```bash
streamlit run topic_1/streamlit_chatbot.py
streamlit run topic_2/enhanced_chatbot.py
streamlit run final_assessments/topic_1/streamlit_chatbot.py
```

Final assessment example:

```bash
streamlit run final_assessments/topic_2/main.py
```

## Main Dependencies

- langchain
- langchain-google-genai
- streamlit
- python-dotenv
- markitdown

## Note

This repository is focused on practice and learning. Some scripts may evolve during the course and are not intended to represent production-ready architecture.
