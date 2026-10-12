from enum import Enum
from pydantic import BaseModel, Field

class Severity(str, Enum):
    """Severity of the incident"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Diagnostic(str, Enum):
    """Diagnostic of the incident"""

    FALSE_POSITIVE = "false_positive"
    DOUBT = "doubt"
    THREAT = "threat"


class ProcessIncidentRequest(BaseModel):
    """Request data regarding a cybersecurity incident"""

    source: str = Field(description="Source that generated the incident")
    alert_type: str = Field(description="Type of security threat that generated the incident")
    severity: Severity = Field("Severity of the incident")
    message: str = Field(description="Description of the incident")
    source_ip: str | None = Field(description="Source IP that generated the threat")
    destination_ip: str | None = Field(description="Destination IP that generated the threat")
    url: str = Field(description="URL that generated the threat")
    file_hash: str = Field(description="Hash of the file that generated the threat")
    real_apis: bool = Field(description="If the system is allowed to use real APIs to investigate the ")
    incident_id: str = Field(description="Identifier of the incident")


class IncidentConclusion(BaseModel):
    """Formated conclusion to the incident processed"""

    conclusion: str = Field(description="Description of the incident and the reasoning on the results")
    diagnostic: Diagnostic = Field(description="Diagnostic of the incident")
    measurements: str = Field(description="Measurements to take on the incident")
    confidence: float = Field(description="A number from 0 meaning no confidence to 1 meaning full confidence on the diagnostic of the incident")