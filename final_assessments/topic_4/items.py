import uuid
from datetime import datetime

TICKET_STATUSES = ["Open", "Human Intervention", "Resolved", "Closed"]

class Response:
    def __init__(self):
        self.response_text = None
        self.confidence_score = None
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

class AIResponse(Response):
    def __init__(self):
        super().__init__()
        self.sources = []

class HumanResponse(Response):
    def __init__(self):
        super().__init__()
        self.ticket_context = None
        self.human_content = None

class Ticket:
    def __init__(self, description, user):
        self.ticket_id = self._generate_id()
        self.description = description
        self.user = user
        self.status = "Open"
        self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.solution = None

    def update_status(self, new_status):
        if new_status in TICKET_STATUSES:
            self.status = new_status
        else:
            raise ValueError(f"Invalid status: {new_status}")

    def _generate_id(self) -> str:
        return f"TK-{str(uuid.uuid4())[:8]}"

    def __str__(self) -> str:
        return f"{self.ticket_id} - {self.created_at}"