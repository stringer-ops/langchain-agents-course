from pydantic import BaseModel, Field

class AnalysisConclusion(BaseModel):
    punctuation: int = Field(description="""
        An int number between 0 and 100 (both inclusive) that indicates the
        likeliness of getting the job offer. Where 0 meaning having 0 options of getting the job and 100 being 
        a perfect match for the job offer
    """, ge=0, le=100)
    summary: str = Field(description="""
        A quick summary that supports the reasoning you have followed for setting the punctuation and explains why
        the candidate is likely to get (or not) the job
    """)

class AnalysisResult(BaseModel):
    pros: str = Field(description="""
        Strengths of the applicant (if applicable) when comparing its CV to the job description
    """)
    cons: str = Field(description="""
        Points of improvement that the applicant's CV has to make to improve the chances of landing the job
    """)
    conclusion: AnalysisConclusion = Field(description="""
        Punctuation and summary if the applicant might get the job or not
    """)