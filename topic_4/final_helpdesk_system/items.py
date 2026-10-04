import uuid
from datetime import datetime

TICKET_STATUSES = ["Open", "Human Intervention", "Resolved"]

class Response:
    """Base class that records when a ticket response was created."""

    def __init__(self, conclusion: str = None):
        """Initialize the response timestamp."""
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class AIResponse(Response):
    """Store an automated RAG answer, its confidence, and its sources."""

    def __init__(self, conclusion: str = None, score: float = None, sources: list = []):
        """Initialize an AI-generated response."""
        super().__init__(conclusion)
        self.score = score
        self.conclusion = conclusion
        self.sources = sources

class HumanResponse(Response):
    """Store the human resolution and the context prepared for that technician."""

    def __init__(self, human_answer: str = None, enriched_context: str = None):
        """Initialize an empty human response and optional support context."""
        super().__init__()
        self.human_answer = human_answer
        self.enriched_context = enriched_context

class Ticket:
    """Represent a helpdesk request and its automated or human resolution."""

    def __init__(self, description, user):
        """Create an open ticket for the supplied user and issue description."""
        self.ticket_id = self._generate_id()
        self.description = description
        self.user = user
        self.status = "Open"
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ai_response = None
        self.human_response = None

    def update_status(self, new_status):
        """Set a valid ticket status or raise an error for an unknown value."""
        if new_status in TICKET_STATUSES:
            self.status = new_status
        else:
            raise ValueError(f"Invalid status: {new_status}")

    def _generate_id(self) -> str:
        """Create a short, unique identifier suitable for display."""
        return f"TK-{str(uuid.uuid4())[:8]}"

    def __str__(self) -> str:
        """Return a compact textual representation of the ticket."""
        return f"{self.ticket_id} - {self.created_at}"
