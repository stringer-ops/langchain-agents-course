from pydantic import BaseModel, Field, model_validator

from config import CONFIDENCE_THRESHOLD

class RAGResponse(BaseModel):
    """Validate the structured answer returned by the RAG model."""

    conclusion: str | None= Field(description=f"""The answer given to the question by using the RAG answer. If the score
        score is low, in this conclusion will be indicated that a human technician will solve it.

        Empty if the score is lower than {CONFIDENCE_THRESHOLD}
    """)
    
    score: float = Field(description="""
        A 2 decimal float that ranges from 0 to 1. It indicates the correlation between the issue given and how accurate is the
        retreived information and the ability to solve that issue with that retrieved info. 0 will be given if the
        RAG response is nothing related with the issue and 1 will be given if the issue can be fully resolved with
        the retrieved answer
    """)

    sources: list[str] = Field(description=f"""
        The name of the files that contained the valuable chunks used to generate your conclusion.
        You can leave it empty list if the score is lower than {CONFIDENCE_THRESHOLD} and you consider it doesn't help for the issue.""")

    justification: str = Field(description="""Quick explanation on the reasoning behind why the score is the number it is""")

    @model_validator(mode="after")
    def clear_conclusion_when_score_is_low(self):
        """Remove an AI conclusion when confidence requires human escalation."""
        if self.score < CONFIDENCE_THRESHOLD:
            self.conclusion = None
        return self
