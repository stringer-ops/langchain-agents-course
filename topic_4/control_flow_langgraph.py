from typing import TypedDict

from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END

load_dotenv()

class State(TypedDict):
    number: int
    result: str

def main():
    graph = StateGraph(State)

    #Node definition
    def even_case(state: State) -> State:
        return {"result": "Number is even"}
    
    def odd_case(state: State) -> State:
        return {"result": "Number is odd"}
    
    graph.add_node("even", even_case)
    graph.add_node("odd", odd_case)

    #Edges definition
    #Edge conditional function to decide which node to redirect
    def choose_branch(state: State):
        if state["number"] % 2 == 0:
            return "even"
        else:
            return "odd"

    #Conditional edge added to workflow 
    graph.add_conditional_edges(START, choose_branch)
    #Regular edges added to workflow
    graph.add_edge("even", END)
    graph.add_edge("odd", END)

    compiled = graph.compile()

    #Test the conditional graph
    print(compiled.invoke({"number": 4})["result"])

if __name__ == "__main__":
    main()