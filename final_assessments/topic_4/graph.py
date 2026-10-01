from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from items import Ticket, AIResponse, HumanResponse

class State(TypedDict):
    ticket: Ticket

class TicketGraph:
    def __init__(self):
        self.graph = StateGraph(State)
        self.graph_compiled = None

    def initialize_graph(self):

        # Define the nodes
        ai_processing_node = "ai_processing"
        def ai_processing(state: State):
            return ai_processing_node

        human_processing_node = "human_processing" 
        def human_processing(state: State):
            return human_processing_node
        
        self.graph.add_node(ai_processing_node, ai_processing)
        self.graph.add_node(human_processing_node, human_processing)

        # Define the edges
        def branch_ticket_response(state: State):
            ticket = state["ticket"]

            if isinstance(ticket.response, AIResponse):
                return ai_processing_node
            elif isinstance(ticket.response, HumanResponse):
                return human_processing_node
            else:
                pass

        self.graph.add_conditional_edges(START, branch_ticket_response)

        self.graph.add_edge(ai_processing_node, END)
        self.graph.add_edge(human_processing_node, END)

        # Generate invokable graph
        self.graph_compiled = self.graph.compile()

    def execute_graph(self, ticket: Ticket):
        if self.graph_compiled is None:
            raise ValueError("Graph has not been initialized. Call initialize_graph() first.")

        initial_state: State = {"ticket": ticket}
        return self.graph_compiled.invoke(initial_state)

