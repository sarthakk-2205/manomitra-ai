
import re

# Basic phrase screening only; this is not a clinical classifier.
RISK_PATTERNS = [
    r"\bkill myself\b",
    r"\bend my life\b",
    r"\bsuicid(?:e|al)\b",
    r"\bhurt myself\b",
    r"\bself[- ]harm\b",
    r"\bi don't want to live\b",
    r"\bi want to die\b",
    r"\bcan't keep myself safe\b",
]

def check_safety(message: str) -> dict:
    text = message.lower()

    possible_risk = any(
        re.search(pattern, text)
        for pattern in RISK_PATTERNS
    )

    if possible_risk:
        return {
            "possible_risk": True,
            "message": (
                "I'm sorry you're going through this. You deserve "
                "support from a real person right now. If you may "
                "act on these thoughts or are in immediate danger, "
                "call India's emergency number 112 or go to the "
                "nearest emergency department. You can also call "
                "Tele-MANAS at 14416 for mental-health support. "
                "If possible, reach out to someone you trust and "
                "stay with them. ManoMitra cannot provide emergency "
                "monitoring or guarantee your safety."
            ),
            "resources": [
                {"name": "Tele-MANAS", "phone": "14416"},
                {"name": "Emergency services", "phone": "112"},
            ],
        }

    return {
        "possible_risk": False,
        "message": None,
        "resources": [],
    }
