import uuid
from datetime import datetime

TICKET_STATUSES = ["Open", "Human Intervention", "Resolved"]

class Response:
    def __init__(self, conclusion: str = None):
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class AIResponse(Response):
    def __init__(self, conclusion: str = None, score: float = None, sources: list = []):
        super().__init__(conclusion)
        self.score = score
        self.conclusion = conclusion
        self.sources = sources

class HumanResponse(Response):
    def __init__(self, human_answer: str = None, enriched_context: str = None):
        super().__init__()
        self.human_answer = human_answer
        self.enriched_context = enriched_context

class Ticket:
    def __init__(self, description, user):
        self.ticket_id = self._generate_id()
        self.description = description
        self.user = user
        self.status = "Open"
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.ai_response = None
        self.human_response = None

    def update_status(self, new_status):
        if new_status in TICKET_STATUSES:
            self.status = new_status
        else:
            raise ValueError(f"Invalid status: {new_status}")

    def _generate_id(self) -> str:
        return f"TK-{str(uuid.uuid4())[:8]}"

    def __str__(self) -> str:
        return f"{self.ticket_id} - {self.created_at}"