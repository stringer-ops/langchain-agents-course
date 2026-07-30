from typing import TypedDict
from langgraph.graph import StateGraph, START, END

from config import CONFIDENCE_THRESHOLD
from rag import TicketRAGProcessor
from items import HumanResponse, Ticket, AIResponse
from langchain_core.documents import Document

class State(TypedDict):
    ticket: Ticket

class HelpDeskGraph:
    def __init__(self):
        self.rag_system = TicketRAGProcessor()
        self.graph_compiled = None

    def build_graph(self):
        graph = StateGraph(State)

        # Define states
        graph.add_node("process_ticket", self.process_ticket)

        # Define transitions
        graph.add_edge(START, "process_ticket")
        graph.add_edge("process_ticket", END)

        self.graph_compiled = graph.compile()

    def execute_graph(self, ticket: Ticket):
        if self.graph_compiled is None:
            self.build_graph()

        initial_state: State = {"ticket": ticket}
        final_state = self.graph_compiled.invoke(initial_state)
        return final_state

    def process_ticket(self, state: State):
        ticket = state["ticket"]
        analysis_result = self.rag_system.analyze_ticket(ticket).model_dump()

        if analysis_result["confidence"] < CONFIDENCE_THRESHOLD:
            ticket.update_status("Human Intervention")

            solution= HumanResponse()
            solution.response_text = analysis_result["answer"]
            solution.confidence_score = analysis_result["confidence"]

            ticket.solution = solution
        else:
            solution= AIResponse()
            solution.response_text = analysis_result["answer"]
            solution.confidence_score = analysis_result["confidence"]
            ticket.update_status("Resolved")

        return {"ticket": ticket}
