
from services.llm import initialize_evaluator_llm
from services.pdf_extractor import extract_pdf_text

def evaluate_candidate_chances(cv_pdf: str, job_offer: str) -> dict:
    """Triggers the inference process passing the LLM the CV in text format
    and the job description. Returns a dictionary with pros, cons and a conclusion"""

    chain = initialize_evaluator_llm()

    result = chain.invoke(
        cv_text = cv_pdf,
        job_description = job_offer
    )

    result = result.model_dump()

    return result



