"""Mock cybersecurity incidents for testing the SOC Center frontend and API."""

from copy import deepcopy
from random import choice


MOCK_INCIDENTS = [
    {
        "source": "Microsoft Defender for Endpoint",
        "alert_type": "Malware detected",
        "severity": "high",
        "message": "A suspicious executable was detected and quarantined on WS-FIN-014.",
        "source_ip": "10.20.14.35",
        "destination_ip": None,
        "url": "",
        "file_hash": "44d88612fea8a8f36de82e1278abb02f",
        "incident_id": "INC-2026-0001",
    },
    {
        "source": "Okta",
        "alert_type": "Multiple failed logins",
        "severity": "medium",
        "message": "Twelve failed login attempts were detected for a finance user account.",
        "source_ip": "198.51.100.42",
        "destination_ip": "203.0.113.15",
        "url": "",
        "file_hash": "",
        "incident_id": "INC-2026-0002",
    },
    {
        "source": "Cloudflare Gateway",
        "alert_type": "Phishing URL accessed",
        "severity": "high",
        "message": "A user attempted to visit a domain classified as credential phishing.",
        "source_ip": "10.20.8.61",
        "destination_ip": "203.0.113.80",
        "url": "https://secure-login-example.test/office365",
        "file_hash": "",
        "incident_id": "INC-2026-0003",
    },
    {
        "source": "Suricata IDS",
        "alert_type": "Command and control traffic",
        "severity": "critical",
        "message": "Possible C2 beaconing detected every 60 seconds from an internal host.",
        "source_ip": "10.20.14.35",
        "destination_ip": "192.0.2.91",
        "url": "",
        "file_hash": "",
        "incident_id": "INC-2026-0004",
    },
    {
        "source": "AWS GuardDuty",
        "alert_type": "Credential exposure",
        "severity": "critical",
        "message": "An access key may have been used from an anomalous external location.",
        "source_ip": "198.51.100.177",
        "destination_ip": "203.0.113.25",
        "url": "",
        "file_hash": "",
        "incident_id": "INC-2026-0005",
    },
    {
        "source": "CrowdStrike Falcon",
        "alert_type": "Suspicious PowerShell execution",
        "severity": "high",
        "message": "Encoded PowerShell executed from a temporary user directory.",
        "source_ip": "10.20.10.22",
        "destination_ip": None,
        "url": "",
        "file_hash": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        "incident_id": "INC-2026-0006",
    },
    {
        "source": "Azure AD Identity Protection",
        "alert_type": "Impossible travel",
        "severity": "low",
        "message": "A sign-in from Madrid was followed by a sign-in from Sydney within 18 minutes.",
        "source_ip": "203.0.113.44",
        "destination_ip": "203.0.113.15",
        "url": "",
        "file_hash": "",
        "incident_id": "INC-2026-0007",
    },
]


def generate_incident() -> dict:
    """Return a new copy of one randomly selected mock incident."""
    return deepcopy(choice(MOCK_INCIDENTS))
