import json

from typing import TypedDict
from langchain_classic.prompts import PromptTemplate
from langchain_classic.schema import StrOutputParser
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from numpy import record

from topic_4.meetings_processor.prompts import (
    PARTICIPANTS_EXTRACTOR, TOPICS_EXTRACTOR, ACTIONS_ITEMS_EXTRACTOR, 
    RECORD_GENERATOR, SUMMARY_GENERATOR
)

LLM_MODEL = "gpt-4o-mini"

chain_participants = None
chain_topics = None
chain_actions_items = None
chain_record = None
chain_summary = None

def init_llm_processors():
    global chain_participants, chain_topics, chain_actions_items, chain_record, chain_summary

    llm_participants = ChatOpenAI(model=LLM_MODEL, temperature=0.0)
    prompt_participants = PromptTemplate.from_template(PARTICIPANTS_EXTRACTOR)
    chain_participants = prompt_participants | llm_participants | StrOutputParser()
    
    llm_topics = ChatOpenAI(model=LLM_MODEL, temperature=0.0)
    chain_topics = PromptTemplate.from_template(TOPICS_EXTRACTOR) | llm_topics | StrOutputParser()

    llm_actions_items = ChatOpenAI(model=LLM_MODEL, temperature=0.0)
    chain_actions_items = PromptTemplate.from_template(ACTIONS_ITEMS_EXTRACTOR) | llm_actions_items | StrOutputParser()

    llm_record = ChatOpenAI(model=LLM_MODEL, temperature=0.0)
    chain_record = PromptTemplate.from_template(RECORD_GENERATOR) | llm_record | StrOutputParser()

    llm_summary = ChatOpenAI(model=LLM_MODEL, temperature=0.0)
    chain_summary = PromptTemplate.from_template(SUMMARY_GENERATOR) | llm_summary | StrOutputParser()

def load_transcript() -> str:
    with open("transcript.txt", "r") as file:
        transcript = file.read()
    return transcript

def main():

    # State definition
    class State(TypedDict):
        notes: str
        participants: list[str]
        topics: list[str]
        actions_items: dict[str, str]
        record: str
        summary: str

    # Graph definition
    graph = StateGraph(State)

    # Models required for each node are initialized
    init_llm_processors()

    # Nodes definition and integrated into the graph
    def extract_participants(state: State):
        print("Extracting participants...")

        response = chain_participants.invoke({"transcript": state["notes"]})

        try:
            participants = json.loads(response)
        except json.JSONDecodeError as e:
            print("Error decoding JSON response for participants:", response, "Error:", e)
            participants = []
        return {"participants": participants}

    def extract_topics(state: State):
        print("Extracting topics...")

        topics = chain_topics.invoke({"transcript": state["notes"]})

        try:
            topics_list = json.loads(topics)
        except json.JSONDecodeError as e:
            print("Error decoding JSON response for topics:", topics, "Error:", e)
            topics_list = []
        return {"topics": topics_list}

    def extract_actions_items(state: State):
        print("Extracting action items...")

        response = chain_actions_items.invoke({"transcript": state["notes"], "participants": state["participants"]})

        try:
            action_items = json.loads(response)
        except json.JSONDecodeError as e:
            print("Error decoding JSON response for action items:", response, "Error:", e)
            action_items = {}
        return {"actions_items": action_items}

    def generate_record(state: State):
        print("Generating record...")

        response = chain_record.invoke({"transcript": state["notes"]})

        if response is None or len(response) == 0:
            print("Error: Record generation returned an empty response.")
            record = ""
        else:
            record = response
        return {"record": record}

    def generate_summary(state: State):
        print("Generating summary...")
        response = chain_summary.invoke({"transcript": state["notes"]})

        if response is None or len(response) == 0:
            print("Error: Summary generation returned an empty response.")
            summary = ""
        else:
            summary = response
        return {"summary": summary}

    extract_participants_node_name = "extract_participants"
    graph.add_node(extract_participants_node_name, extract_participants)

    extract_topics_node_name = "extract_topics"
    graph.add_node(extract_topics_node_name, extract_topics)

    extract_actions_items_node_name = "extract_actions_items"
    graph.add_node(extract_actions_items_node_name, extract_actions_items)

    generate_record_node_name = "generate_record"
    graph.add_node(generate_record_node_name, generate_record)

    generate_summary_node_name = "generate_summary"
    graph.add_node(generate_summary_node_name, generate_summary)

    # Edges that connect the defined nodes
    graph.add_edge(START, extract_participants_node_name)
    graph.add_edge(extract_participants_node_name, extract_topics_node_name)
    graph.add_edge(extract_topics_node_name, extract_actions_items_node_name)
    graph.add_edge(extract_actions_items_node_name, generate_record_node_name)
    graph.add_edge(generate_record_node_name, generate_summary_node_name)
    graph.add_edge(generate_summary_node_name, END)

    # Compile the graph
    graph_compiled = graph.compile()

    # Execute the graph with an initial state
    initial_state = {
        "notes": load_transcript(),
    }
    result = graph_compiled.invoke(initial_state)

    print(result)

main()
