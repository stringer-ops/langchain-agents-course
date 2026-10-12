from fastapi import APIRouter, Request

from backend.schemas import ProcessIncidentRequest

router = APIRouter(
    prefix="/api"
)


@router.get("/health")
async def health():
    return {
        "health": "Everything works fine!"
    }


@router.post("/process_incident")
async def process_incident(incident_data: ProcessIncidentRequest, request: Request):
    supervisor = request.app.state.supervisor
    response = await supervisor.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "Analyze this cybersecurity incident and return a conclusion: "
                        f"{incident_data.model_dump_json()}"
                    ),
                }
            ]
        }
    )

    return response["structured_response"]

