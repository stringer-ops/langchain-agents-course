from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define the state schema
class State(TypedDict):
    original_text: str
    uppercase_text: str
    length: int

# 2. Create the state graph
graph = StateGraph(State)

# 3. Define node functions
def to_uppercase(state: State):
    text = state["original_text"]
    return {"uppercase_text": text.upper()}

def calculate_length(state: State):
    text = state["original_text"]
    return {"length": len(text)}

# 4. Add nodes to the graph
graph.add_node("uppercase", to_uppercase)
graph.add_node("count", calculate_length)

# 5. Connect nodes as a sequence
graph.add_edge(START, "uppercase")
graph.add_edge("uppercase", "count")
graph.add_edge("count", END)

# 6. Compile the graph
compiled_graph = graph.compile()

# 7. Execute the graph with an initial state
initial_state = {"original_text": "Hello, world"}
result = compiled_graph.invoke(initial_state)
print(result)