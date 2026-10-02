from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_core.documents import Document

from items import Ticket, AIResponse, HumanResponse
from services import RAGSystem, EnrichContext
from config import CONFIDENCE_THRESHOLD

class State(TypedDict):
    ticket: Ticket
    rag_docs: list[Document]

class TicketGraph:
    def __init__(self):
        self.graph_compiled = None
        self.rag_system = RAGSystem()
        self.context_system = EnrichContext()

    def initialize_graph(self):

        # Define the nodes
        rag_node = "rag_processing"
        def rag_processing(state: State) -> State:
            ticket = state["ticket"]
            rag_result = self.rag_system.consult_query(ticket.description)
            response = rag_result["response"]

            ticket.ai_response = AIResponse(
                conclusion=response.conclusion,
                score=response.score,
                sources=response.sources
            )

            return {
                "ticket": ticket, 
                "rag_docs": rag_result["documents"]
            }

        ai_processing_node = "ai_processing"
        def ai_processing(state: State) -> State:

            ticket = state["ticket"]
            ticket.update_status("Resolved")

            return {"ticket": ticket}

        human_processing_node = "human_processing" 
        def human_processing(state: State) -> State:

            ticket = state["ticket"]
            documents= state["rag_docs"]
            ticket.update_status("Human Intervention")

            ticket.human_response = HumanResponse(
                enriched_context=self.context_system.geneate_context(
                    documents, ticket.description
                )
            )
            
            return {"ticket": ticket}

        graph = StateGraph(State)

        graph.add_node(rag_node, rag_processing)
        graph.add_node(ai_processing_node, ai_processing)
        graph.add_node(human_processing_node, human_processing)

        # Define the edges       
        def branch_ticket_response(state: State):
            ticket = state["ticket"]

            if ticket.ai_response.score > CONFIDENCE_THRESHOLD:
                return ai_processing_node
            return human_processing_node


        graph.add_edge(START, rag_node)
        graph.add_conditional_edges(rag_node, branch_ticket_response)
        graph.add_edge(ai_processing_node, END)
        graph.add_edge(human_processing_node, END)

        # Generate invokable graph
        return graph.compile()

    def execute_graph(self, ticket: Ticket):
        if self.graph_compiled is None:
            self.graph_compiled = self.initialize_graph()

        initial_state: State = {"ticket": ticket, "rag_docs": None}
        return self.graph_compiled.invoke(initial_state)